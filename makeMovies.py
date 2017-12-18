#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:19:11 2017

@author: dgratz
"""
from pythonmovie import makeMovie


videos = {'Figure7_C':'/home/dgratz/development/synchrony-paper/data/AllConnLogNormal/0.38/',
'Figure7_B':'/home/dgratz/development/synchrony-paper/data/ManyParamsLogNormal/data0.0038_20/',
'Figure7_A':'/home/dgratz/development/synchrony-paper/data/AllConnLogNormal/0.0/',
'0.00014':'/home/dgratz/development/synchrony-paper/data/ManyParamsLogNormal/data0.0016_51/',
'0.00022':'/home/dgratz/development/synchrony-paper/data/ManyParamsLogNormal/data0.0026_46/',
'0.00033':'/home/dgratz/development/synchrony-paper/data/ManyParamsLogNormal/data0.0038_23/'
}
folder = '/home/dgratz/development/synchrony-paper/finalvids/'
for vid in videos:
    makeMovie(videos[vid],folder+vid+'.mp4',flipY = True)
