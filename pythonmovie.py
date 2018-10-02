#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib
#matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import re
from pathlib import Path
from readFile import readFile

def makeMovieArray(times,vals,moviename,fps = 40,flipY = False,metadata = None,slowFactor=2,cmap='hot',showColorbar=True):
    dataFPS = 1//(np.mean(np.diff(times[0,0,:]))*0.001)
    nrows,ncols = times.shape[:2]
    print('FPS of the data is:',dataFPS)
    '''
    construct mp4 video writer and plt that will be used as the frame buffer
    '''
    FFMpegWriter = manimation.writers['ffmpeg']
    writer = FFMpegWriter(fps=fps,metadata=metadata)

    fig = plt.figure()
    im = plt.imshow(np.zeros((nrows,ncols)),cmap=cmap,vmax=vals.max(),vmin=vals.min(),extent=[0,ncols,nrows,0])
    ax = plt.axes()
    if showColorbar:
        plt.colorbar()
    ax.grid(color='k', linewidth=2)
    ax.set_xticklabels('')
    ax.set_xticks(np.arange(0.5,ncols,1), minor=True)
    ax.set_xticklabels(np.arange(1,ncols+1), minor=True)
    ax.set_yticklabels('')
    ax.set_yticks(np.arange(0.5,nrows,1), minor=True)
    ax.set_yticklabels(np.arange(1,nrows+1), minor=True)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    if flipY:
        plt.gca().invert_yaxis()
    else:
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
    '''
    write frames to video and save file
    '''
    with writer.saving(fig, str(moviename), dpi=100):
        lenData = vals.shape[2]
        perc = 0.1
        percVal = lenData*perc
        for i in range(0,lenData,max(1,int(dataFPS//fps)//slowFactor)):
            im.set_data(vals[:,:,i])
            writer.grab_frame()
            if i >= percVal:
                print('%{0:.1f}'.format(perc*100),sep='',end=' ')
                perc += 0.1
                percVal = lenData*perc
    plt.close(fig)
    print()

def makeMovie(src,moviename,fps = 40,flipY = False,metadata = None,slowFactor=2,cmap='hot'):
    '''
    creates a movie from the voltage values for a grid simulation
    src: the directory that contains the files
    moviename: the name of the movie (should end in .mp4)
    ex. makeMovie('/home/dgratz/Documents/data092517-1149/','data092517-1149.mp4')
    '''
    src = Path(src)
    moviename = Path(moviename)
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
            voltages = np.zeros((nrows,ncols,len(data['vOld'])))
            first = False
        times[pos] = data['t']
        voltages[pos] = data['vOld']
        print(pos,'',end='')
    print()

    makeMovieArray(times,voltages,moviename,fps=fps,flipY=flipY,metadata=metadata,slowFactor=slowFactor,cmap=cmap)
    return times
