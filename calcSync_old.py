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

def calcTimeSync(vVal,vTime,nextBeatDist=3):
    tVals = np.concatenate(tuple(arr for col in vTime for arr in col))
    vVals = np.concatenate(tuple(arr for col in vVal for arr in col))
    badData = []
    for i in range(len(vVals)):
        if vVals[i] < 0:
            badData.append(i)
    tVals = np.delete(tVals,badData)
    vVals = np.delete(vVals,badData)
    sortedPos = tVals.argsort()
    tVals = tVals[sortedPos]
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
        syncT.append(vals[aM])
        syncV.append(np.std(vVals[beatList]))
        times.append(np.mean(tVals[beatList]))
    times,syncT,syncV = np.array(times),np.array(syncT),np.array(syncV)
    sortedArgs = times.argsort()
    times = times[sortedArgs]
    syncT = syncT[sortedArgs]
    return times,syncT,syncV
    
def calcSyncVarLen(vVal,vTime):
    tVals = np.concatenate(tuple(arr for col in vTime for arr in col))
    vVals = np.concatenate(tuple(arr for col in vVal for arr in col))
    badData = []
    for i in range(len(vVals)):
        if vVals[i] < 0:
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
    
    mhatDistCells = np.zeros(len(cells)-1)
    for i in range(len(cells)-1):
        mhatDistCells[i] = manhatDist((cells[i],cells[i+1]))

#    plt.plot(mhatDistCells)
    beatSets = []
    foundCells = set()
    begin = 0
    for i,cell in enumerate(cells):
        if cell in foundCells and len(foundCells) >= 2:
            beatSets.append(slice(begin,i))
            begin += cells[begin:i].index(cell)+1
            foundCells = set(cells[begin:i+1])
        else:
            foundCells.add(cell)

    
    syncT = []
    syncV = []
    times = []
    beatSetNum = 0
    i = 0
    while i < len(cells) and beatSetNum < len(beatSets):
        minBeatSet = beatSetNum
        minBeatSetVal = 0
        while beatSetNum < len(beatSets) and beatSets[beatSetNum].start <= i and i < beatSets[beatSetNum].stop:
            beatSetVal = np.mean(mhatDistCells[beatSets[beatSetNum]])
            if beatSetVal < minBeatSetVal:
                minBeatSetVal = beatSetVal
                minBeatSet = beatSetNum
            beatSetNum += 1
        begin = beatSets[minBeatSet].start
        end = beatSets[minBeatSet].stop
        beatCells = set(cells[begin:end])
        
        smCells = smallestDistCells(beatCells)
        
#            distances = np.array([distance(cells[pos],cells[begin]) for pos in  range(begin+1,i)])
        smCellsL = list(smCells)
        vals = list(map(lambda am: tDiff(am,tVals[begin:end],cells[begin:end]),smCellsL))
        aM = np.argmax(vals)
#            print(tVals[begin],tVals[begin:i][cells[begin:i].index(p[0])])
#            syncT.append(np.max((tVals[begin+1:i]-tVals[begin])/(distances))/len(foundCells))
#        syncT.append(vals[aM])
        syncT.append(np.std(vals))
        syncV.append(np.std(vVals[begin:end]))
        times.append(np.mean(tVals[begin:end]))
        i = end
        while beatSetNum < len(beatSets) and beatSets[beatSetNum].start <= i-1 and i-1 < beatSets[beatSetNum].stop:
            beatSetNum += 1
#        plt.plot([begin,end],[8,7])
#    plt.figure()
    return np.array(times),np.array(syncT),np.array(syncV)
        