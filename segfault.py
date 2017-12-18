import PyLongQt as pylqt
proto = pylqt.Protocols.GridProtocol()
settings = pylqt.Misc.SettingsIO.getInstance()
settings.readSettings(proto,'/home/dgratz/Documents/data112917-1426/simvars.xml')
ci = pylqt.Structures.CellInfo(0,1,cell=pylqt.Cells.DumbyCell())
#proto.grid.setCell(ci)
