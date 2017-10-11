#!/user/bin/env python
from math import log10, sqrt, copysign, log
from time import strftime, time
from optparse import OptionParser
import os
import re

# Error Messages
SUCCESS = 0
CONVERGENCE_FAILED = 1
VAR_CHANGED = 2
ACCURACY_WORSE = 3
BIASED_WORSE = 4
VARIANCE_WORSE = 5

def getFileName(FileName):
    pass

def getCommandName():
    return command

def runCase(command):
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return stdout, stderr

def compareOutout(stdout,pathToRefData):
    #getting the solution from this run
    #comparing it with the existing solution within the ref_data directory
    #if they did not match, return the error code
    pass

def compareAccuracy(stdout,pathToRefData):
    #getting accuracy of this run
    #comparing it with the accuracy of the existing solution
    #if weren't matched, return the error code
    pass
