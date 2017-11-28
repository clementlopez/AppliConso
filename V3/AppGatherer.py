import platform
import os
import importlib as il


class AppGatherer:


    def __init__(self, pid,constante):
        self.tabColumns=[]
        self.tabFonctions=[]
        self.constante = constante
        self.pid = int(pid)
        if platform.system() == 'Linux':
            fileNames = os.listdir('LinuxProbes')
            self.osDir = 'LinuxProbes'
        elif platform.system() == 'Windows':
            fileNames = os.listdir('WindowsProbes')
            self.osDir = 'WindowsProbes'
        else:
            print('unsuported os')

        i=0
        for fileN in fileNames:
            if fileN[0:3] == 'app':
                moduleName = fileN.split('.')[0]
                columnName = moduleName.split('app')[1]


                self.tabColumns.append(columnName)

                imported = il.import_module(self.osDir+'.'+moduleName,self.osDir)
                self.tabFonctions.append(imported.getData)
                if columnName == 'CPU_USAGE':
                    self.cpu_usage_pos = i
                i+=1
        """
        for fn in self.tabFonctions:
            print(fn())
        """

    def getDatas(self):
        tab = []
        for fn in self.tabFonctions:
            tab.append(fn(self.pid))
        return tab

    def getColumns(self):
        return self.tabColumns

    def getPid(self):
        return self.pid

    def getCPU_USAGE(self):
        if self.cpu_usage_pos >= 0:
            return self.tabFonctions[self.cpu_usage_pos](self.pid)
        else:
            return -1
