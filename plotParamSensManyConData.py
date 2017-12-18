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

cons = np.logspace(-4,-1,10)*3.87138
pvars = list(readFile('/home/dgratz/development/synchrony-paper/data/2SAN1RandLogNormal/0/cell_0_0_dss0_pvars.tsv').keys())
datadir = '/home/dgratz/development/synchrony-paper/data/600Sims10Conns1Rand/'

filesPvars = glob(datadir+'*/*_pvars.tsv')
numData = 616
pvarsVals = [np.zeros((2,numData,len(pvars))) for con in range(len(cons))]
s = re.compile('/')
u = re.compile('_')

for file in filesPvars:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    num = int(fnames[-2])
    for i,pvar in enumerate(pvars):
        pvarsVals[num//numData][col,num%numData,i] = temp[pvar]
        
props = ['vOld/peak','vOld/cl','vOld/min','caI/peak','caI/min',
         'vOld/ddr']
filesProps = glob(datadir+'*/*dss0.tsv')
propsVals = [np.zeros((2,numData,len(props))) for con in range(len(cons))]
for file in filesProps:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    num = int(fnames[-2])
    for i,prop in enumerate(props):
        propsVals[num//numData][col,num%numData,i] = temp['cell'+str(row)+'_'+str(col)+'/'+prop]



'''
Synchrony Params Sens
'''
filesProps = glob(datadir+'*/*dt0.tsv')
dtPropsVals = [np.zeros((1,2,numData,2),dtype='object') for con in range(len(cons))]
bad = [set() for con in range(len(cons))]
for file in filesProps:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    num = int(fnames[-2])
    dtPropsVals[num//numData][0,col,num%numData,0] = temp['cell'+str(row)+'_'+str(col)+'/vOld/peak']
    dtPropsVals[num//numData][0,col,num%numData,1] = temp['cell'+str(row)+'_'+str(col)+'/vOld/maxt']
    cls = temp['cell'+str(row)+'_'+str(col)+'/vOld/cl']
    if np.std(cls[-10:-1]) > 100:    
        bad[num//numData].add(num%numData)
propsValsSync = [np.zeros((numData,2)) for con in range(len(cons))]
for i in range(numData):
    for co in range(10):
        times,syncT,syncV = calcSyncVarLen(dtPropsVals[co][:,:,i,0],dtPropsVals[co][:,:,i,1])
        propsValsSync[co][i,0] = np.nanmean(syncT[-30:len(syncT)])
        if np.isnan(propsValsSync[co][i,0]):
            bad[co].add(i)
        propsValsSync[co][i,1] = np.nanmean(syncV[-30:len(syncV)])
#    if propsValsSync[i,0] > 50:
#        bad.add(i)
syncs = ['syncT','syncV']
bad = list(bad)
for co in range(len(bad)):
    pvarsVals[co] = np.delete(pvarsVals[co],list(bad[co]),axis=1)
    propsValsSync[co] = np.delete(propsValsSync[co],list(bad[co]),axis=0)
    propsVals[co] = np.delete(propsVals[co],list(bad[co]),axis=1)
    
coefs = np.zeros(shape=(10,len(pvars),len(props)))
for i in range(10):
    coefs[i,:,:] = ParamSensetivity(pvarsVals[i][1,:,:], propsVals[i][1,:,:])
for pr in range(coefs.shape[2]):
    plt.figure()
    plt.xscale('log')
    for pv in range(coefs.shape[1]):
        plt.scatter(cons,coefs[:,pv,pr],label=pvars[pv])
    plt.title(props[pr])
    plt.legend()

syncCoefs = np.zeros(shape=(10,len(pvars),len(syncs)))
for co in range(10):
    syncCoefs[co,:,:] = ParamSensetivity(pvarsVals[co][1,:,:],propsValsSync[co][:,:])
for sy in range(syncCoefs.shape[2]):
    plt.figure()
    plt.xscale('log')
    for pv in range(syncCoefs.shape[1]):
        plt.scatter(cons,syncCoefs[:,pv,sy],label=pvars[pv])
    plt.title(syncs[sy])
    plt.legend()