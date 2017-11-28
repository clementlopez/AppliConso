import threading
import numpy as np


class CPUChargeGenerator(threading.Thread):

    def __init__(self):
        self.kill = False
        self.a = [[150552, 2051, 3516], [1479, 21156, 646846], [15315, 4684, 35352]]
        self.b = [[5186, 351853, 53354], [25616, 666465, 6544], [351354, 351453, 643454]]
        threading.Thread.__init__(self)

    def run(self):
        while self.kill is False:
            self.a = np.matmul(np.matmul(self.a, self.b),np.matmul(self.b,self.a))
            self.b = np.matmul(np.matmul(self.b, self.a),np.matmul(self.b,self.a))

    def kill(self):
        self.kill = True

    def heavy_function():
            a = [[150552, 2051, 3516], [1479, 21156, 646846], [15315, 4684, 35352]]
            b = [[5186, 351853, 53354], [25616, 666465, 6544], [351354, 351453, 643454]]
            a = np.matmul(np.matmul(self.a, self.b),np.matmul(self.b,self.a))
            b = np.matmul(np.matmul(self.b, self.a),np.matmul(self.b,self.a))
