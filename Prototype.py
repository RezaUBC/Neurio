#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:21:16 2017

@author: zangeneh
"""

""" 
*Assuming that this is the ML prototype created by the Data Scientist
*It calculates the peak time of the energy consumption within a day \
using the  sensor data in '.hdf' format

"""
import IO_module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from datetime import datetime, timedelta
import pytz
import re

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cross_validation import train_test_split

fig_size = [10,5] 
plt.rcParams["figure.figsize"] = fig_size


### Start of Debugging
if __debug__:
    directory="/Users/larathompson/Desktop/tmp/"
    sensor="0x0000C47F510198BD"
    file_format='.hdf'
    files = IO_module.readFile(directory, sensor, file_format)
    
    print(files[0])
    
    df = pd.read_hdf(files[0])
    
    df.columns
    
    plt.plot(df.consumption_real)
    plt.plot(df.generation)
    
    tz = pytz.timezone('America/Los_Angeles')
    
    int(re.findall(r"[xA-Z0-9]+", files[0].split('_')[-1])[0])
    
    dt = datetime.fromtimestamp(1501570800, tz=tz)
    
    (dt.astimezone(pytz.utc) - pytz.utc.localize(datetime(1970,1,1)))/timedelta(0,1)
    
    dt0 = datetime.combine(dt.date(), datetime.strptime('14:00', '%H:%M').time())
    dt1 = datetime.combine(dt.date(), datetime.strptime('22:00', '%H:%M').time())
    
    ts = [(tz.localize(dt0).astimezone(pytz.utc)-pytz.utc.localize(datetime(1970, 1, 1)))/timedelta(0, 1), 
     (tz.localize(dt1).astimezone(pytz.utc)-pytz.utc.localize(datetime(1970, 1, 1)))/timedelta(0, 1)]
    i_peak = [np.argmin(np.abs(df.sample_times - ts[0])), np.argmin(np.abs(df.sample_times - ts[1]))]
    print(i_peak)
    
    np.nansum(df.consumption_real[i_peak[0]:i_peak[1]])

### End of Debugging
class Prototype(object):
    def __init__(self,trainingFiles=None,model=None):
        self.files=trainingFiles
        self.p_peak, self.p_morn = self._timetwik()
        self.model = model
        
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self,model):
        if model is not None:
            self._model = model
        else:
            self._model = self.fit_transform(True)
        
        
    def _timetwik(self):
        p_peak = np.zeros(len(self.files))
        p_morn = np.zeros(len(self.files))
        for i, file in enumerate(self.files):
            df = pd.read_hdf(file)
            t0 = int(re.findall(r"[xA-Z0-9]+", file.split('_')[-1])[0])
            dt = datetime.fromtimestamp(t0, tz=tz)
            dt0 = datetime.combine(dt.date(), datetime.strptime('14:00', '%H:%M').time())
            dt1 = datetime.combine(dt.date(), datetime.strptime('22:00', '%H:%M').time())
            ts = [(tz.localize(dt0).astimezone(pytz.utc)-pytz.utc.localize(datetime(1970, 1, 1)))/timedelta(0, 1), 
                  (tz.localize(dt1).astimezone(pytz.utc)-pytz.utc.localize(datetime(1970, 1, 1)))/timedelta(0, 1)]
            i_peak = [np.argmin(np.abs(df.sample_times - ts[0])), np.argmin(np.abs(df.sample_times - ts[1]))]
            i_0 = np.argmin(np.abs(df.sample_times - t0))
            p_peak[i] = np.nansum(df.consumption_real[i_peak[0]:i_peak[1]])
            p_morn[i] = np.nansum(df.consumption_real[i_0:i_peak[0]])
            
        return p_peak, p_morn
    def visualizeTimeTwik(self):
        plt.plot(self.p_peak)
        plt.plot(self.p_morn)
        
        plt.plot(self.p_morn, self.p_peak, '*')
    
    def fit_transform(self,withEvaluation=True):
        x_fit, x_eval, y_fit, y_eval= train_test_split(self.p_morn[:,np.newaxis], self.p_peak, test_size=0.3, random_state=32)
        regr = linear_model.LinearRegression()
        regr.fit(x_fit, y_fit)
    
        if withEvaluation:
            y_pred = regr.predict(x_eval)
            print('Coefficients: {}'.format(regr.coef_))
            print('rms: {}'.format(np.sqrt(mean_squared_error(y_eval, y_pred))))
            print('variance score: {}'.format(r2_score(y_eval, y_pred)))
            model_report = {"Coefficients":regr.coef_, "rms":np.sqrt(mean_squared_error(y_eval, y_pred)),
                            "variance score":r2_score(y_eval, y_pred)}
            IO_module.writeJSON('report.json',model_report)
            plt.plot(x_fit, y_fit, '*')
            plt.plot(x_eval, y_pred, 'o')
        
        return regr
    
    def __call__(self,X_Test: numpy.ndarray)->numpy.ndarray:
        Y_Test = self.model.predict(X_Test)
        IO_module.writeFile('prediction.txt',Y_Test)
        

