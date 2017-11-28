from TensorFlowObject import TensorFlowObject
import time
from threading import Thread
from DataGatherer import DataGatherer
import sys
from Constantes import Constantes
import os
from AppGetter import AppGetter
import pandas as pd
from CPUChargeGenerator import CPUChargeGenerator
import multiprocessing as mp
import datetime
import platform
import importlib as il

now = datetime.datetime.now()

class DataTrainer(Thread):


    def __init__(self):
        Thread.__init__(self)
        self.dg = DataGatherer()
        self.columns  = self.dg.getColumns()
        self.cons = Constantes(self.columns)
        self.ten =TensorFlowObject(self.cons)
        if platform.system() == 'Linux':
            from LinuxCL import ChargeListener
        elif platform.system() == 'Windows':
            from WindowsCL import ChargeListener

	
        self.cl = ChargeListener()
        self.kill = False
        self.rawdatas=self.formatDatas(self.columns)
        self.testDatas = self.formatDatas(self.columns)
        self.status=None
        self.AppGetter = None
        self.CPUChargeGenerators = []
        self.fichierLog = None
        if self.cons.is_log_enabled() :
           self.fichierLog = open(self.cons.get_log_file_name(),"a")





    def run(self):
        result=self.CPUChargeGenerator_start(1000)
        try:
            self.cl.start()
            i=0
            needTrain = True
            while(True and not self.kill):
                self.status = self.cl.getStatus()

                #si l'ordinateur se decharge, on recupere les donnees"""
                if self.status == "Discharging":
                    #on formatte le tableau de donnee
                    #self.rawdatas = self.formatDatas(self.columns)
                    #on recupere les donnees
                    self.gatherDatas(self.rawdatas)
                    if self.cons.is_log_enabled() is True:
                        self.fichierLog.write(now.strftime("%Y-%m-%d %H:%M:  ") + "status: Discharging\n")
                        self.fichierLog.write(now.strftime("%Y-%m-%d %H:%M:  ")+"need train?: " +str(needTrain)+"\n")
                        self.fichierLog.flush()
                    if needTrain == True:
                        if(i%10== 0):
                            self.gatherDatas(self.testDatas)
                        if(self.ten.checkModel(self.toDict(self.testDatas,self.columns)) == True):
                            needTrain=False
                        i+=1

                #si l'ordinateur charge,on enregistre les donnees si il y en a
                elif len(self.rawdatas[0]) >0:
                    #on transforme les donnee en dictionnaire
                    if self.cons.is_log_enabled() is True:
                        self.fichierLog.write(now.strftime("%Y-%m-%d %H:%M:  ") + "status: Charging\n")
                    dictData = self.toDict(self.rawdatas,self.columns)
                    data_set = pd.DataFrame(dictData,columns = self.columns)

                    #on train tensorflow avec ces donnee
                    self.ten.StartTrain(data_set)
                    self.rawdatas=self.formatDatas(self.columns)
                time.sleep(2)

            self.cl.kill = True
        except (KeyboardInterrupt, SystemExit):
            self.kill = True
            self.cl.kill = True
            if self.fichierLog != None:
                self.fichierLog.close()

    """
    ajoute les donnees a la liste
    """
    def gatherDatas(self,liste):
        datas = self.dg.getDatas()
        for i in range(len(datas)):
            liste[i].append(datas[i])
        
    #ajoute les donnes de application a la liste (formatee au prealable)
    def gatherAppDatas(self,liste):
        datas = self.AppGetter.getAppDatas()
        for j in range(len(datas)):
            for i in range(len(datas[j])):
                liste[i].append(datas[j][i])


    """
    retourne un dictionnaire a partir de datas
    """
    def toDict(self,datas,columns):
        dictData={}
        if self.cons.is_log_enabled() is True:
            self.fichierLog.write(now.strftime("%Y-%m-%d %H:%M: "))
            self.fichierLog.flush()
        for i in range(len(datas)):
            dictData[columns[i]] = datas[i]
            
            if self.cons.is_log_enabled() is True:
                self.fichierLog.write(columns[i]+": "+str(datas[i])+"\n")
                self.fichierLog.flush()
        return dictData
    """
    formatte le tableau avec len(columns) cases
    """
    def formatDatas(self,columns):
        rawdatas = []
        for i in columns:
           rawdatas.append([])
        return rawdatas

    """
    ne garde que les colonnes dans featuresget
    """

    def popBattery(self,dictionnaire):
        dictPredict2={}
        for i in self.cons.get_features():
            dictPredict2[i] = dictionnaire[i]
        return dictPredict2

    def getTensorFlow(self):
        return self.ten


    def getPredictDict(self):
        predictData = self.formatDatas(self.columns)

        self.gatherDatas(predictData)


        predictDict = self.toDict(predictData,self.columns)

        predictDict = self.popBattery(predictDict)

        return predictDict
    def getCons(self):
        return self.cons

        #retounr la consommation du systeme : si il charge c'est la prediction sinon la valeur reelle
    def getConsomation(self):
        if(self.status == "Discharging"):
            dictData = self.toDict(self.rawdatas,self.columns)
            return dictData['BAT_POWER'][len(dictData['BAT_POWER'])-1]

        dictP = self.getPredictDict()
        return self.ten.MakePrediction(dictP)[0]

    def initAppGetter(self,pid):
        self.AppGetter = AppGetter(pid,self.cons)

    #retourne une liste de liste de donnees, liste[0] donne la liste des donnes de la premiere application
    def getAppDatas(self):
        return self.AppGetter.getAppDatas()

    def getAppPids(self):
        return self.AppGetter.getAppPids()


    #retourne la liste des sondes communes entre les sondes systemes et les sondes application
    def getCommunColAppSys(self):
        sysColumns=self.columns
        appColumns=self.AppGetter.getColumns()

        comColumns = []
        for appCol in appColumns:
            if appCol in sysColumns:
                comColumns.append(appCol)
        return comColumns

    #retourne les donnes des applications sous forme de dictionnaire : une liste de valeur / cle,la cle etant le nom de la sonde.

    def getAppsDict(self):
        appDataFormated = self.formatDatas(self.AppGetter.getColumns())
        self.gatherAppDatas(appDataFormated)
        dictAppData = self.toDict(appDataFormated,self.AppGetter.getColumns())
        return dictAppData

    #retourne une liste de dictionnaire.Chaque dictionnaire est le dictionnaire de prediction systeme auquel les valeurs des sondes des applications sont soustraites
    #exemple : dict_systeme = ["CPU_USAGE":10,"LUMINOSITY":1700], dictApp = ["CPU_USAGE":1] => dictPredictApp = ["CPU_USAGE":9,"LUMINOSITY":1700]
    #chaque dictPredictApp est ensuite ajoutee a la liste qui sera alors retournee
    def getAppsPredictDicts(self,sysPredictDict):
        listeDicts = []
        appsDict = self.getAppsDict()
        for i in range(self.AppGetter.getNbApps()):
            dictTemp = {}
            for key, value in sysPredictDict.items():
                dictTemp[key] = list(value)
            for col in self.getCommunColAppSys():
                dictTemp[col][0] -=appsDict[col][i]
            listeDicts.append(dictTemp)
        return listeDicts

    #retourne un dictionnaire.Chaque application est representee par un dictionnaire ["pid"=>consommation]
    #la consommation est calculee avec la formule suivante : consommation(systeme) - consommation(systeme-application)
    def getAppsConso(self):
        dictConsoApps = dict()
        if self.AppGetter.getNbApps() >0:
            sysPredictDict = self.getPredictDict()
            consoSysteme = self.ten.MakePrediction(sysPredictDict)[0]
            appsPid = self.AppGetter.getAppPids()
            appsPredictDicts = self.getAppsPredictDicts(sysPredictDict)
            dictConsoApps = dict()
            for i in range(len(appsPredictDicts)):
                appDict = appsPredictDicts[i]

                consoSysMoinsApp = self.ten.MakePrediction(appDict)[0]

                consoApp = consoSysteme - consoSysMoinsApp
                dictConsoApps[appsPid[i]] = consoApp
        else:
            dictConsoApps["pas d'application consommant de cpu lors du lancement de appliconso"]=0
        return dictConsoApps

    def CostlyFunction(self,z):
        result = 0
        for k in range(1,100):
            result += z ** (1 / k**1.5)
            print(result)
        return result

    def CPUChargeGenerator_start(self,nb):
        pool = mp.Pool(processes=8)
        result=pool.apply_async(self.CostlyFunction,args=(100))

    def CPUChargeGenerator_stop(self):
        for i in range(len(self.CPUChargeGenerators)):
            self.CPUChargeGenerators[i].kill()
