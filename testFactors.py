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
    settings.readSettings(proto,'/home/dgratz/development/synchrony-paper/data/ela7x7NoConn.xml')
    lastProto = settings.lastProto.clone()
    lastProto.pvars.calcIonChanParams()
    for row in lastProto.grid:
        for node in row:
            for side in range(4):
                node.setCondConst(0.05,pylqt.Side(side),False,val)
    for n in range(num):
        proto = lastProto.clone()
        proto.pvars.calcIonChanParams()
        proto.setDataDir('/home/dgratz/development/synchrony-paper/data/ManyParams_'+str(val)+'/'+str(n))
        print(n)
        proto.runSim()
        settings.writeSettings(proto,proto.datadir+'/'+proto.simvarfile)
