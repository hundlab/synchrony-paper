#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:19:11 2017

@author: dgratz
"""
from pythonmovie import makeMovie,makeMovieArray
import re
from pathlib import Path
from readFile import readFile
import numpy as np
from calcSync import calcClusters
from glob import glob
import matplotlib.pyplot as plt
import matplotlib

def readTimes(src):
    src = Path(src)
    files = list(src.glob('*dvars.tsv'))
    s = re.compile('_')
    filePos = []
    for file in files:
        file = str(file)
        sp = s.split(file)
        filePos.append(tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),sp))))
    ncols = max(map(lambda x: x[1],filePos))+1
    nrows = max(map(lambda x: x[0],filePos))+1
    first = True
    print('Reading Cells: ',end='')
    for i,(file,pos) in enumerate(zip(files,filePos)):
        data = readFile(file)
        if first:
            times = np.zeros((nrows,ncols,len(data['t'])))
            first = False
        times[pos] = data['t']
        print(pos,'',end='')
    print()
    return times

def b2bClusters(folder,nextBeatDist=3):
    dtFiles = glob(folder+'/*_dt0.tsv')
    s = re.compile('_')
    filePos = []
    for file in dtFiles:
        sp = s.split(file)
        filePos.append(tuple(map(lambda x: int(x),filter(lambda x: x.isdigit(),sp))))
    nrows = max(map(lambda x: x[0],filePos))+1
    ncols = max(map(lambda x: x[1],filePos))+1
    dataPK = np.zeros((nrows,ncols),dtype='object')
    dataMT = np.zeros((nrows,ncols),dtype='object')
    for (file,pos) in zip(dtFiles,filePos):
        dataPK[pos] = readFile(file)['cell'+str(pos[0])+'_'+str(pos[1])+'/vOld/peak']
        dataMT[pos] = readFile(file)['cell'+str(pos[0])+'_'+str(pos[1])+'/vOld/maxt']
    tVals,vVals,cells,beatLists = calcClusters(dataPK, dataMT,nextBeatDist)
    return tVals,vVals,cells,beatLists

videos = {'Figure7_C':'D:/synchrony-data/AllConnLogNormal/0.38/',
'Figure7_B':'D:/synchrony-data/ManyParamsLogNormal/data0.0038_20/',
'Figure7_A':'D:/synchrony-data/AllConnLogNormal/0.0/',
#'0.00014':'D:/synchrony-data/ManyParamsLogNormal/data0.0016_51/',
#'0.00022':'D:/synchrony-data/ManyParamsLogNormal/data0.0026_46/',
#'0.00033':'D:/synchrony-data/ManyParamsLogNormal/data0.0038_23/'
}
folder = 'C:/Users/grat05/Documents/synchrony-paper/finalvids/'

cmaplist = np.array([
       [ 0.        ,  0.        ,  0.        ,  1.        ],
       [ 0.90196078,  0.09803922,  0.29411765,  1.        ],
       [ 0.96078431,  0.50980392,  0.18823529,  1.        ],
       [ 0.23529412,  0.70588235,  0.29411765,  1.        ],
       [ 0.56862745,  0.11764706,  0.70588235,  1.        ],
       [ 0.2745098 ,  0.94117647,  0.94117647,  1.        ]])
cmap = matplotlib.colors.ListedColormap(cmaplist,name='Custom cmap')

for vid in videos:
    times = makeMovie(videos[vid],folder+vid+'.mp4',flipY = True)

    maxColor = cmap.N
#    times = readTimes(videos[vid])
    tVals,vVals,cells,beatLists = b2bClusters(videos[vid])
    vals = np.zeros_like(times,dtype='int')
    timesAvg = np.mean(times,axis=(0,1))
    for bLn,beatList in map(lambda x: ((x[0]%(maxColor-1))+1,x[1]), enumerate(beatLists)):
        beatCellsL = [cells[c] for c in beatList]
        idxs = np.searchsorted(timesAvg,tVals[beatList],side="left")
        idxs = np.append(idxs,min(idxs[-1]+40,vals.shape[2])-1)
        for i,cell in enumerate(beatCellsL):
            vals[cell[0],cell[1],idxs[i]:idxs[-1]] = bLn
    makeMovieArray(times,vals,folder+vid+'_clusters.mp4',fps=40,flipY = True,cmap=cmap,showColorbar=False,slowFactor=4)


