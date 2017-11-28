from Constantes import Constantes

def getData():
    path = Constantes.BAT_PATH
    fileCurrent = open(path+"/current_now")
    current = float(fileCurrent.read())

    fileVoltage = open(path+"/voltage_now")
    voltage = float(fileVoltage.read())

    power = voltage/1000000*current/1000000
    return power
