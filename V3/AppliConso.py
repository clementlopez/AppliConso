import sys,time,traceback
from DataTrainer import DataTrainer
import numpy
from Constantes import Constantes

from http.server import BaseHTTPRequestHandler,HTTPServer
import json


PORT_NUMBER = 8080
PID = 3395
dataTrainer = None
ten = None
cons = None






class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,numpy.integer):
            return int(o)
        elif isinstance(o,numpy.float32):
            return float(o)
        elif isinstance(o,numpy.ndarray):
            return o.tolist()
        else:
            return super(MyEncoder,self).default(o)

class myHandlerSys(BaseHTTPRequestHandler):
    # Handler for the GET requests

    init = False
    dataTrainer = None

    def do_GET(self):

        self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


        # Send the json datas
        try:
            global cons
            global ten
            global dataTrainer
            conso = dataTrainer.getConsomation()
            dictConsoApps = dataTrainer.getAppsConso()
            dictConsoApps['systeme'] = conso
            self.wfile.write(bytes(json.dumps(dictConsoApps,cls=MyEncoder),'utf-8'))
        except Exception as e:
            dataTrainer.kill = True
            print(e)

        return

class myHandlerApp(BaseHTTPRequestHandler):
    # Handler for the GET requests




    init = False
    dataTrainer = None

    def do_GET(self):

        if myHandlerApp.init == False:
            global cons
            global ten
            global dataTrainer

        self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


        # Send the json datas
        try:

            conso = dataTrainer.getConsomation()
            dictConsoApps = dataTrainer.getAppsConso()
            dictConsoApps['systeme'] = conso
            self.wfile.write(bytes(json.dumps(dictConsoApps,cls=MyEncoder),'utf-8'))
        except Exception:
            dataTrainer.kill = True
            traceback.print_exc(file=sys.stdout)

        return




if len(sys.argv) > 3:
    print("usage : python AppliConso.py [-w] [Application to monitor]")
    sys.exit()


if len(sys.argv) == 2 and sys.argv[1] == "-w":
    PORT_NUMBER = Constantes.PORT
    dataTrainer = DataTrainer()
    ten = dataTrainer.getTensorFlow()
    cons = dataTrainer.getCons()
    dataTrainer.initAppGetter(-1)
    dataTrainer.start()

    server = None
    try:
        server = HTTPServer(('',PORT_NUMBER),myHandlerSys)
        print("Server listening on port: " + str(PORT_NUMBER))
        server.serve_forever()
    except Exception as e:
        if server != None:
            server.socket.close()
        print(e)

elif len(sys.argv) == 3 and sys.argv[2] == "-w":
    sys.stdout.flush()
    server = None
    PID = sys.argv[1]
    PORT_NUMBER = Constantes.PORT
    dataTrainer = DataTrainer()
    ten = dataTrainer.getTensorFlow()
    cons = dataTrainer.getCons()
    dataTrainer.initAppGetter(PID)
    dataTrainer.start()
    try:
        server = HTTPServer(('', PORT_NUMBER), myHandlerApp)
        print("Server listening on port: "+str(PORT_NUMBER))
        server.serve_forever()
    except Exception as e:
        if server != None:
            server.socket.close()
        print(e)

elif len(sys.argv) == 2:
    print("lancement de l'interface console\nsurveillance de:",sys.argv[1])
    dataTrainer = DataTrainer()
    ten = dataTrainer.getTensorFlow()
    cons = dataTrainer.getCons()
    dataTrainer.start()
    dataTrainer.initAppGetter(int(sys.argv[1]))
    try:
        while(True):
            conso = dataTrainer.getConsomation()
            print("consommation: ", conso)
            print("")
            print("consommation de l'application:")
            dictConsoApps = dataTrainer.getAppsConso()
            for key,value in dictConsoApps.items():
                print(key,": ",value)

            print("\n\n")


            time.sleep(2)
        dataTrainer.kill = True
    except Exception as e:
        print(e)
        dataTrainer.kill = True



else:
    print("lancement de l'interface console")
    dataTrainer = DataTrainer()
    ten = dataTrainer.getTensorFlow()
    cons = dataTrainer.getCons()
    dataTrainer.start()

    print("\nanalyse des application.")
    print("cela peut prendre plusieurs minutes mais ne consomme pas beaucoup")
    print("le programme continue a apprendre en arriere plan,n'hesitez debrancher votre ordinateur pour recolter des donnees\n")
    dataTrainer.initAppGetter(-1)
    print("started")
    try:
        while(True):
            conso = dataTrainer.getConsomation()
            print("consommation: ", conso)
            print("\n\n")
            print("consommation des applications:")
            dictConsoApps = dataTrainer.getAppsConso()
            for key,value in dictConsoApps.items():
                print(key,": ",value)

            print("\n\n")


            time.sleep(2)
        dataTrainer.kill = True
    except Exception as e:
        print(e)
        dataTrainer.kill = True
