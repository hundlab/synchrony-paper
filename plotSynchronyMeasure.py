#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 16:12:34 2017

@author: dgratz
"""
import re
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from readFile import readFile
from calcSync import calcSyncVarLen,calcTimeSync


def b2bSync(folder,nextBeatDist=3):
    dtFiles = glob(folder+'/*_dt0.tsv')
    s = re.compile('_')
    filePos = []
    for file in dtFiles:
        sp = s.split(file)
        filePos.append(tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),sp))))
    ncols = max(map(lambda x: x[1],filePos))+1
    nrows = max(map(lambda x: x[0],filePos))+1
    dataPK = np.zeros((nrows,ncols),dtype='object')
    dataMT = np.zeros((nrows,ncols),dtype='object')
    for (file,pos) in zip(dtFiles,filePos):
        dataPK[pos] = readFile(file)['cell'+str(pos[0])+'_'+str(pos[1])+'/vOld/peak']
        dataMT[pos] = readFile(file)['cell'+str(pos[0])+'_'+str(pos[1])+'/vOld/maxt']
    T,syncT,syncV = calcTimeSync(dataPK, dataMT,nextBeatDist)
#    plt.plot(syncT)
#    plt.plot(syncV)
    plt.show()
    return T,syncT,syncV

s = re.compile('/')
allSyncT = []
allSyncV = []
conns = []
for i,folder in enumerate(glob('D:/synchrony-data/AllConnLogNormal/*/')):
#    plt.figure(i)
#    plt.title(s.split(folder)[-2])
    times,syncT,syncV=b2bSync(folder)
    allSyncT.append(np.mean(syncT))
    allSyncV.append(np.mean(syncV))
    conns.append(s.split(folder)[-2])
    plt.figure()
    plt.title(str(conns[-1]))
    plt.plot(times,syncT)
    plt.plot(times,np.mean(syncT)*np.ones(len(times)))
#for i in range(len(allSyncT)):
#    allSyncT[i] = (allSyncT[i]-allSyncT[-1])
#    allSyncV[i] = (allSyncV[i]-allSyncV[-1])
#for i in reversed(list(range(len(allSyncT)))):
#    allSyncT[i] = allSyncT[i]/allSyncT[0]
#    allSyncV[i] = allSyncV[i]/allSyncV[0]
#    plt.annotate(conns[i], xy=(allSyncT[i],allSyncV[i]), textcoords='data')
plt.figure()
plt.plot(conns,allSyncT)
plt.plot(conns,allSyncV)
