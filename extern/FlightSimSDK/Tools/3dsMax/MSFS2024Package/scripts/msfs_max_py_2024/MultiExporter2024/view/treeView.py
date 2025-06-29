"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
import logging

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..constants import *
from ..presetUtils import *

from maxsdk_2024.logger import SignalHandler

handler = SignalHandler()
treeViewLogger = logging.getLogger("TreeViewLogger")
treeViewLogger.setLevel(level=logging.INFO)
treeViewLogger.addHandler(handler)

class LongPathDelegate(QStyledItemDelegate): #Cut too long path but NOT on the right
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        option.textElideMode = Qt.ElideLeft #Qt.ElideMiddle
        
        QStyledItemDelegate.paint(self, painter, option, index)

class TreeView(QTreeWidget):
    """Parent class, unused.
    """
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self._alwaysSelectInScene = False
        self._selectInSceneSelectsChildren = True
        self._rootDict = {}
        self.loaded = False
        self.itemSelectionChanged.connect(self._selectionChanged)
        self.itemDoubleClicked.connect(self._doubleClickedItem)
        self.itemChanged.connect(lambda item, column: self._changedWidgetItem(item, column))

    def setGlobalCheckBox(self, qGlobalCheckBox):
        self._qGlobalCheckBox = qGlobalCheckBox
        self._qGlobalCheckBox.setTristate(False)
        self._qGlobalCheckBox.stateChanged.connect(lambda: self._modifyGlobalCheckBox())

    def createTree(self):
        return

    def refreshTree(self):
        self.createTree()

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

    def getSelectedQtItems(self):
        return self.selectedItems()

    def getQtItemsDescendants(self, item):
        hierarchy = []
        hierarchy.append(item)
        for i in range(item.childCount()):
            child = item.child(i)
            hierarchy += self.getQtItemsDescendants(child)
        return hierarchy

    def getTopParentQtItem(self, widget):
        widgetParent = widget.parent()
        if widgetParent is None:
            return widget
        else:
            return self.getTopParentQtItem(widgetParent)

    def getParentQtItem(self, widget):
        widgetParent = widget.parent()
        if widgetParent is None:
            return widget
        else:
            return widgetParent

    def createRootWidget(self):
        return QTreeWidgetItem()

    def areAllChildrenHidden(self, item):
        for i in range(item.childCount()):
            if not item.child(i).isHidden():
                return False
        return True
    
    def removeItem(self, qtItem):
        if qtItem is None:
            return
        
        parent = qtItem.parent()
        if parent:
            parent.removeChild(qtItem)
        else:
            self.takeTopLevelItem(self.indexOfTopLevelItem(qtItem))

    def startEditingItem(self, item, columns):
        for column in columns:
            self.editItem(item, column)
        self.hasChanged.emit()

    @Slot()
    def _doubleClickedItem(self, item):
        return None

    @Slot()
    def _selectionChanged(self):
        return None

    @Slot()
    def _modifyGlobalCheckBox(self):
        selectedItems = self.selectedItems()
        for selectedItem in selectedItems:
            hierarchy = self.getQtItemsDescendants(selectedItem)
            for childItem in hierarchy:
                if childItem in self._rootDict:
                    childItem.setCheckState(0, self._qGlobalCheckBox.checkState())

    @Slot()
    def _changedWidgetItem(self, widget, col):
        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, widget.checkState(col))


