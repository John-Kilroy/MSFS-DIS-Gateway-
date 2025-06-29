
import logging
import os

import TextureTool2024.textureUtils as textureUtils
import TextureTool2024.ui.TT_mainwindow as TT_mainWindowUI

from TextureTool2024.constants import *
from TextureTool2024.TextureLib.BitmapConfig import compatibleBitmapIndex
from TextureTool2024.TextureLib.textureXmlLib import XmlSerializer
from TextureTool2024.view import treeViewFlags, treeViewTexture
from TextureTool2024.view.treeViewFlags import FLAGS
from TextureTool2024 import textureTool as TT

from pymxs import runtime as rt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import maxsdk_2024.qtUtils as qtUtils
import maxsdk_2024.sceneUtils as sceneUtils
import maxsdk_2024.userprop as userprop

from maxsdk_2024.globals import *
from maxsdk_2024.logger import LoggerWidget, SignalHandler
from maxsdk_2024.perforce import *
from maxsdk_2024.sceneUtils import *

if MAXVERSION() >= MAX2021:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

handler = SignalHandler()

class MainWindow(QMainWindow, TT_mainWindowUI.Ui_TextureTool):
    
    def __init__(self, parent=None):

        ### Init attributes :
        ## Set the Config Parser
        self.config = ConfigParser()
        ## Set the last edited texture
        self.lastEditedTextures = []
        ## Set Dict of filter Flags
        self.filteredFlags = []
        
        parent = QWidget.find(rt.windows.getMAXHWND())
        QMainWindow.__init__(self, parent)
        
    """
        Methods
    """
    def run(self):
        TT.run()

    def show(self):
        """
            Init TextureTool View and  Create trees and initialize Data
        """
        self.setupUi(self)
        self.initUI()

        self.initTrees()
        super().show()
        
    def initUI(self):
        """
            Filters
        """
        self.ckQualityHigh.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.QualityHigh.name.upper(), state = self.ckQualityHigh.isChecked()))
        self.ckAlphaPreserv.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.AlphaPreservation.name.upper(), state = self.ckAlphaPreserv.isChecked()))
        self.ckNoReduc.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.NoReduce.name.upper(), state = self.ckNoReduc.isChecked()))
        self.ckNoMipmap.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.NoMipmap.name.upper(), state = self.ckNoMipmap.isChecked()))
        self.ckPreComputedInvAvg.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.PreComputedInvAvg.name.upper(), state = self.ckPreComputedInvAvg.isChecked()))
        self.ckAnis0.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.Anisotropicx0.name.replace("x", "=").upper(), state = self.ckAnis0.isChecked()))
        self.ckAnis2.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.Anisotropicx2.name.replace("x", "=").upper(), state = self.ckAnis2.isChecked()))
        self.ckAnis4.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.Anisotropicx4.name.replace("x", "=").upper(), state = self.ckAnis4.isChecked()))
        self.ckAnis8.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.Anisotropicx8.name.replace("x", "=").upper(), state = self.ckAnis8.isChecked()))
        self.ckAnis16.stateChanged.connect(lambda : self._filterFlags(flag = FLAGS.Anisotropicx16.name.replace("x", "=").upper(), state = self.ckAnis16.isChecked()))

        """
            Textures Tab
        """        
        # Texture(s) View Tab Set Up
        self.verticalLayout.removeWidget(self.treeTexture)
        self.treeTexture.deleteLater()
        self.treeTexture = treeViewTexture.TreeViewTexture(self.tabTextureWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeTexture.sizePolicy().hasHeightForWidth())
        self.treeTexture.setSizePolicy(sizePolicy)
        self.treeTexture.setAlternatingRowColors(True)
        self.treeTexture.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeTexture.setSortingEnabled(True)
        self.treeTexture.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.treeTexture.setDragEnabled(True)
        self.treeTexture.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeTexture.setDefaultDropAction(Qt.MoveAction)
        self.treeTexture.setObjectName("treeTexture")
        self.treeTexture.headerItem().setText(0, QApplication.translate("TextureTool", "         Textures", None, -1))
        self.treeTexture.setColumnWidth(0, 450)
        self.treeTexture.headerItem().setText(1, QApplication.translate("TextureTool", "Path", None, -1))
        self.checkBoxTextureModifier = qtUtils.createCheckBox(qtWidget=self.treeTexture)
        self.treeTexture.setGlobalCheckBox(self.checkBoxTextureModifier)
        self.verticalLayout.insertWidget(2, self.treeTexture)
        self.treeTexture.itemSelectionChanged.connect(self._selectionChangedTexture)

        header = self.treeTexture.header()
        header.setDefaultSectionSize(250)
        
        """
            Textures View
        """
        ## Add new group
        self.btnAddGroup.clicked.connect(self._addNewGroup)
        ## Add new texture(s)
        self.btnAddTexture.clicked.connect(self._addNewTexture)
        ## Button Remove Group
        self.btnRemoveGroup.clicked.connect(self._removeGroup)
        ## Button Expand All Textures
        self.btnExpandAll.clicked.connect(self.treeTexture.expandAll)
        ## Button Collapse All Textures
        self.btnCollapseAll.clicked.connect(self.treeTexture.collapseAll)
        ## Bar Filter Name
        self.filterBar.textChanged.connect(self._filterItem)

        """
            Flags Tab
        """
        self.verticalLayout_2.removeWidget(self.treeFlags)
        self.treeFlags.deleteLater()
        self.treeFlags = treeViewFlags.TreeViewFlags(self.tabTextureWidget)
        self.treeFlags.setAlternatingRowColors(True)
        self.treeFlags.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeFlags.setObjectName("treeFlags")
        self.treeFlags.headerItem().setText(0, QApplication.translate("TextureTool", "         Flags", None, -1))
        self.checkBoxFlagsModifier = qtUtils.createCheckBox(qtWidget=self.treeFlags)
        self.treeFlags.setGlobalCheckBox(self.checkBoxFlagsModifier)
        self.verticalLayout_2.insertWidget(0, self.treeFlags)
        self.treeFlags.buildQTreeFlags()
        self.treeFlags.itemChanged.connect(self._changedFlagsItem)
        
        ## Button Apply Flags(s) to selected texture(s)
        self.btnApplyFlags.clicked.connect(self._clickedApplyFlagsSelectionToSelected)
        ## Button Apply Flags(s) to ticked texture(s)
        self.btnApplyFlagsTicked.clicked.connect(self._clickedApplyFlagsSelectionToTicked)
        
        """
            Texture Lib View
        """
        ## Button to generate XML for selected Texture(s) and Group(s)
        self.btnSelectedTextures.clicked.connect(self._generateXMLSelected)
        ## Generate XML for ticked Texture(s)
        self.btnTickedTextures.clicked.connect(self._generateXMLTicked)
        ## Generate XML for all Texture(s)
        self.btnAllTextures.clicked.connect(self._generateXMLAll)
        
        """
            Utilities View
        """
        ## Open Texture Path Button
        self.btnOpenPath.clicked.connect(self._openTexturePath)
        
        """
            ToolBarMenu
        """
        ## Toolbar Action Remove unused textures in scene
        self.actionRemoveUnusedTextures.triggered.connect(self._removeDeletedTextures)
        ## Toolbar Action Reset Tool
        self.actionResetTool.triggered.connect(self._resetTool)
        ## Toolbar Action Refresh Tool
        self.actionRefreshTool.triggered.connect(self._refreshTool)
        
        """
            Logger
        """
        self.loggerWidget = LoggerWidget()
        self.loggerAreaVerticalLayout.addWidget(self.loggerWidget)
        handler.emitter.logRecord.connect(self.loggerWidget.appendLogRecord)
        
        self.textureToolLogger = logging.getLogger("TextureToolLogger")
        self.textureToolLogger.setLevel(level=logging.INFO)
        self.textureToolLogger.addHandler(handler)

        
        """"
            Splitter(s)
        """
        self.splitter_2.moveSplitter(5, 1)
        
        """
            Others
        """
        self.setFocus()
           
    def initTrees(self):
        """Initialize Qt items"""
        self.treeTexture.createTree()
        self.treeFlags.createTree()
    
    def applyFlagsSelectionToItems(self, items, flagNames):
        for item in items:
            item.edit(flags=flagNames)
            if not isinstance(item, textureUtils.GroupObject):
                self.textureToolLogger.info(f"[FLAGS][{', '.join(flagNames)}] applied to: {item.name}")
                continue

            groupQtItem = self.treeTexture.getQtGroupItemFromIdentifier(item.identifier)
            self.treeTexture.updateWidget(item, groupQtItem)
            
            textures = self.treeTexture.getTexturesFromGroup(item)
            self.applyFlagsSelectionToItems(textures, flagNames)

        self.treeFlags.isEdited = False
                
    def saveScene(self):
        """Save max scene"""
        r = qtUtils.popup_Yes_No(title="Apply Unsaved Changes ?",text="You need to save the scene to apply modification")
        baseFile = rt.maxFilePath + rt.maxFileName
        if r:
            if baseFile != None:
                s = rt.saveMaxFile(baseFile)
                if s == False:
                    rt.messageBox("Save failed, your file could be readonly. Choose another path.")
                    f = rt.getSaveFileName(caption="Save as", filename=baseFile)
                    if f != None:
                        rt.saveMaxFile(f)
                        self.textureToolLogger.info("[TextureTool] Successfully saved the scene ")
                        return True
                    else:
                        self.textureToolLogger.warning("[TextureTool][WARNING] Your scene has not been saved, you need to save it before generating XMLs for your textures")
                        return False  
                else:
                    self.textureToolLogger.info("[TextureTool] Successfully saved the scene ")
                    return True
            else:
                f = rt.getSaveFileName(caption="Save as", filename=baseFile)
                if f != None:
                    rt.saveMaxFile(f)
                    self.textureToolLogger.info("[TextureTool] Successfully saved the scene ")
                    return True
                else:
                    self.textureToolLogger.warning("[TextureTool][WARNING] Your scene has not been saved, you need to save it before generating XMLs for your textures")
                    return False
        else:
            return False
        
    def checkSameFlags(self, textures):
        """Check if texture(s) have the same flags in a List -> Return True if they have the same flags and False if not"""
        if (len(textures) < 2):
            return True

        for i in range(0, len(textures) - 1):
            tex1 = textures[i]
            tex2 = textures[i + 1]
            if (tex1.flags != tex2.flags):
                return False

        return True
        
    def generateXML(self, textures=[]):
        """Generate XML for a list of TextureObject(s)"""
        for texture in textures:
            if not texture.config:
                self.textureToolLogger.error(f"[TEXTURELIB][ERROR] An xml couldn't be created for this texture : {texture.name}")
                continue
            
            if texture.config.materialBitmap == 0:
                self.textureToolLogger.warning(f"[TEXTURELIB][WARNING] {texture.name} -> has no valid configuration in scene")
                continue

            if texture.flags and len(texture.flags) > 0:
                texture.config.userFlags = '+' + ('+'.join(texture.flags)).upper()

            done, returnString = self.createXML(texture.path, texture.config)
            if not done:
                self.textureToolLogger.error(f"[TEXTURELIB][ERROR] {texture.name} -> {returnString}")
            else:
                self.textureToolLogger.info(f"[TEXTURELIB] {texture.name} -> {returnString}")

    def createXML(self, texturePath, textureConfig) :
        """
        Write a new xml with the textureConfig at the xmlPath location
        Return a tuple with a bool return value and string with information if it's (created / skipped / overwriting compatible / overwriting / Failed)
        """
        absTexturePath = textureUtils.convertRelativePathToAbsolute(texturePath)
        if absTexturePath is None:
            return (False, f"Failed, Texture path {absTexturePath} does not exist.")

        if ' ' in os.path.basename(absTexturePath):
            return (False, "Failed, the name of the texture contains whitespace(s), so the XML will not be generated for it. Please remove them before regenerating.")

        xmlPath = absTexturePath + ".xml"
        serializer = XmlSerializer(xmlPath)
        doesFileAlreadyExists = os.path.exists(xmlPath)
        if doesFileAlreadyExists:
            P4edit(xmlPath)
            if not serializer.Open() :
                return (False, f"File {xmlPath} is maybe readonly and can't be opened.")

            if (serializer.bmpConfig.materialBitmap == textureConfig.materialBitmap 
                and serializer.bmpConfig.forceNoAlpha == textureConfig.forceNoAlpha 
                and serializer.bmpConfig.userFlags == textureConfig.userFlags):
                return (True, "Done (skip)")
            elif compatibleBitmapIndex(serializer.bmpConfig.materialBitmap, textureConfig.materialBitmap) :
                serializer.bmpConfig.materialBitmap = textureConfig.materialBitmap
                serializer.bmpConfig.forceNoAlpha = textureConfig.forceNoAlpha
                if (serializer.bmpConfig.userFlags != textureConfig.userFlags): ## Compatible Bitmaps but not same userflags
                    serializer.bmpConfig.userFlags = textureConfig.userFlags
                retString = "Done (overwriting compatible)"
            else :
                self.textureToolLogger.warning(f"[TEXTURELIB][WARNING] {xmlPath} - Texture has changed slot and configuation.")
                serializer.bmpConfig = textureConfig
                retString = "Done (overwriting)"
        else:
            serializer.bmpConfig = textureConfig
            retString = "Done (created)"
        
        saved = serializer.Save()
        if saved:
            P4edit(xmlPath)
            P4edit(absTexturePath)
            return (True, retString)

        return (False, "Failed (writing went wrong).")
   
    """
        Events Handlers 
    """ 
    def _refreshTool(self):
        """Refresh Qt Items"""
        self.treeTexture.refreshTree()
        self.treeFlags.refreshTree()
    
    def _addNewGroup(self):
        """Create a new group and assign selected texture(s) to it if there is"""
        newGroup = textureUtils.createNewGroup(labelName = "NewGroup")
        newGroupQtItem = self.treeTexture.createGroupWidget(newGroup)
        newGroupQtItem.setExpanded(True)

        textures = self.treeTexture.getSelectedTextures()
        for texture in textures:
            texture.edit(groupID=newGroup.identifier)
            self.treeTexture.updateParentingTexture(texture, newGroupQtItem)

        self.treeTexture.setCurrentItem(newGroupQtItem)
    
    def _addNewTexture(self):
        """ Add new texture if a texture with same name if referenced in scene """
        textures = self.treeTexture.getSelectedTextures()
        if (len(textures) == 0):
            filPath = textureUtils.askForExistingPath("Select an existing texture(s)", rt.maxFilePath)
        else:
            filPath = textureUtils.askForExistingPath("Select an existing texture(s)", textures[0].path)
        
        if filPath is None or filPath == '.':
            return

        textures = self.treeTexture.getAllTexturesList()
        for path in filPath:
            path = textureUtils.convertRelativePathToAbsolute(path)
            texture = self.treeTexture.getTextureWithSameNameButDiffPathInList(path, textures)
            if texture is None:
                self.textureToolLogger.error(f"[TEXTURE][ERROR] Texture Name : {os.path.basename(path)} does not exists in project or already added in the Texture Tool. Texture item will not be created.")
                continue

            path = textureUtils.convertAbsolutePathToRelative(path)
            name = os.path.basename(path)
            newTexture = textureUtils.createNewTexture(
                labelName = name, 
                filePath = path, 
                groupID = texture.groupID, 
                flags = texture.flags, 
                config = texture.config
            )
            newTextureQtItem = self.treeTexture.createTextureWidget(newTexture)  
            self.treeTexture.setCurrentItem(newTextureQtItem)   
                        
    def _removeGroup(self):
        """ Remove Group Item(s) """
        groups = self.treeTexture.getSelectedGroups()
        self.treeTexture.removeItems(groups=groups)
    
    ## TODO see if this is useful
    def _resetTool(self):
        """Reset saved DATA to default"""
        confirm = qtUtils.popup_Yes_No(
                title="Confirm choice ?",
                text="Are you sure you want to reset the tool ? If you do your will lost all the saved DATA applied to your textures."
        )
        if not confirm:
            return
        sceneRoot = sceneUtils.getSceneRootNode()
        textureList = userprop.getUserPropList(sceneRoot, PROP_TEXTURE_LIST)
        if (textureList is not None):
            userprop.removeUserProp(sceneRoot, PROP_TEXTURE_LIST)
            for texture in textureList:
                userprop.removeUserProp(sceneRoot, texture)
        groupList = userprop.getUserPropList(sceneRoot, PROP_TEXTURE_GROUP_LIST)
        if (groupList is not None):
            userprop.removeUserProp(sceneRoot, PROP_TEXTURE_GROUP_LIST)
            for group in groupList:
                userprop.removeUserProp(sceneRoot, group)
        self._refreshTool()
    
    def _clickedApplyFlagsSelectionToSelected(self):
        """If groups are selected or ticked"""
        checkedFlags = self.treeFlags.getCheckedFlagNames()

        selectedGroups = self.treeTexture.getSelectedGroups()
        selectedTextures = self.treeTexture.getSelectedTextures()
        selectedItems = [*selectedGroups, *selectedTextures]
        if len(selectedItems) > 0:
            self.applyFlagsSelectionToItems(selectedItems, checkedFlags)
            rt.setSaveRequired(True)
                  
    def _clickedApplyFlagsSelectionToTicked(self):
        """If groups are selected or ticked"""
        checkedFlags = self.treeFlags.getCheckedFlagNames()

        checkedGroups = self.treeTexture.getCheckedGroups()
        checkedTextures = self.treeTexture.getCheckedTextures()
        checkedItems = [*checkedGroups, *checkedTextures]
        if len(checkedItems) > 0:
            self.applyFlagsSelectionToItems(checkedItems, checkedFlags)
            rt.setSaveRequired(True)
    
    def _selectionChangedTexture(self):
        """Signal when texture(s) are selected"""
        if (self.treeFlags.isEdited and self.lastEditedTextures):
            flagSelection = self.treeFlags.getCheckedFlagNames()
            self.applyFlagsSelectionToItems(self.lastEditedTextures, flagSelection)
                        
        selectedGroups = self.treeTexture.getSelectedGroups()
        selectedTextures = self.treeTexture.getSelectedTextures() 

        selectedItems = [*selectedGroups, *selectedTextures]
        sameFlags = self.checkSameFlags(selectedItems)
        if not sameFlags:
            self.treeFlags.uncheckAllFlags()
            self.treeFlags.setEnabled(False)
            return

        self.treeFlags.setEnabled(True)
        flagNamesGroups = selectedGroups[0].flags if len(selectedGroups) > 0 else []
        flagNamesTextures = selectedTextures[0].flags if len(selectedTextures) > 0 else []
        flagNames = [*flagNamesGroups, *flagNamesTextures]
        self.treeFlags.initializeCheckFlags(flagNames)            
           
    def _changedFlagsItem(self):
        """Signal when flag item is changed"""
        textures = self.treeTexture.getSelectedTextures()
        textures.extend(self.treeTexture.getCheckedTextures())
        textures = list(dict.fromkeys(textures))
        
        groups = self.treeTexture.getSelectedGroups()
        groups.extend(self.treeTexture.getCheckedGroups())
        groups = list(dict.fromkeys(groups))
        
        for group in groups:
            textureGroup = self.treeTexture.getTexturesFromGroup(group)
            result = [t for t in textureGroup if not t in textures]
            textures.extend(result)

        self.lastEditedTextures = [*textures, *groups]
        self.treeFlags.isEdited = True if len(self.lastEditedTextures) > 0 else False
            
    def _removeDeletedTextures(self):
        """Remove not used texture(s) in scene"""
        if (not self.treeTexture.removeDeletedTexturesFromView()):
            rt.messageBox("There are no textures to delete.")
    
    def _generateXMLSelected(self):
        """Generate XML for selected group(s) and texture(s)"""
        textures = []
        groupsSelected = self.treeTexture.getSelectedGroups()
        for group in groupsSelected:
            texturesGroup = self.treeTexture.getTexturesFromGroup(group)
            textures.extend(texturesGroup)

        texturesSelected = self.treeTexture.getSelectedTextures()
        textures.extend(texturesSelected)

        ## Delete duplicate if there is
        textures = list(dict.fromkeys(textures))

        ## Generate XMl
        self.generateXML(textures)
    
    def _generateXMLTicked(self):
        """Generate XML for ticked Textures"""
        ## We don't need to get the groups (if they are check, their internal textures will be checked too)
        textures = self.treeTexture.getCheckedTextures()
        ## Delete duplicate if there is
        textures = list(dict.fromkeys(textures))
        ## Generate XMl
        self.generateXML(textures)
    
    def _generateXMLAll(self):
        """Generate XML for all texture(s)"""
        textures = self.treeTexture.getAllTexturesList()
        ## Delete duplicate if there is
        textures = list(dict.fromkeys(textures))
        ## Generate XMl
        self.generateXML(textures)
    
    def _openTexturePath(self):
        """ Open an explorer in the path of selected texture"""
        textures = self.treeTexture.getSelectedTextures()
        if len(textures) <= 0:
            rt.messageBox("Select a valid texture path to open.")
            return

        path = textureUtils.convertRelativePathToAbsolute(textures[0].path)
        if path is None:
            self.textureToolLogger.error(f"[TEXTURE] '{textures[0].name}' have not a valid path.")
            return

        try:
            exportPath = os.path.split(path)[0]
            os.startfile(exportPath)
        except WindowsError:
            self.textureToolLogger.error(f"The given path : {exportPath} does not exist")

    def _filterItem(self):
        filterName = self.filterBar.text()
        self.treeTexture.filterTree(filterName = filterName)    

    def _filterFlags(self, flag = "", state = False):
        if state:
            self.filteredFlags.append(flag)
        else:
            self.filteredFlags.remove(flag)
        
        self.treeTexture.filterTreeWithFlags(self.filteredFlags)

    def closeEvent(self, event):
        global window
        window = None

################################
########## Window ##############
################################    
window = None
        
def run():
    global window
    if window is None:
        window = MainWindow()
        window.show()
        return
    
    if window.windowState() != Qt.WindowActive:
        window.showNormal()