from Constantes import Constantes

def getData():
        path = Constantes.BACKLIGHT_PATH
        fileBrightness = open(path+"brightness")
        brightness = fileBrightness.read()
        brightness=brightness.rstrip()
       
        return int(brightness)
