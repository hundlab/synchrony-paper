#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:26:02 2017

@author: dgratz
"""
from readFile import readFile
from glob import glob
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def calcPartialSums(array):
    s = 0
    sums = np.zeros(array.shape)
    for i in range(len(array)):
        if not np.isnan(array[i]):    
            s += array[i]
        sums[i] = s
    return sums

def b2bCL(folder):
    dtFiles = glob(folder+'/*_dt0.tsv')
    s = re.compile('_')
    filePos = []
    for file in dtFiles:
        sp = s.split(file)
        filePos.append(tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),sp))))
    ncols = max(map(lambda x: x[1],filePos))+1
    nrows = max(map(lambda x: x[0],filePos))+1
    data = np.zeros((nrows,ncols),dtype='object')
    dataX = np.zeros(data.shape,dtype='object')
    dataY = np.zeros(data.shape,dtype='object')
    for (file,pos) in zip(dtFiles,filePos):
        data[pos] = readFile(file)['cell'+str(pos[0])+'_'+str(pos[1])+'/vOld/cl']
    for row in range(nrows):
        for col in range(ncols):
            pos = (row,col)
            temp = data[pos]
            i=0
            for i in range(len(temp)):
                if np.isnan(temp[i]):
                    temp[i] = np.nanmean(temp)
                temp = signal.medfilt(temp)
                i += 1
#            if temp.max() > 600:
#                continue
            dataY[pos] = np.array(temp)
            dataX[pos] = np.array(calcPartialSums(temp))
#            linestyle = '-' if temp.max() < 600 else 'None'
#            plt.plot(dataY[pos],dataX[pos])
#    plt.show()
    return dataX,dataY