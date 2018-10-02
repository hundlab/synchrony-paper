#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:58:02 2017

@author: dgratz
"""
import numpy as np
from glob import glob
from readFile import readFile
import re
from ParameterSensitivity import ParamSensetivity
import matplotlib.pyplot as plt

pvars = list(readFile('D:/synchrony-data/2SAN1RandLogNormal/0/cell_0_0_dss0_pvars.tsv').keys())
datadir = 'D:/synchrony-data/600Sims1CellRand/'

filesPvars = glob(datadir+'*/*_pvars.tsv')
numData = len(filesPvars)
pvarsVals = np.zeros((numData,len(pvars)))
s = re.compile('/')
u = re.compile('_')

for file in filesPvars:
    file = file.replace('\\','/')
    temp = readFile(file)
    fnames = s.split(file)
    num = int(fnames[-2])
    for i,pvar in enumerate(pvars):
        pvarsVals[num,i] = temp[pvar]
        
props = ['vOld/peak','vOld/cl','vOld/min','caI/peak','caI/min',
         'vOld/ddr']
filesProps = glob(datadir+'*/dss0.tsv')
propsVals = np.zeros((numData,len(props)))
for file in filesProps:
    file = file.replace('\\','/')
    temp = readFile(file)
    fnames = s.split(file)
    num = int(fnames[-2])
    for i,prop in enumerate(props):
        propsVals[num,i] = temp[prop]

filesProps = glob(datadir+'*/dt0.tsv')
bad = set()
for file in filesProps:
    file = file.replace('\\','/')
    temp = readFile(file)
    fnames = s.split(file)
    num = int(fnames[-2])
    cls = temp['vOld/cl']
    if np.std(cls[-10:-1]) > 20:    
        bad.add(num)
bad = list(bad)
pvarsVals = np.delete(pvarsVals,bad,axis=0)
propsVals = np.delete(propsVals,bad,axis=0)

coefs = ParamSensetivity(pvarsVals, propsVals)
for i in range(coefs.shape[1]):
    plt.figure()
    plt.bar(range(len(pvars)),coefs[:,i],tick_label=pvars)
    plt.title(props[i])