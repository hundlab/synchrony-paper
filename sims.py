# coding: utf-8
import PyLongQt
proto = PyLongQt.protoMap['Grid Protocol']()
settings = PyLongQt.Misc.SettingsIO.getInstance()
settings.readSettings(proto,'/home/dgratz/development/synchrony-paper/data/1KurataRandom_1OnalAtrial.xml')
proto.setDataDir('/home/dgratz/development/synchrony-paper'+'/data/1KurataRandom_1OnalAtrial')
for i in range(400,500):
    simProto = proto.clone()
    simProto.setDataDir(simProto.datadir+'/'+str(i))
    simProto.pvars.calcIonChanParams()
    simProto.runSim()
    settings.writeSettings(simProto,simProto.datadir+'/simvars.xml')
    print(i)
