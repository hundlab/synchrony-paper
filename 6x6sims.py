# coding: utf-8
import sys
import PyLongQt
testName = sys.argv[1]
print(testName)
proto = PyLongQt.protoMap['Grid Protocol']()
settings = PyLongQt.Misc.SettingsIO.getInstance()
settings.readSettings(proto,'/home/dgratz/Documents/'+testName+'.xml')
#proto.setDataDir('/home/dgratz/development/synchrony-paper'+'/data/1KurataRandom_1OnalAtrial')
simProto = proto.clone()
#simProto.setDataDir(simProto.datadir+'/'+str(i))
#simProto.pvars.calcIonChanParams()
simProto.runSim()
settings.writeSettings(simProto,simProto.datadir+'/simvars.xml')
print(simProto.datadir)
from pythonmovie import *
makeMovie(simProto.datadir+'/','/tmp/'+testName+'.mp4')
