#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:03:12 2017

@author: dgratz
"""

import PyLongQt as pylqt

settings = pylqt.Misc.SettingsIO.getInstance()
proto = pylqt.Protocols.GridProtocol()
settings.readSettings(proto,'/home/dgratz/development/synchrony-paper/data/ela7x7NoConn.xml')
lastProto = settings.lastProto.clone()
lastProto.pvars.calcIonChanParams()
vals = [0.0, .00038, .0008, .0016, .0026, .0038, .038, .38, 3.8]
for val in vals:
#for i in np.linspace(B[1]*0.001,B[1],20):
    for row in lastProto.grid:
        for node in row:
            for side in range(4):
                node.setCondConst(0.05,pylqt.Side(side),False,val)
    proto = lastProto.clone()
    proto.setDataDir('/home/dgratz/development/synchrony-paper/data/AllConnLogNormal/'+str(val))
    print(val)
    proto.runSim()
    settings.writeSettings(proto,proto.datadir+'/'+proto.simvarfile)
