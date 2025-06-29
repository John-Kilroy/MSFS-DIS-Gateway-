"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..constants import *
from ..textureUtils import *    

from maxsdk_2024 import sceneUtils
from pymxs import runtime as rt



class TreeView(QTreeWidget):
    """Parent class, unused.
    """
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self._rootDict = {}  # holds link between QTreeWidgetItem and 3ds max node
        self.itemDoubleClicked.connect(lambda item, column: self._doubleClickedItem(item, column))
        self.itemChanged.connect(lambda item, column: self._changedWidgetItem(item, column))

    def setGlobalCheckBox(self, qGlobalCheckBox):
        self._qGlobalCheckBox = qGlobalCheckBox
        self._qGlobalCheckBox.setTristate(False)
        self._qGlobalCheckBox.stateChanged.connect(lambda: self._modifyCheckBox())

    def getSelectedQtItems(self):
        return self.selectedItems()

    def getQtItemsDescendants(self, item):
        hierarchy = []
        hierarchy.append(item)
        for i in range(item.childCount()):
            c = item.child(i)
            hierarchy += self.getQtItemsDescendants(c)
        return hierarchy

    def removeItem(self, qtItem):
        parent = qtItem.parent()
        if parent:
            parent.removeChild(qtItem)
        else:
            self.takeTopLevelItem(self.indexOfTopLevelItem(qtItem))

    def getQtItemWithoutParent(self, qtItem):
        qtItemWithoutParent = qtItem
        oldParentQtItem = qtItem.parent()
        if oldParentQtItem:
            qtItemIdx = oldParentQtItem.indexOfChild(qtItem)
            qtItemWithoutParent = oldParentQtItem.takeChild(qtItemIdx)
        else:
            qtItemWithoutParent = self.takeTopLevelItem(self.indexOfTopLevelItem(qtItemWithoutParent))
        return qtItemWithoutParent

    def changeParent(self, qtItem, newParentQtItem):
        qtItemWithoutParent = self.getQtItemWithoutParent(qtItem)
        newParentQtItem.addChild(qtItemWithoutParent)

    @Slot()
    def _doubleClickedItem(self, item, column):
        if item.childCount() == 0:
            if Qt.ItemIsEditable in item.flags():
                rt.select(self._rootDict[item])

    @Slot()
    def _modifyCheckBox(self):
        selection = self.selectedItems()
        for s in selection:
            hier = self.getQtItemsDescendants(s)
            for h in hier:
                h.setCheckState(0, self._qGlobalCheckBox.checkState())

    @Slot()
    def _changedWidgetItem(self, widget, col):
        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, widget.checkState(col))



