#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:13:14 2017

@author: dgratz
"""

from scipy import stats
import numpy as np
from numpy.linalg import inv

def ParamSensetivity(X,Y,logData=True):
    if logData:
        X = np.log(X)
    Xz = np.zeros(X.shape)
    Yz = np.zeros(Y.shape)
    for rn in range(X.shape[1]):
        Xz[:,rn] = stats.zscore(X[:,rn])
    for rn in range(Y.shape[1]):
        Yz[:,rn] = stats.zscore(Y[:,rn])
    return inv(np.transpose(Xz).dot(Xz)).dot(np.transpose(Xz)).dot(Yz)