#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:32:36 2017

@author: dgratz
"""
import matplotlib.pyplot as plt

'''
read in files for CL graphs adn sync graphs
'''
from plotBeat2beatCLGrid import b2bCL
from plotSynchronyMeasure import b2bSync

b2bSTimes,b2bST,b2bSV=b2bSync('/home/dgratz/development/synchrony-paper/data/AllConnLogNormal/0.0/')
b2bCLX, b2bCLY = b2bCL('/home/dgratz/development/synchrony-paper/data/AllConnLogNormal/0.0')
for i in range(b2bCLX.shape[0]):
    for j in range(b2bCLX.shape[1]):
        plt.plot(b2bCLX[i,j],b2bCLY[i,j])
plt.plot(b2bSTimes,b2bST)