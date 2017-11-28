import tensorflow as tf
import pandas as pd
import functools
import numpy as np
from Constantes import Constantes
import os

class TensorFlowObject:


    def __init__(self,cons):
        self.sCOLUMNS = cons.get_columns();
        self.sFEATURES = cons.get_features();
        self.sLABEL = cons.get_label();
        self.straining_set = None
        self.sCons = None
        model_dir="TensorFlowModel"
        for feat in self.sFEATURES:
            model_dir+=feat[0]

        if os.path.isdir(model_dir) == False:
            os.mkdir(model_dir)

        self.sfeature_cols = [tf.contrib.layers.real_valued_column(k) for k in self.sFEATURES]
        self.sregressor = tf.contrib.learn.DNNRegressor(feature_columns = self.sfeature_cols,hidden_units=[10,10],enable_centered_bias=True,model_dir = model_dir)
        tf.logging.set_verbosity(tf.logging.ERROR)

    def input_fn(self,data_set):
        feature_cols = {k:tf.constant(data_set[k].values) for k in self.sFEATURES}
        labels = tf.constant(data_set[self.sLABEL].values)
        return feature_cols,labels

    def predict_input_fn(self,data_set):
        feature_cols = {k:tf.constant(data_set[k].values) for k in self.sFEATURES}
        return feature_cols

    def StartTrain(self,data):
        try:
            self.straining_set = data
            self.sregressor.fit(input_fn=lambda:self.input_fn(self.straining_set),steps=5000)
        except Exception as e:
            print(e)

    def MakePrediction(self,data):
        try:
            data_set = pd.DataFrame(data,columns=self.sCOLUMNS)
            return self.sregressor.predict(input_fn=lambda: self.predict_input_fn(data_set))
        except Exception as e:
            print("Le modele n'a pas ete entraine");
            a = []
            a.append(0)
            return a


    def checkModel(self,data):
        dict_dataFull=data
        dict_predict = self.popBattery(dict_dataFull)
        battery = dict_dataFull["BAT_POWER"]
        battery_predict = self.MakePrediction(dict_predict)
        for i in range(len(battery)):
            if(abs(battery[i]-battery_predict[i])>1.5):
                return False
        return True


    def popBattery(self,dictionnaire):
        dictPredict2={}
        for i in self.sFEATURES:
            dictPredict2[i] = dictionnaire[i]
        return dictPredict2

    def toDict(self,datas):

        dictData={}
        for i in range(len(datas)):
            dictData[self.sCOLUMNS[i]] = datas[i]
        return dictData
