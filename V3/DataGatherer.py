import platform
import os
import importlib as il
class DataGatherer:


    def __init__(self):
        self.tabFonctions = []
        self.tabColumns = []
        if platform.system() == 'Linux':
            fileNames = os.listdir('LinuxProbes')
            self.osDir='LinuxProbes'
        elif platform.system() == 'Windows':
            fileNames = os.listdir('WindowsProbes')
            self.osDir = 'WindowsProbes'
        else:
            print('unsuported os')

        tabFile =[]
        for fileN in fileNames:
            if fileN[0:5] == 'probe':
                moduleName = fileN.split('.')[0]
                columnName = moduleName.split('probe')[1]
                self.tabColumns.append(columnName)
                imported =il.import_module(self.osDir+'.'+moduleName)
                self.tabFonctions.append(imported.getData)
        """
        for fn in self.tabFonctions:
            print(fn())
        """

    def getDatas(self):
        tab=[]
        for fn in self.tabFonctions:
            tab.append(fn())
        return tab

    def getColumns(self):
        return self.tabColumns
