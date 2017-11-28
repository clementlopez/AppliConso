import psutil
from AppGatherer import AppGatherer


class AppGetter:


    def __init__(self, pid,constante):
        self.apps = []
        self.constante = constante
        if pid == -1:
            pids = psutil.pids()
            for pid in pids:
                try:
                    app = AppGatherer(pid,self.constante)
                    if(app.getCPU_USAGE() >self.constante.get_min_cpu_usage() ):
                        self.apps.append(app)
                except:
                    pass

        else:
            self.apps.append(AppGatherer(pid,self.constante))

    def getAppDatas(self):
        data = []
        for app in self.apps:
            data.append(app.getDatas())
        return data

    def getAppPids(self):
        pids=[]
        for app in self.apps:
            pids.append(app.getPid())
        return pids

    def getColumns(self):
        return self.apps[0].getColumns()

    def getNbApps(self):
        return len(self.apps)
