"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""

from MultiExporter2024.view.treeView import TreeView
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk_2024 import layer as sdklayer
from maxsdk_2024 import sceneUtils as sdksceneUtils
from maxsdk_2024 import qtUtils

from ..constants import *
from ..presetUtils import *


class TreeViewLayer(TreeView):
    """Class to gather scene layers and represent them as a hierarchy in a QTreeView. _layerDict connects the QtItems with their corresponding sdklayer
    """
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._layerDict = {}
        self.isEdited = False
        self.repercuteCheck = True

    def gatherLayers(self):
        return sdklayer.getAllRootLayer()

    def getExpandedLayersNames(self):
        expandedLayerNames = set()
        for layerItem, layer in self._layerDict.items():
            if layerItem.isExpanded():
                expandedLayerNames.add(layer.name)
        return expandedLayerNames

    def createTree(self, progressBar=None, lbProgressBar=None):
        if not self.loaded:
            expandedLayerNames = self.getExpandedLayersNames()

            self.clear()
            self._rootDict.clear()
            self._layerDict.clear()
            layers = self.gatherLayers()
            qtUtils.initProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar, maxRange=len(layers), actionTitle="Loading Layers")
            for layer in layers:
                qTreeWidget = self.buildQTreeLayer(None, layer)
                self.addTopLevelItem(qTreeWidget)
                if progressBar is not None:
                    progressBar.setValue(progressBar.value() + 1)
            qtUtils.resetProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar)
            
            ## Expand last expanded layers
            for layerItem, layer in self._layerDict.items():
                if layer.name in expandedLayerNames:
                    self.expandItem(layerItem)

            self.loaded = True

    def refreshTree(self, progressBar=None, lbProgressBar=None):
        self.loaded = False
        self.createTree(progressBar=progressBar, lbProgressBar=lbProgressBar)

    # recursive function to build hierarchy of layers
    def buildQTreeLayer(self, widget, layer):
        qTreeChild = QTreeWidgetItem()
        qTreeChild.setCheckState(0, Qt.CheckState.Unchecked)

        qTreeChild.setText(0, layer.name)
        # add widget to dictionary with actual sdklayer as value
        self._layerDict[qTreeChild] = layer
        childrenLayers = sdklayer.getChildrenLayer(layer)
        for c in childrenLayers:
            self.buildQTreeLayer(qTreeChild, c)
        if widget is not None:  # if it's not the initial call
            widget.addChild(qTreeChild)  # bind new widget to parent
            return None  # and we get out of the function
        else:
            return qTreeChild  # only return reference to the widget when in the initial call

    def _modifyGlobalCheckBox(self):
        selectedItems = self.selectedItems()
        for selectedItem in selectedItems:
            hierarchy = self.getQtItemsDescendants(selectedItem)
            selectedItem.setCheckState(0, self._qGlobalCheckBox.checkState())
            for child in hierarchy:
                child.setCheckState(0, self._qGlobalCheckBox.checkState())

    def intializeCheckLayers(self, layerNames):
        topItem = [x for x in self._layerDict.keys() if x.parent() is None]
        childItem = [x for x in self._layerDict.keys() if x.parent() is not None]
        # A change to a parent's checkbox cascades to its children
        # So we first work on the parents and then the children
        self.repercuteCheck = False

        for item in topItem + childItem: 
            if item.text(0) in layerNames:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)

        self.repercuteCheck = True
        self.isEdited = False

    def uncheckAllLayers(self):
        for k in self._layerDict.keys():
            k.setCheckState(0, Qt.CheckState.Unchecked)
        self.isEdited = False

    def getCheckedLayerNames(self):
        layerNames = []
        for item in self._layerDict.keys():
            if item.checkState(0) == Qt.CheckState.Checked:
                layerNames.append(item.text(0))
        return layerNames
    
    def getCheckedLayers(self):
        layers = []
        for item in self._layerDict.keys():
            if item.checkState(0) == Qt.CheckState.Checked:
                layers.append(item)
        return layers
    
    def getPartCheckedLayerNames(self):
        layerNames = []
        for item in self._layerDict.keys():
            if item.checkState(0) == Qt.CheckState.PartiallyChecked:
                layerNames.append(item.text(0))
        return layerNames   

    def getSelectedLayers(self):
        layers = []
        selection = self.getSelectedQtItems()
        for s in selection:
            items = self.getQtItemsDescendants(s)
            for item in items:
                i = self._layerDict[item]
                if (i not in layers):
                    layers.append(i)
        return layers


    @Slot()
    def _changedWidgetItem(self, widget, col):
        if (self.repercuteCheck == False):
            return # Don't do anything when not repercuting 

        state = widget.checkState(col)

        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, state)
        self.repercuteCheck = False
        if widget.parent() is not None:
            par = widget.parent()
            self._updateParentCheckbox(parent = par, checkBoxColumn = col, state = state)
        self.repercuteCheck = True

    def _updateParentCheckbox(self, parent, checkBoxColumn, state = Qt.CheckState.Unchecked):
        col = checkBoxColumn
        if (parent.childCount() != 0):
            isallUnchecked = True
            isallChecked = True      
            for i in range(parent.childCount()):
                if parent.child(i).checkState(0) == Qt.CheckState.Unchecked or parent.child(i).checkState(0) == Qt.CheckState.PartiallyChecked:
                    isallChecked = False
                if parent.child(i).checkState(0) == Qt.CheckState.Checked or parent.child(i).checkState(0) == Qt.CheckState.PartiallyChecked:
                    isallUnchecked = False
                if isallChecked == False and isallUnchecked == False:
                    break                
            if isallChecked:
                parent.setCheckState(col, Qt.CheckState.Checked)
            if isallUnchecked:
                parent.setCheckState(col, Qt.CheckState.Unchecked)
            if isallChecked == False and isallUnchecked == False:
                parent.setCheckState(col, Qt.CheckState.PartiallyChecked)
        else:
            parent.setCheckState(col, state)
        if parent.parent() is not None:
            newParent = parent.parent()
            self._updateParentCheckbox(newParent, col, state)


    @Slot()
    def _selectionChanged(self):
        selection = self.getSelectedLayers()
        sdksceneUtils.selectLayers(selection)

    def _doubleClickedItem(self):
        return None