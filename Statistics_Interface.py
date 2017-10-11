#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:26:21 2017

@author: zangeneh
"""

import numpy as np
import math
from Prototype import Prototype
import IO_module

'''
Module for misc. statistical methods 
for time series data
'''

# makes predictions
# for xTest
# Returns a 1-d vector representing predictions
class statisticsInterface(object):
    def __init__(self,datapath, file_format, doTraining=False):
        files = IO_module.readFile(datapath, file_format)  
        metadata = IO_module.readJSON('data.json')
        if doTraining:
            self.model = Prototype(files,None)
        else:
            self.model = Prototype(None,metadata['model'])
        self.dataloader = IO_module.dataLoader(datapath, file_format)
    
    def predict(self,bach_size=100):
        predictions = np.array([])
        for data in dataloader(bach_size=100):
            bach_prediction = self.model(data)
            predictions = np.concatenate((predictions,bach_prediction), axis=0)
            
        return predictions
        	

    # Computes the Mean Squared Error for predicted values against
    # actual values
    def _meanSquareError(self,actual,pred):
        	if (not len(actual) == len(pred) or len(actual) == 0):
        		return -1.0
        	total = 0.0
        	for x in range(len(actual)):
        		total += math.pow(actual[x]-pred[x],2)
        	return total/len(actual)

    # Computes Normalized Root Mean Square Error (NRMSE) for
    # predicted values against actual values
    def _normRmse(self,actual,pred):
        	if (not len(actual) == len(pred) or len(actual) == 0):
        		return -1.0
        	sumSquares = 0.0
        	maxY = actual[0]
        	minY = actual[0]
        	for x in range(len(actual)):
        		sumSquares += math.pow(pred[x]-actual[x],2.0)
        		maxY = max(maxY,actual[x])
        		minY = min(minY,actual[x])
        	return math.sqrt(sumSquares/len(actual))/(maxY-minY)
        
    def reportStatistics(self,actual,pred):
        dictRep = {}
        rmse = self._normRmse(actual,pred)
        mse = self._meanSquareError(actual,pred)
        #do something with these statistics
        pass

    # Estimates missing data
    def estimateMissing(self,data,targ):
        for x in range(len(data)):
            for y in range(len(data[x])):
                if (data[x][y] == targ):
                    if (y > 0 and y < len(data[x])-1):
                        data[x][y] = (data[x][y-1]+data[x][y+1])/2.0
                    else:
                        data[x][y] = np.mean(data[x])
                    

if __name__=="__main__":
    directory="/Users/larathompson/Desktop/tmp/"
    sensor="0x0000C47F510198BD"
    file_format='.hdf'
    
    statistics_interface = statisticsInterface(directory+sensor,file_format,False)
    predictions = statistics_interface.predict()
    
    ### doing some other useful stuff with predictions
    