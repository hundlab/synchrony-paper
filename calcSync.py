#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:47:25 2017

@author: dgratz
"""
import numpy as np
import itertools
import math
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib
from collections import deque

def calcSync(vVal,vTime):
    syncT = np.zeros(vTime.shape[0])
    syncV = np.zeros(vVal.shape[0])
    for i in range(vTime.shape[0]):
        syncT[i] = np.std(vTime[i,:])
        syncV[i] = np.std(vVal[i,:])
    return syncT,syncV

def distance(p1,p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def manhatDist(p):
    p1,p2 = p
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def addCells(cells):
    newCells = set()
    for cell in cells:
        newCells.add((cell[0]+1,cell[1]))
        newCells.add((cell[0]-1,cell[1]))
        newCells.add((cell[0],cell[1]+1))
        newCells.add((cell[0],cell[1]-1))
    return newCells.union(cells)

def smallestDistCells(cells):
    cellList = list(cells)
    cellsDists = [{c} for c in cellList]
    while not any(map(lambda cd: len(cd.intersection(cells))>1,cellsDists)):
        for i in range(len(cellsDists)):
            cellsDists[i] = addCells(cellsDists[i])
    pairs = set()
    for cell,cellDist in zip(cellList,cellsDists):
        for pair in cellDist.intersection(cells)-set([cell]):
            pairs.add(frozenset([cell,pair]))
    return set(map(lambda x: tuple(x),pairs))

def argmins(beatCells):
    
    minVal = None
    minsPos = [] 
    for pos,elem in enumerate(nl):
        if minVal is None:
            minVal = elem
            minsPos.append(pos)
        elif minVal == elem:
            minsPos.append(pos)
        elif elem < minVal:
            minsPos = [pos]
    return minsPos

def tDiff(cs,times,poses):
    c1,c2 = cs
    return abs(times[poses.index(c1)]-times[poses.index(c2)])

def calcTimeSync(vVal,vTime,nextBeatDist=3,M=True):
    tVals = np.concatenate(tuple(arr for col in vTime for arr in col))
    vVals = np.concatenate(tuple(arr for col in vVal for arr in col))
    badData = []
    comp = None
    if M:
        comp = lambda a,b: a<b
    else:
        comp = lambda a,b: a>b
    for i in range(len(vVals)):
        if comp(vVals[i],0):
            badData.append(i)
    tVals = np.delete(tVals,badData)
    vVals = np.delete(vVals,badData)
    sortedPos = tVals.argsort()
    tVals = tVals[sortedPos]
    vVals = vVals[sortedPos]
    cells = []
    for cn,col in enumerate(vVal):
        for rn,arr in enumerate(col):
            cells += [(rn,cn)]*len(arr)
    cells = [cells[ind] for ind in sortedPos]
    beatLists = []
    currentBeatSets = []
    currentBeatLists = []
    for i,cell in enumerate(cells):
        removeCBS = None
        potentials = []
        for j,CBS in enumerate(currentBeatSets):
            if cell in CBS:
                removeCBS = j
            elif any(map(lambda c: manhatDist((cell,c)) <= nextBeatDist,CBS)):
                potentials.append((j,len(currentBeatSets[j])))
        ML = max(potentials,key=lambda x: x[1]) if len(potentials) > 0 else None
        if ML is not None:
            currentBeatSets[ML[0]].add(cell)
            currentBeatLists[ML[0]].append(i)
        else:
            currentBeatSets.append(set([cell])) 
            currentBeatLists.append([i])
        if removeCBS is not None:
            beatLists.append(currentBeatLists[removeCBS])
            del currentBeatSets[removeCBS]
            del currentBeatLists[removeCBS]
            
    syncT = []
    syncV = []
    times = []
    for beatList in beatLists:
#        syncT.append(np.std(tVals[beatList]))
        if len(beatList) < 2:
            continue
        beatCellsL = [cells[c] for c in beatList]
        beatCells = set(beatCellsL)
        smCells = smallestDistCells(beatCells)
        smCellsL = list(smCells)
        vals = list(map(lambda am: tDiff(am,tVals[beatList],beatCellsL),smCellsL))
        aM = np.argmax(vals)
        syncT.append(vals[aM]/len(vals))
        syncV.append(np.std(vVals[beatList])/(manhatDist(smCellsL[aM])*len(beatList)))
        times.append(np.mean(tVals[beatList]))
    times,syncT,syncV = np.array(times),np.array(syncT),np.array(syncV)
    sortedArgs = times.argsort()
    times = times[sortedArgs]
    syncT = syncT[sortedArgs]
    syncV = syncV[sortedArgs]
    zs = np.where(syncT == 0)[0]
    syncT[zs] = np.inf
    syncT[zs] = syncT.min()
    zs = np.where(syncV == 0)[0]
    syncV[zs] = np.inf
    syncV[zs] = syncV.min()
    return times,syncT**-1,syncV**-1
    
def calcSyncVarLen(vVal,vTime,M=True):
    tVals = np.concatenate(tuple(arr for col in vTime for arr in col))
    vVals = np.concatenate(tuple(arr for col in vVal for arr in col))
    badData = []
    if M:
        comp = lambda a,b: a<b
    else:
        comp = lambda a,b: a>b
    for i in range(len(vVals)):
        if comp(vVals[i],0):
            badData.append(i)
    tVals = np.delete(tVals,badData)
    vVals = np.delete(vVals,badData)
    sortedPos = tVals.argsort()
    tVals = tVals[sortedPos]
    vVals = vVals[sortedPos]
    cells = []
    for cn,col in enumerate(vVal):
        for rn,arr in enumerate(col):
            cells += [(rn,cn)]*len(arr)
    cells = [cells[ind] for ind in sortedPos]
    
    syncT = []
    syncV = []
    times = []
    beatSet = set()
    begin = 0
    for i,cell in enumerate(cells):
        if cell in beatSet and len(beatSet) >= 2:
            if tVals[i-1]-tVals[begin] > tVals[i] - tVals[i-1] and cells[i-1] != cells[i]:
                begin = i-1
                beatSet = {cells[i-1],cells[i]}
            syncT.append(np.std(tVals[begin:i]))
            syncV.append(np.std(vVals[begin:i]))
            times.append(np.mean(tVals[begin:i]))
            begin = i
            beatSet = {cell}
        else:
            beatSet.add(cell)
    times = np.array(times)
    syncT = np.array(syncT)
    syncV = np.array(syncV)
    zs = np.where(syncT == 0)[0]
    syncT[zs] = np.inf
    syncT[zs] = syncT.min()
    zs = np.where(syncV == 0)[0]
    syncV[zs] = np.inf
    syncV[zs] = syncV.min()
    return times, syncT**-1, syncV**-1
        