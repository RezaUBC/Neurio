#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:31:17 2017

@author: zangeneh
"""
import datetime
import pandas
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from datetime import datetime, timedelta
import pytz
import re
import json
'''
Module for time series visualization and I&O
'''

# Plots the (x,y) data using matplotlib with the given labels
def yearlyPlot(ySeries,year,month,day,plotName ="Plot",yAxisName="yData"):

	date = datetime.date(year,month,day)
	dateList = []
	for x in range(len(ySeries)):
		dateList.append(date+datetime.timedelta(days=x))

	plt.plot_date(x=dateList,y=ySeries,fmt="r-")
	plt.title(plotName)
	plt.ylabel(yAxisName)
	plt.xlabel("Date")
	plt.grid(True)
	plt.show()
    

def _isPathHealthy(pathname:str):
    if not (isinstance(pathname,str)):
        return False
    if not os.path.isdir(pathname):
        return False
    return True
    
def readFile(pathname:str,file_format):
    return None if not _isPathHealthy(pathname)
    files = sorted([pathname + "/" + file for file in 
                    listdir(pathname) if file.endswith(file_format)])
    return files

def writeFile(pathname:str, data: numpy.ndarray):
    with open(pathname,'w') as f:
        for i in data.size:
            f.write('{}'.format(data[i]))

def writeJSON(pathname:str,data:dict,encoding='utf8'):
    with open(pathname,'w') as f:
        json.dump(data, f,
                  indent=4, sort_keys=True,
                  separators=(',', ': '), ensure_ascii=False)

def readJSON(pathname:str)->dict:
    return None if not _isPathHealthy(pathname)
    with open(pathname) as f:
        data_loaded = json.load(f)
    return data_loaded


class dataLoader(object):
    def __init__(self,pathToFile:str,file_format='.hdf'):
        self.files = readFile(pathToFile,file_format)
        self.data = None
        self.features = None
        
    
    def _loadData(self,batch_size, make_random):
        pass
    
    def __call__(self, batch_size=100, make_random=False, cpu_monitoring=False):
        if cpu_monitoring:
            self._cpuStats()
        sz = 0
        while sz<len(self.files):
            yield _loadData(batch_size, make_random)
            sz += 1
        
        
    def _cpuStats(self):
        print(sys.version)
        print(psutil.cpu_percent())
        print(psutil.virtual_memory())  # physical memory usage
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
        print('memory GB:', memoryUse)
