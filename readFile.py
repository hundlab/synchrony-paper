#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 10:37:50 2017

@author: dgratz
"""
import numpy as np

def readFile(filename,delem='\t'):
    with open(filename,'r') as f:
        headers = f.readline().strip().split(delem)
    data = np.genfromtxt(filename, delimiter=delem,skip_header=1)
    if len(data.shape) == 2:
        return {header: data[:,i] for i,header in enumerate(headers)}
    else:
        return {header: data[i] for i,header in enumerate(headers)}