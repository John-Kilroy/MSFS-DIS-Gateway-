"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..constants import *
from ..textureUtils import *
from TextureTool2024.view.treeView import TreeView

from enum import Enum

"""Enumerate the different flags"""
class FLAGS(Enum):
    QualityHigh = "Quality High"
    AlphaPreservation = "Alpha Preservation"
    NoReduce = "No Reduction"
    NoMipmap = "No Mipmaps"
    PreComputedInvAvg = "PreComputed Inverse Average"
    Anisotropic = "Anisotropic"
    Anisotropicx0 = "x0 (Standard)"
    Anisotropicx2 = "x2 (High)"
    Anisotropicx4 = "x4 (Very High)"
    Anisotropicx8 = "x8 (Extreme)"
    Anisotropicx16 = "x16 (Insane)"


class TreeViewFlags(TreeView):
    """Class to gather texture Flags to add in the XML
    """
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._flagsDict = {}
        self.isEdited = False
      
    def createTree(self):
        """Create a list of tickable items for flags""" 
        self.clearSelection()
        self._rootDict.clear()
        self._flagsDict.clear()
        self.clear()
        
        self.buildQTreeFlags()
    
    def refreshTree(self):
        """refresh the flags tree"""
        self.initializeCheckFlags()   
    
    def getCheckedFlagNames(self):
        """return a list of flags ticked(checked)"""    
        flagNames = []
        flag = ""
        for item in self._flagsDict.keys():
            if item.checkState(0) != Qt.CheckState.Checked:
                continue
            
            if (item.parent()): ## Anisotropic Case
                flag = self._flagsDict[item].replace("x", "=").upper()
            else:
                flag = self._flagsDict[item].upper()
            flagNames.append(flag)
        return flagNames
    
    def initializeCheckFlags(self, flagNames = []):
        """Initialize check(s) / tick(s) for flags depending of the texture selected"""
        ## TODO find a way to show tristate value if flag is not selected in all selected textures
        for item, flag in self._flagsDict.items():
            flag =  flag.upper()
            if (flag == FLAGS.Anisotropic.name.upper()): ## Anisotropic don't need to be checked, only its children are checked
                continue

            if (flag.split("X")[0] == FLAGS.Anisotropic.name.upper()):
                flag = flag.replace("X", "=")

            if flag in flagNames:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)
        self.isEdited = False
    
    def uncheckAllFlags(self):
        """Uncheck all flags"""
        for k in self._flagsDict.keys():
            k.setCheckState(0, Qt.CheckState.Unchecked)
        self.isEdited = False

    def buildQTreeFlags(self):
        """Build the flags tree items"""
        item1 = QTreeWidgetItem(self, [FLAGS.QualityHigh.value])
        item1.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[item1] = FLAGS.QualityHigh.name
        
        item2 = QTreeWidgetItem(self, [FLAGS.AlphaPreservation.value])
        item2.setCheckState(0, Qt.CheckState.Unchecked)
        item2.setToolTip(0, "*IMPORTANT* To be checked only if the texture has 4 slots (RGBA)")
        self._flagsDict[item2] = FLAGS.AlphaPreservation.name
        
        item3 = QTreeWidgetItem(self, [FLAGS.NoReduce.value])
        item3.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[item3] = FLAGS.NoReduce.name
        
        item4 = QTreeWidgetItem(self, [FLAGS.NoMipmap.value])
        item4.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[item4] = FLAGS.NoMipmap.name
        
        item5 = QTreeWidgetItem(self, [FLAGS.PreComputedInvAvg.value])
        item5.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[item5] = FLAGS.PreComputedInvAvg.name

        item6 = QTreeWidgetItem(self, [FLAGS.Anisotropic.value])
        item6.setExpanded(True)
        item6.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self._flagsDict[item6] = FLAGS.Anisotropic.name
        
        child1 = QTreeWidgetItem(item6, [FLAGS.Anisotropicx0.value])
        child1.setCheckState(0, Qt.CheckState.Unchecked)        
        self._flagsDict[child1] = FLAGS.Anisotropicx0.name
        
        child2 = QTreeWidgetItem(item6, [FLAGS.Anisotropicx2.value])
        child2.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[child2] = FLAGS.Anisotropicx2.name
        
        child3 = QTreeWidgetItem(item6, [FLAGS.Anisotropicx4.value])
        child3.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[child3] = FLAGS.Anisotropicx4.name
        
        child4 = QTreeWidgetItem(item6, [FLAGS.Anisotropicx8.value])
        child4.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[child4] = FLAGS.Anisotropicx8.name
        
        child5 = QTreeWidgetItem(item6, [FLAGS.Anisotropicx16.value])
        child5.setCheckState(0, Qt.CheckState.Unchecked)
        self._flagsDict[child5 ] = FLAGS.Anisotropicx16.name
        
    @Slot()
    def _selectionChanged(self):
        return None 
    
    @Slot()
    def _changedWidgetItem(self, widget, col):
        super()._changedWidgetItem(widget, col)
        if(widget.checkState(col) == Qt.CheckState.Checked):
            parent = widget.parent() ## In our case could be anisotropic only
            if(parent is not None):
                for i in range(parent.childCount()):
                    if(widget != parent.child(i)):
                        parent.child(i).setCheckState(col, Qt.CheckState.Unchecked)
                    else:
                        widget.setCheckState(col, Qt.CheckState.Checked)

    @Slot()
    def _doubleClickedItem(self, item, column):
        return None
    
    