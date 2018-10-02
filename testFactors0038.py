#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:37:07 2017

@author: dgratz
"""

import PyLongQt as pylqt

def testFactors(val,num=20):
    settings = pylqt.Misc.SettingsIO.getInstance()
    proto = pylqt.Protocols.GridProtocol()
    settings.readSettings(proto,'D:/synchrony-data/ela7x7NoConn.xml')
    lastProto = settings.lastProto.clone()
    for row in lastProto.grid:
        for node in row:
            for side in range(4):
                node.setCondConst(0.05,pylqt.Side(side),False,val)
    for val in range(num):
        proto = lastProto.clone()
        proto.pvars.calcIonChanParams()
        proto.setDataDir('D:/synchrony-data/ManyParams/'+str(val))
        print(val)
        proto.runSim()
        settings.writeSettings(proto,proto.datadir+'/'+proto.simvarfile)
