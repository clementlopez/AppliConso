import psutil

def getData():
    return psutil.cpu_percent(interval=0.1)
