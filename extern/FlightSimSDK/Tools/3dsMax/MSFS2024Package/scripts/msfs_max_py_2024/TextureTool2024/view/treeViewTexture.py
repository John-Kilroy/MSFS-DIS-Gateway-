"""Module to handle PySide2 QTreeWidget in the 3dsMax context.
"""
import logging
import os

import TextureTool2024.constants as const

import maxsdk_2024.sceneUtils as sceneUtils

from pymxs import runtime as rt

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from TextureTool2024.textureUtils import *
from TextureTool2024.textureConfig import *
from TextureTool2024.TextureLib.BitmapConfig import compatibleBitmapIndex
from TextureTool2024.view.treeView import TreeView

from maxsdk_2024.logger import SignalHandler


handler = SignalHandler()

class TreeViewTexture(TreeView):
    """
        Class to gather textures and put them in a QTreeWidget.
    """
    hasChanged = Signal()
    rootNode = sceneUtils.getSceneRootNode()

    def __init__(self, parent, textureStorageId = const.PROP_TEXTURE_LIST, groupStorageid = const.PROP_TEXTURE_GROUP_LIST):
        TreeView.__init__(self, parent)
        self.textureStorageId = textureStorageId
        self.groupStorageId = groupStorageid
        self._groupDict = {}

        self._logger = logging.getLogger("TextureToolLogger")
        self._logger.setLevel(level=logging.INFO)
        self._logger.addHandler(handler)

    def updateWidget(self, obj, qTreeWidget):
        if hasattr(obj, "name") and obj.name != None: ## Texture + Group
            qTreeWidget.setText(0, str(obj.name))

        if hasattr(obj, "path") and obj.path != None: ## Texture
            relativePath = obj.path
            relativePath = convertAbsolutePathToRelative(obj.path)
            qTreeWidget.setText(1, relativePath)

        elif hasattr(obj, "flags") and len(obj.flags) > 0: ## Group
            qTreeWidget.setText(1, f"Flags = [{', '.join(obj.flags)}]")

    def createTextureWidget(self, texture):
        qTreeWidgetItem = QTreeWidgetItem()
        qTreeWidgetItem.setCheckState(0, Qt.CheckState.Unchecked)
        qTreeWidgetItem.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsSelectable |
                                 Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.updateWidget(texture, qTreeWidgetItem)

        groupItem = self.getTextureGroupItem(texture=texture)
        if groupItem:
            groupItem.addChild(qTreeWidgetItem)
        else:
            self.addTopLevelItem(qTreeWidgetItem)

        self._rootDict[qTreeWidgetItem] = texture
        return qTreeWidgetItem

    def createGroupWidget(self, group):
        qTreeWidgetItem = QTreeWidgetItem()
        qTreeWidgetItem.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable |
                                 Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        qTreeWidgetItem.setCheckState(0, Qt.CheckState.Unchecked)
        self.updateWidget(group, qTreeWidgetItem)
        self.addTopLevelItem(qTreeWidgetItem)

        self._groupDict[qTreeWidgetItem] = group
        return qTreeWidgetItem

    def createTree(self):
        """Create a list of checkable items for textures"""
        curExpandedGroupsID = self.getExpandedGroupsID()

        self.clearSelection()
        self._rootDict.clear()
        self._groupDict.clear()
        self.clear()
        
        textureList = userprop.getUserPropList(self.rootNode, const.PROP_TEXTURE_LIST)
        groupList = userprop.getUserPropList(self.rootNode, const.PROP_TEXTURE_GROUP_LIST)

        textureList = textureList if textureList is not None else []
        groupList = groupList if groupList is not None else []

        groups = self.getGroups(groupList=groupList)
        for group in groups:
            self.createGroupWidget(group)

        self.savedTexturesPaths, self.savedTextures = self.getSavedTexturesSceneObjects(textureList=textureList)
        for texture in self.savedTextures:
            self.createTextureWidget(texture)

        newTextures = self.getAllNewTextures(textureList=textureList)
        for texture in newTextures:
            self.createTextureWidget(texture)

        ## Expand expanded groups after the refresh
        for widget in self._groupDict.keys():
            if self._groupDict[widget].identifier in curExpandedGroupsID:
                self.expandItem(widget)

    def updateParentingTexture(self, texture, parentItem):
        textureItem = self.getQtTextureItemFromIdentifier(texture.identifier)
        self.changeParent(textureItem, parentItem)

    def getExpandedGroupsID(self):
        """ Return a List of Expanded -> Group Identifier(s)"""
        expandedGroupsKeys = list()
        for widget, group in self._groupDict.items():
            if widget.isExpanded():
                expandedGroupsKeys.append(group.identifier)
        return expandedGroupsKeys

    def getTextureGroupItem(self, texture):
        """ Check wether a texture object has a group id or not - Return the Item of the group"""
        for groupItem, group in self._groupDict.items():
            if group.identifier == texture.groupID:
               return groupItem
        return None

    def refreshTree(self):
        """ Refresh the texture items list"""
        self.createTree()

    def getSelectedTextures(self):
        """ Return the selected textures -> List of TextureObject"""
        selected = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            if item not in self._rootDict:
                continue
            selected.append(self._rootDict[item])
        return selected

    def getSelectedGroups(self):
        """ Return the selected groups -> List of GroupObject"""
        selected = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            if item not in self._groupDict:
                continue
            selected.append(self._groupDict[item])
        return selected

    def getCheckedTextures(self):
        """Return the checked(ticked) textures -> List of TextureObject"""
        selected = []
        for k in self._rootDict.keys():
            if k.checkState(0) == Qt.Checked:
                texture = self._rootDict[k]
                selected.append(texture)
        return selected

    def getCheckedGroups(self):
        selected = []
        for k in self._groupDict.keys():
            if k.checkState(0) == Qt.Checked:
                group = self._groupDict[k]
                selected.append(group)
        return selected

    def getQtTextureItemFromIdentifier(self, identifier):
        """Get a QT Item from a given identifier (QtItem.identifier)"""
        for k, v in self._rootDict.items():
            if v.identifier == identifier:
                return k
        return None

    def getQtGroupItemFromIdentifier(self, identifier):
        """Get a QT Item from a given identifier (QtItem.identifier)"""
        for k, v in self._groupDict.items():
            if v.identifier == identifier:
                return k
        return None

    def getAllNewTextures(self, textureList=[]):
        """Return all textures references in max scene in a List of TextureObject with its configuration"""
        resultList = []
        textureConfigs = self.getTexturesConfig()

        for textureName, textureConfig in textureConfigs.items():
            path = convertAbsolutePathToRelative(textureConfig.path)
            if (textureName in const.PATH_FORBIDDEN_TEXTURE_NAMES): ## Case MSFS2024_Material Textures
                continue

            if (path in self.savedTexturesPaths):
                continue

            textureObject = createNewTexture(
                labelName = textureName, 
                filePath = path, 
                flags = [], 
                config = textureConfig.bitmapConfig,
                sceneRoot = self.rootNode,
                textureList = textureList
            )
            resultList.append(textureObject)

        return resultList

    def getTextureWithSameNameButDiffPathInList(self, path = '', textures = []):
        """ Return True if a path exist in the list of Texture Items"""
        for texture in textures:
            if os.path.basename(path) != texture.name:
                continue

            texturePath = convertRelativePathToAbsolute(texture.path)
            if path != texturePath:
                return texture

        return None

    def getTexturesConfig(self):
        """Return all textures references in max scene in a Dict of TextureObject with key == name if the texture"""
        resultedTextureConfigs = dict()
        msfs2024Materials = self.getMSFS2024Materials()
        for msfs2024Material in msfs2024Materials:
            materialTextureConfig = GetMatConfigFromScene(msfs2024Material)
            for textureName, textureConfig in materialTextureConfig.items():
                if textureName not in resultedTextureConfigs:
                    resultedTextureConfigs[textureName] = textureConfig

                    if (textureConfig.bitmapConfig.materialBitmap == 0):
                        self._logger.warning(f"[TEXTURE][BITMAP][WARNING] {textureName} has no valid configuration in scene.")

                elif not compatibleBitmapIndex(resultedTextureConfigs[textureName].bitmapConfig.materialBitmap, textureConfig.bitmapConfig.materialBitmap):
                    self._logger.warning(f"[TEXTURE][BITMAP][WARNING] Same image name for different config : {textureName} -> {str(textureConfig.bitmapConfig.__name__)} / {resultedTextureConfigs[textureName].bitmapConfig.__name__}")
        
        return resultedTextureConfigs

    def getMSFS2024Materials(self):
        result = []
        allSceneMaterials = list(rt.sceneMaterials)
        for sceneMaterial in allSceneMaterials:
            if str(rt.classOf(sceneMaterial)) == "Multimaterial":
                nbrSubMat =  rt.getNumSubMtls(sceneMaterial)
                for i in range(1, nbrSubMat + 1):
                    subMat = rt.getSubMtl(sceneMaterial, i)
                    if str(rt.classOf(subMat)) == "MSFS2024_Material":
                        result.append(subMat)

            elif str(rt.classOf(sceneMaterial)) == "MSFS2024_Material":
                result.append(sceneMaterial)
        
        return result

    def getAllUsedTexturesInScene(self):
        """Get all textures in scene in a list of Tuple(name, path)"""
        resultSet = set()
        resultList = dict()
        materials = self.getMSFS2024Materials()

        for material in materials:
            textureList = material.TexList            
            for textureProp in textureList:
                texturePropName = textureProp + "Tex"
                texturePath = rt.getProperty(material, texturePropName)
                resultSet.add(texturePath)

        for usedMapPath in resultSet:
            name = basename(usedMapPath)
            if (name in const.PATH_FORBIDDEN_TEXTURE_NAMES): ## Case MSFS2024_Material Textures
                continue
            path = convertAbsolutePathToRelative(usedMapPath)
            resultList[path] = name

        return resultList

    def getDeletedTextureObjects(self, textureList):
        """Get the textures saved but deleted from material"""
        allTexturesPathNameMap = self.getAllUsedTexturesInScene()
        sceneRoot = sceneUtils.getSceneRootNode() 
        resultList = dict()
        for savedTexture in textureList:
            textureObject = TextureObject(savedTexture, sceneRoot=sceneRoot, propList=textureList)
            if textureObject.path not in allTexturesPathNameMap:
                resultList[savedTexture] = textureObject
        return resultList

    def removeDeletedTexturesFromView(self):
        """Reset the texture view by deleting textures saved but does not exist anymore"""
        sceneRoot = sceneUtils.getSceneRootNode()
        textureList = userprop.getUserPropList(sceneRoot, const.PROP_TEXTURE_LIST)
        if (textureList is None):
            return False

        deletedTextureObjects = self.getDeletedTextureObjects(textureList)
        if len(deletedTextureObjects) == 0:
            return False

        found = False
        for textureId, toDeleteTextureObject in deletedTextureObjects.items():
            if textureId not in textureList:
                continue

            absPath = convertRelativePathToAbsolute(toDeleteTextureObject.path)
            try:
                textureList.remove(textureId)
                userprop.removeUserProp(sceneRoot, textureId)

                textureQtItem = self.getQtTextureItemFromIdentifier(toDeleteTextureObject.identifier)
                self.removeItem(textureQtItem)
                if textureQtItem in self._rootDict:
                    self._rootDict.pop(textureQtItem)

                found = True
                
                self._logger.info(f"[TEXTURE][{toDeleteTextureObject.name}] Path '{absPath}' : is not used anymore, deleted from Texture Tool View")
            except:
                self._logger.warning(f"[TEXTURE][{toDeleteTextureObject.name}] Path '{absPath}' : could not be deleted from saved DATA")

        userprop.setUserPropList(sceneRoot, const.PROP_TEXTURE_LIST, textureList)

        return found

    def getGroups(self, groupList=[]):
        """Get the stored group(s) object(s) in scene Root"""
        groups = []
        for groupID in groupList:
            g = GroupObject(groupID, sceneRoot=self.rootNode, propList=groupList)
            groups.append(g)
        return groups

    def getSavedTexturesSceneObjects(self, textureList=[]):
        """Get the stored texture(s) object(s) in scene root"""
        texturesObject = []
        texturesPaths = []

        if textureList is None:
            return (texturesPaths, texturesObject)

        for textureID in textureList:
            texture = TextureObject(textureID, sceneRoot=self.rootNode, propList=textureList)
            texturesObject.append(texture)
            texturesPaths.append(texture.path)

        return (texturesPaths, texturesObject)

    def getTexturesFromGroup(self, group):
        """Get List of TextureObject assigned to a group"""
        textures = []
        for texture in self._rootDict.values():
            if texture.groupID == group.identifier:
                textures.append(texture)
        return textures

    def getGroupItemFromTexture(self, texture):
        for groupItem, group in self._groupDict.items():
            if group.identifier == texture.groupID:
                return groupItem
        return None

    def getAllTexturesList(self):
        """Get a list of all textures items presents in texture view tab -> list(qtreewidgetItem)"""
        return list(self._rootDict.values())

    def filterTree(self, filterName = ""):
        for item in self._rootDict.keys():
            if (filterName == "" or str.lower(filterName) in str.lower(item.text(0))):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def filterTreeWithFlags(self, flags):
        for item in self._rootDict.keys():
            if len(flags) <= 0:
                item.setHidden(False)
                continue

            texture = self._rootDict[item]
            if all(flag in texture.flags for flag in flags):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def removeItems(self, groups=[]):
        yesAll = False
        for group in groups:
            if not yesAll:
                popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                    title="Delete Group ?", text="Are you sure you want to delete the group {0}".format(group.name))
                if popup == QMessageBox.NoToAll:
                    return
                if popup == QMessageBox.YesToAll:
                    yesAll = True
                if popup == QMessageBox.No or popup == popup == QMessageBox.NoToAll:
                    continue
            
            textures = self.getTexturesFromGroup(group)
            for texture in textures:
                textureItem = self.getQtTextureItemFromIdentifier(texture.identifier)
                textureItemWithoutParent = self.getQtItemWithoutParent(textureItem)
                self.addTopLevelItem(textureItemWithoutParent)

            groupItem = self.getQtGroupItemFromIdentifier(group.identifier)
            self.removeItem(groupItem)
            group.delete()
            try:
                self._groupDict.pop(groupItem)
            except KeyError as exception:
                print("There is no such key : " + exception.message)

    """ Events Handlers """
    def _doubleClickedItem(self, item, column):
        if not item in self._groupDict:
            return

        if (column == 1):
            item.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsSelectable |
                        Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        else:
            item.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable |
                        Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

    @Slot()
    def _changedWidgetItem(self, item, col):
        """Update the widget and the group(s) according to the new data"""
        ## Modify Checkbox for descendants if there is
        for i in range(item.childCount()):
            child = item.child(i)
            if (col == 0):
                child.setCheckState(col, item.checkState(col))

        newName = item.text(0)
        newName = userprop.cleanupStringForPropListStorage(newName)
        ## Change name of the group
        if item in self._groupDict:
            self._groupDict[item].edit(name=newName)

        self.hasChanged.emit()

    def dropEvent(self, event):
        """To Handle the drop event"""
        targetItem = self.itemAt(event.pos())
        selectedTextures = self.getSelectedTextures()

        parentItem = targetItem.parent() if targetItem is not None else None
        targetItem = parentItem if parentItem is not None else targetItem
        found = (targetItem in self._groupDict) if targetItem is not None else False

        target = self._groupDict[targetItem] if found else None
        for selectedTexture in selectedTextures:
            selectedItem = self.getQtTextureItemFromIdentifier(selectedTexture.identifier)
            if not selectedItem:
                continue

            if found:
                selectedTexture.edit(groupID=target.identifier)
                self.changeParent(selectedItem, targetItem)
            else:
                selectedTexture.edit(groupID="-")
                selectedItemWithoutParent = self.getQtItemWithoutParent(selectedItem)
                self.addTopLevelItem(selectedItemWithoutParent)

        self.hasChanged.emit()