#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:52:09 2017

@author: dgratz
"""
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import re

# def graphDSS(foldername):
#     dssFiles = glob(foldername+'/*_dss0.tsv')
#     for dssFile in dssFiles:
#         data = np.genfromtxt(dssFile, delimiter='\t',skip_header=1)
#         for i in range(data.shape[1]):
#             plt.bar(i,data[0,i])

def graphDT(foldername):
    dtFiles = glob(foldername+'/*_dt0.tsv')
    for dtFile in dtFiles:
        with open(dtFile, 'r') as f:
            line = list(filter(None,re.split('\t|cell._./',f.readline().strip())))
            clLoc = line.index('vOld/cl')
            peakLoc = line.index('vOld/peak')
        data = np.genfromtxt(dtFile, delimiter='\t',skip_header=1)
        print(data.shape[0])
        plt.scatter(range(data.shape[0]),data[:,clLoc])
    
def graphDVARS(foldername):
    dvarsFiles = glob(foldername+'/*_dvars.tsv')
    for dvarsFile in dvarsFiles:
        with open(dvarsFile, 'r') as f:
            line = f.readline().strip().split('\t')
            vLoc = line.index('vOld')
            tLoc = line.index('t')
        data = np.genfromtxt(dvarsFile, delimiter='\t',skip_header=1)
        plt.plot(data[:,tLoc],data[:,vLoc])

def graphAll(foldername):
    plt.figure(0)
    graphDVARS(foldername)
    plt.xlim([0,100])
#    plt.figure(1)
#    graphDT(foldername)
    plt.show()
