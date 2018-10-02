#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 15:45:45 2017

@author: dgratz
"""
from readFile import readFile
import re
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

s = re.compile('/')
u = re.compile('_')
datadir = 'D:/synchrony-data/AllConnAndRand/'
conns = list(map(lambda x: float(s.split(x)[-1]), glob(datadir+'0/*')))
data = np.zeros((2,26,20))

files = glob(datadir+'*/*/cell*dt0.tsv*')
for file in files:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    conn = float(fnames[-2])
    connPos = conns.index(conn)
    simNum = int(fnames[-3])
    data[col,connPos,simNum] = np.min(temp['cell'+str(row)+'_'+str(col)+'/vOld/cl'][-10:-1])
plt.figure(0)
vOld_cl_line = np.zeros(shape=(2,26))
vOld_cl_line[0,:] = np.mean(data[0,:,:],axis=1)
vOld_cl_line[1,:] = np.mean(data[1,:,:],axis=1)
vOld_cl_error = np.zeros(shape=(2,26)) 
vOld_cl_error[0,:] = np.std(data[0,:,:],axis=1)
vOld_cl_error[1,:] = np.std(data[1,:,:],axis=1)
plt.errorbar(conns,vOld_cl_line[0,:],yerr=vOld_cl_error[0,:],alpha=0.7)
plt.errorbar(conns,vOld_cl_line[1,:],yerr=vOld_cl_error[1,:],alpha=0.7)
plt.xscale('log')
plt.title('vOld/cl')

files = glob(datadir+'*/*/cell*dss0.tsv*')
for file in files:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    conn = float(fnames[-2])
    connPos = conns.index(conn)
    simNum = int(fnames[-3])
    data[col,connPos,simNum] = temp['cell'+str(row)+'_'+str(col)+'/vOld/peak']
plt.figure(1)
vOld_peak_line = np.zeros(shape=(2,26))
vOld_peak_line[0,:] = np.mean(data[0,:,:],axis=1)
vOld_peak_line[1,:] = np.mean(data[1,:,:],axis=1)
vOld_peak_error = np.zeros(shape=(2,26))
vOld_peak_error[0,:] = np.std(data[0,:,:],axis=1)
vOld_peak_error[1,:] = np.std(data[1,:,:],axis=1)
plt.errorbar(conns,vOld_peak_line[0,:],yerr=vOld_peak_error[0,:],alpha=0.7)
plt.errorbar(conns,vOld_peak_line[1,:],yerr=vOld_peak_error[1,:],alpha=0.7)
plt.xscale('log')
plt.title('vOld/peak')


files = glob(datadir+'*/*/cell*dss0.tsv*')
for file in files:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    conn = float(fnames[-2])
    connPos = conns.index(conn)
    simNum = int(fnames[-3])
    data[col,connPos,simNum] = temp['cell'+str(row)+'_'+str(col)+'/vOld/min']
plt.figure(2)
vOld_min_line = np.zeros(shape=(2,26))
vOld_min_line[0,:] = np.mean(data[0,:,:],axis=1)
vOld_min_line[1,:] = np.mean(data[1,:,:],axis=1)
vOld_min_error = np.zeros(shape=(2,26))
vOld_min_error[0,:] = np.std(data[0,:,:],axis=1)
vOld_min_error[1,:] = np.std(data[1,:,:],axis=1)
plt.errorbar(conns,vOld_min_line[0,:],yerr=vOld_min_error[0,:],alpha=0.7)
plt.errorbar(conns,vOld_min_line[1,:],yerr=vOld_min_error[1,:],alpha=0.7)
plt.xscale('log')
plt.title('vOld/min')

files = glob(datadir+'*/*/cell*dss0.tsv*')
for file in files:
    temp = readFile(file)
    fnames = s.split(file)
    uparts = u.split(fnames[-1])
    (row,col) = tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),uparts)))
    conn = float(fnames[-2])
    connPos = conns.index(conn)
    simNum = int(fnames[-3])
    data[col,connPos,simNum] = temp['cell'+str(row)+'_'+str(col)+'/caI/peak']
plt.figure(3)
caI_peak_line = np.zeros(shape=(2,26))
caI_peak_line[0,:] = np.mean(data[0,:,:],axis=1)
caI_peak_line[1,:] = np.mean(data[1,:,:],axis=1)
caI_peak_error = np.zeros(shape=(2,26))
caI_peak_error[0,:] = np.std(data[0,:,:],axis=1)
caI_peak_error[1,:] = np.std(data[1,:,:],axis=1)
plt.errorbar(conns,caI_peak_line[0,:],yerr=caI_peak_error[0,:],alpha=0.7)
plt.errorbar(conns,caI_peak_line[1,:],yerr=caI_peak_error[1,:],alpha=0.7)
plt.xscale('log')
plt.title('caI/peak')
