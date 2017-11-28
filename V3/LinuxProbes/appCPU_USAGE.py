from __future__ import division
import psutil

def getData(pid):
    p = psutil.Process(pid)
    cpu = p.cpu_percent(interval=0.1)
    nbCore = psutil.cpu_count()
    cpu_usage = cpu/nbCore
    return cpu_usage
