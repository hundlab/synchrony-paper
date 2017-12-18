# coding: utf-8
import PyLongQt
grid = PyLongQt.Structures.Grid()
grid.addColumns(2)
grid.addRow(0)
newNode = PyLongQt.Structures.CellInfo()
newNode.cell = PyLongQt.cellMap['Rabbit Sinus Node (Kurata 2008)']()
print(newNode.cell.type)
newNode.X = 0
newNode.Y = 0
grid.setCellTypes(newNode)
