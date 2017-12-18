#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:08:46 2017

@author: dgratz
"""

import PyLongQt as pylqt
from multiprocessing import Pool
settings = pylqt.Misc.SettingsIO.getInstance()
proto = pylqt.Protocols.GridProtocol()
settings.readSettings(proto,'/home/dgratz/development/synchrony-paper/data/2SAN1RandLogNormal.xml')
lastProto = settings.lastProto.clone()
def runSim(num):
    proto = lastProto.clone()
    proto.pvars.calcIonChanParams()
    proto.setDataDir('/home/dgratz/development/synchrony-paper/data/2SAN1RandLogNormal/'+str(num))
    proto.runSim()
    settings.writeSettings(proto,proto.datadir+'/'+proto.simvarfile)
    return num
p = Pool(4)
print(p.map(runSim,range(300)))