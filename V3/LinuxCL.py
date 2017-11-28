import socket
import threading
import time
import sys

class  ChargeListener(threading.Thread):


    def __init__(self):
        self.status= "Unknown"
        self.kill = False
        threading.Thread.__init__(self)


    def run(self):
        path = "/sys/class/power_supply/BAT1"

        i=0
        while(not self.kill):
            fileStatus = open(path+"/status")
            self.status = fileStatus.read().strip();
            time.sleep(0.5)
            fileStatus.close()
            i+=1

    def getStatus(self):
        return self.status
