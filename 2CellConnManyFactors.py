#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:14:59 2017

@author: dgratz
"""

import PyLongQt as pylqt
import numpy as np

settings = pylqt.Misc.SettingsIO.getInstance()
proto = pylqt.Protocols.GridProtocol()
settings.readSettings(proto,'D:/synchrony-data/2Kurata_oneRandom.xml')
lastProto = settings.lastProto.clone()
connVals = np.zeros(26)
connVals[1:] = np.logspace(-4,0,25)*lastProto.grid[0,0].getCondConst(pylqt.Side.right)
for counter in range(20):
    lastProto.pvars.calcIonChanParams()
    for val in connVals:
        lastProto.grid[0,0].setCondConst(0.05,pylqt.Side.right,False,val)
        proto = lastProto.clone()
        proto.setDataDir('D:/synchrony-data/AllConnAndRand/'+str(counter)+'/'+str(val))
        print(val,proto.pvars['itoFactor'].cells)
        proto.runSim()
        settings.writeSettings(proto,proto.datadir+'/'+proto.simvarfile)
