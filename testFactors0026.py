#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:03:15 2017

@author: dgratz
"""

import PyLongQt as pylqt

settings = pylqt.Misc.SettingsIO.getInstance()
proto = pylqt.Protocols.GridProtocol()
settings.readSettings(proto,'/home/dgratz/development/synchrony-paper/data/ela7x7NoConn.xml')
lastProto = settings.lastProto.clone()
for row in lastProto.grid:
    for node in row:
        for side in range(4):
            node.setCondConst(0.05,pylqt.Side(side),False,0.0016)
for val in range(2):
    proto = lastProto.clone()
    proto.pvars.calcIonChanParams()
    proto.setDataDir('/home/dgratz/development/synchrony-paper/data/ManyParamsConn0026/'+str(val))
    print(val)
    proto.runSim()
    settings.writeSettings(proto,proto.datadir+'/'+proto.simvarfile)
