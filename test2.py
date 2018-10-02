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
from glob import glob
import re

folders = glob('D:/synchrony-data/AllConnLogNormal/*/')
s = re.compile('/')
conns = []
#avgCL = []
avgSV = []
avgST = []
for folder in folders:
#    plt.figure()
    conns.append(float(s.split(folder)[-2]))
#    plt.subplot(3,1,1)
    b2bSTimes,b2bST,b2bSV=b2bSync(folder+'/',3)
    b2bCLX, b2bCLY = b2bCL(folder)
#    avgCL.append(np.mean(b2bCLY))
    avgSV.append(np.mean(b2bSV))
    avgST.append(np.mean(b2bST))
    for rn in range(b2bCLY.shape[0]):
        for cn in range(b2bCLY.shape[1]):
            if b2bCLY[rn,cn].max() > 450:
                b2bCLY[rn,cn] = np.zeros(0)
                b2bCLX[rn,cn] = np.zeros(0)
#    for i in range(b2bCLX.shape[0]):
#        for j in range(b2bCLX.shape[1]):
#            plt.plot(b2bCLX[i,j],b2bCLY[i,j])
#    plt.subplot(3,1,2)
#    plt.plot(b2bSTimes,b2bST)
    #plt.plot(b2bSTimes,signal.medfilt(b2bST,kernel_size=5))
#    plt.subplot(3,1,3)
#    plt.plot(b2bSTimes,b2bSV)
#plt.plot(conns,avgCL)
plt.plot(conns,avgSV)
plt.plot(conns,avgST)