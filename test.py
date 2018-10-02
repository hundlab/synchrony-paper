#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 13:48:17 2017

@author: dgratz
"""

from plotBeat2beatCLGrid import b2bCL
from plotSynchronyMeasure import b2bSync
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

#folder = 'D:/synchrony-data/AllConnLogNormal/0.38/'
#folder = 'D:/synchrony-data/ManyParamsLogNormal/data0.0038_20/'
folder = 'D:/synchrony-data/AllConnLogNormal/0.0/'
plt.figure(1)
plt.subplot(3,1,1)
b2bSTimes,b2bST,b2bSV=b2bSync(folder+'/',3)
b2bCLX, b2bCLY = b2bCL(folder)
for rn in range(b2bCLY.shape[0]):
    for cn in range(b2bCLY.shape[1]):
        if b2bCLY[rn,cn].max() > 450:
            b2bCLY[rn,cn] = np.zeros(0)
            b2bCLX[rn,cn] = np.zeros(0)
for i in range(b2bCLX.shape[0]):
    for j in range(b2bCLX.shape[1]):
        plt.plot(b2bCLX[i,j],b2bCLY[i,j])
plt.subplot(3,1,2)
plt.plot(b2bSTimes,b2bST)
#plt.plot(b2bSTimes,signal.medfilt(b2bST,kernel_size=5))
plt.subplot(3,1,3)
plt.plot(b2bSTimes,b2bSV)
'''
from writeGridToFile import writeGrid
writeGrid(b2bCLX,b2bCLY,'AllConnLogNormal_00_b2bCL.csv')

#with open('AllConnLogNormal_38_b2bSync.csv','w') as fl:
#with open('ManyParamLogNormal_0038_20_b2bSync.csv','w') as fl:
with open('AllConnLogNormal_00_b2bSync.csv','w') as fl:
    for time,T,V in zip(b2bSTimes,b2bST,b2bSV):
        print(time,T,V,sep=',',file=fl)
'''