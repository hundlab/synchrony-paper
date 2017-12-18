#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:04:05 2017

@author: dgratz
"""
import numpy as np

def writeGrid(dataTimes,dataVals,fname):
    someWriten = True
    num = 0
    with open(fname,'w') as f:
        while someWriten:
            someWriten = False
            for row in range(dataTimes.shape[0]):
                for col in range(dataTimes.shape[1]):
                    for data in (dataTimes,dataVals):
                        if not isinstance(data[row,col],np.ndarray) or num >= len(data[row,col]):
                            f.write(',')
                        else:
                            f.write(str(data[row,col][num])+',')
                            someWriten = True
            num += 1
            f.write('\n')