

class Constantes:
    COLUMNS = []
    FEATURES=[]
    LABEL = "BAT_POWER"
    
    BAT_PATH = "/sys/class/power_supply/BAT1"
    BACKLIGHT_PATH = "/sys/class/backlight/intel_backlight/"
    
    MIN_CPU_USAGE = 0
    LOG = True
    LOG_FILE_NAME = "log.txt"
    PORT = 3035

    def __init__(self,columns):
        self.COLUMNS = columns
        tempCol = list(columns)
        tempCol.remove("BAT_POWER")
        self.FEATURES = tempCol
        self.LABEL = "BAT_POWER"


    def get_label(self):
        return self.LABEL

    def get_columns(self):
        return self.COLUMNS

    def get_features(self):
        return self.FEATURES

    def get_min_cpu_usage(self):
        return self.MIN_CPU_USAGE

    def is_log_enabled(self):
        return self.LOG

    def get_log_file_name(self):
        return self.LOG_FILE_NAME

