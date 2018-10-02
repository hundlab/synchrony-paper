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
from calcSync import calcTimeSync, calcSyncVarLen
import xml.etree.ElementTree as ET

pvars = list(readFile('D:/synchrony-data/2SAN1RandLogNormal/0/cell_0_0_dss0_pvars.tsv').keys())
pvars.append('cond')
#datadir = 'D:/synchrony-data/2SAN1RandLogNormal/'
#datadir = 'D:/synchrony-data/2SAN1RandLogNormalT2_038/'
#datadir = 'D:/synchrony-data/2SAN1RandLogNormalT4_0038/'
datadir = 'D:/synchrony-data/2SAN1RandLogNormalManyCond/'
filesPvars = glob(datadir+'*/*_pvars.tsv')
numData = len(filesPvars)//2
pvarsVals = np.zeros((2,numData,len(pvars)))
s = re.compile('/')
u = re.compile('_')

def getCond(file):
    simvars = s.split(file)
    simvars[-1] = 'simvars.xml'
    simvars = '/'.join(simvars)
    tree = ET.parse(simvars)
    root = tree.getroot()
    cond = root[1][0][0][1][1].text
    return float(cond)

for file in filesPvars:
    file = file.replace('\\','/')
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    num = int(fnames[-2])
    for i,pvar in enumerate(pvars):
        if pvar == 'cond':
            pvarsVals[col,num,i] = getCond(file)
        else:
            pvarsVals[col,num,i] = temp[pvar]
        
props = ['vOld/peak','vOld/cl','vOld/min','vOld/maxt','caI/peak','caI/min','vOld/ddr']
filesProps = glob(datadir+'*/*dss0.tsv')
propsVals = np.zeros((2,numData,len(props)))
for file in filesProps:
    file = file.replace('\\','/')
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    num = int(fnames[-2])
    for i,prop in enumerate(props):
        propsVals[col,num,i] = temp['cell'+str(row)+'_'+str(col)+'/'+prop]
'''
coefs = ParamSensetivity(pvarsVals[1,:,:],propsVals[1,:,:])
for i in range(coefs.shape[1]):
    plt.figure()
    plt.bar(range(len(pvars)),coefs[:,i],tick_label=pvars)
    plt.title(props[i])
'''
'''
Synchrony Params Sens
'''
filesProps = glob(datadir+'*/*dt0.tsv')
dtPropsVals = np.zeros((1,2,numData,2),dtype='object')
bad = set()
for file in filesProps:
    file = file.replace('\\','/')
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    num = int(fnames[-2])
    dtPropsVals[0,col,num,0] = temp['cell'+str(row)+'_'+str(col)+'/vOld/peak']
    dtPropsVals[0,col,num,1] = temp['cell'+str(row)+'_'+str(col)+'/vOld/maxt']
    cls = temp['cell'+str(row)+'_'+str(col)+'/vOld/cl']
    if np.std(cls[-10:-1]) > 20:    
        bad.add(num)
propsValsSync = np.zeros((numData,2))
for i in range(numData):
    times,syncT,syncV = calcSyncVarLen(dtPropsVals[:,:,i,0],dtPropsVals[:,:,i,1])
    propsValsSync[i,0] = np.nanmean(syncT)
    propsValsSync[i,1] = np.nanmean(syncV)
#    if propsValsSync[i,0] > 50:
#        bad.add(i)
syncs = ['syncT','syncV']
bad = list(bad)
gpvarsVals = np.delete(pvarsVals,bad,axis=1)
gpropsValsSync = np.delete(propsValsSync,bad,axis=0)
syncCoefs = ParamSensetivity(gpvarsVals[1,:,:],gpropsValsSync)
for i in range(syncCoefs.shape[1]):
    plt.figure()
    plt.bar(range(len(pvars)),syncCoefs[:,i],tick_label=pvars)
    plt.title(syncs[i]+' '+u.split(s.split(datadir)[-2])[-1])