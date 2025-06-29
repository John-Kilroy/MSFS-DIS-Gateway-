"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""

from MultiExporter2024.view.treeView import *
from pymxs import runtime as rt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk_2024 import sceneUtils, userprop, qtUtils

from ..constants import *
from ..presetUtils import *


class TreeViewPreset(TreeView):
    """Class to gather presets in the root node and put them in a QTreeWidget. Widget are connected to Preset using the Dictionary _rootDict and Group Widget using the _groupDict
    """
    hasChanged = Signal()  # custom signal

    def __init__(self, parent, presetStorageId = PROP_PRESET_LIST, groupStorageId = PROP_PRESET_GROUP_LIST):
        TreeView.__init__(self, parent)
        # Path elide
        self.pathDelegate = LongPathDelegate()
        self.setItemDelegateForColumn(getEnumId(PRESETS_COLUMN.PATH), self.pathDelegate)

        self.presetStorageId = presetStorageId
        self.groupStorageId = groupStorageId
        self._groupDict = {} # Dict (qTreewidget, GroupObject)
        

    # upon dropping widget find target and find its group then store selected widgets in said group
    def dropEvent(self, event):
        targetItem = self.itemAt(event.pos())
        found = False
        selectedPresets = self.getSelectedPresets()

        parentItem = targetItem.parent() if targetItem is not None else None
        targetItem = parentItem if parentItem is not None else targetItem
        found = (targetItem in self._groupDict) if targetItem is not None else False

        target = self._groupDict[targetItem] if found else None
        for selectedPreset in selectedPresets:
            selectedQtItem = self.getQtPresetItemFromIdentifier(selectedPreset.identifier)
            if not selectedQtItem:
                continue

            if found:
                selectedPreset.edit(group=target.identifier)
                self.changeParent(selectedQtItem, targetItem)
            else:
                selectedPreset.edit(group="-")
                selectedItemWithoutParent = self.getQtItemWithoutParent(selectedQtItem)
                self.addTopLevelItem(selectedItemWithoutParent)

        self.hasChanged.emit()

    @Slot()
    def _changedWidgetItem(self, widget, col):            
        ## Update the widget and the presets according to the new data
        for i in range(widget.childCount()):
            child = widget.child(i)
            if(col == 0):
                child.setCheckState(col, widget.checkState(col))
            
        newName = widget.text(0)
        newName = userprop.cleanupStringForPropListStorage(newName)
        widget.setText(0, newName)
        
        path = widget.text(1).rsplit('\\', 1)[0]
        if widget in self._rootDict.keys():
            path += '\\' + newName.split('.')[0] + '.gltf'
            widget.setText(1, path)
        
            preset = self._rootDict[widget]
            preset.edit(name=newName, path=path)
        elif widget in self._groupDict.keys():
            group = self._groupDict[widget] 
            group.edit(name=newName)

        self.hasChanged.emit()

    def createTree(self, progressBar = None, lbProgressBar=None):
        if self.loaded:
            return
        
        ## Store expanded groups ids before the refresh
        curExpandedGroupsID = self.getExpandedGroupsID()

        self.clearSelection()
        self.clear()
        self._rootDict.clear()
        self._groupDict.clear()

        rootNode = sceneUtils.getSceneRootNode()
        groupList = userprop.getUserPropList(rootNode, self.groupStorageId)
        presetList = userprop.getUserPropList(rootNode, self.presetStorageId)

        progressBarRange = 0
        progressBarRange += len(groupList) if groupList is not None else 0
        progressBarRange += len(presetList) if presetList is not None else 0

        qtUtils.initProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar, maxRange=progressBarRange, actionTitle="Loading Presets")
        groups = self._gatherSceneGroups(groupList=groupList, progressBar=progressBar)
        presets = self._gatherScenePresets(presetList=presetList, progressBar=progressBar)
        qtUtils.resetProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar)

        if (isinstance(groups, list) and groups is not None):
            for group in groups:
                self.createRootWidget(obj=group)
                
        if (isinstance(presets, list) and presets is not None):
            for preset in presets:
                self.createRootWidget(obj=preset)
                
        ## Expand expanded groups after the refresh
        for groupItem, group in self._groupDict.items():
            if group.identifier in curExpandedGroupsID:
                self.expandItem(groupItem)

        self.loaded = True

    def _gatherSceneGroups(self, groupList=None, progressBar=None):
        groups = []
        if groupList is not None:
            for groupID in groupList:
                g = GroupObject(groupID)
                groups.append(g)
                if progressBar is not None:
                    progressBar.setValue(progressBar.value() + 1)
        return groups

    def _gatherScenePresets(self, presetList= None, progressBar=None):
        presets = []
        if presetList is not None:
            for presetID in presetList:
                p = PresetObject(presetID)
                presets.append(p)
                if progressBar is not None:
                    progressBar.setValue(progressBar.value() + 1)
        return presets

    def createRootWidget(self, obj):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
        qTreeWidget.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable |
                             Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
        self._updateWidget(obj, qTreeWidget)

        if isinstance(obj, GroupObject):
            if obj.optionPreset is not None:
                options = OptionPresetObject(identifier=obj.optionPreset)
            else:
                options = getDefaultExportPresetOptions()

            qTreeWidget.setData(0, Qt.UserRole, obj)
            qTreeWidget.setData(1, Qt.UserRole, options)
            
            self.addTopLevelItem(qTreeWidget)
            self._groupDict[qTreeWidget] = obj

        elif isinstance(obj, PresetObject):
            presetGroupItem = None
            for groupItem, group in self._groupDict.items():
                if group.identifier == obj.group:
                    presetGroupItem = groupItem
                    break

            if presetGroupItem is not None:
                presetGroupItem.addChild(qTreeWidget)
                selectedGroups = self.getSelectedGroups()
                if len(selectedGroups) > 0 and selectedGroups[0].identifier == self._groupDict[groupItem].identifier:
                    # Expand the selected group where we want to add a preset
                    self.expandItem(presetGroupItem)
            else:
                self.addTopLevelItem(qTreeWidget)

            self._rootDict[qTreeWidget] = obj

        return qTreeWidget
    
    def _updateParentingPreset(self, preset, parentItem):
        presetItem = self.getQtPresetItemFromIdentifier(preset.identifier)
        self.changeParent(presetItem, parentItem)

    def _updateWidget(self, obj, qTreeWidget):
        columnIdName = getEnumId(PRESETS_COLUMN.NAME)
        columnIdPath = getEnumId(PRESETS_COLUMN.PATH)
        
        if hasattr(obj, "name") and obj.name != None:
            qTreeWidget.setText(columnIdName, str(obj.name))

        if hasattr(obj, "path") and obj.path != None:
            relativePath = obj.path
            qTreeWidget.setText(columnIdPath, relativePath)

    def _modifyGlobalCheckBox(self):
        selection = self.selectedItems()
        for s in selection:
            hierarchy = self.getQtItemsDescendants(s)
            for child in hierarchy:
                child.setCheckState(0, self._qGlobalCheckBox.checkState())

    def _doubleClickedItem(self, item, column):
        if(column == 1):
            item.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsSelectable |
                          Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        return None

    def _selectionChanged(self):
        return None

    def startEditingItemWithGroupID(self, groupID):
        for groupItem, group in self._groupDict.items():
            if group.identifier == groupID:
                self.setCurrentItem(groupItem)
                self.editItem(groupItem, 0)
                break

    def startEditingSelectedItem(self, columns = [0]):
        items = self.getSelectedQtItems()
        if (len(items) > 0):
            self.startEditingItem(items[0], columns)
    
    def getExpandedGroupsID(self):
        expandedGroupsKeys = set()
        for groupItem, group in self._groupDict.items():
            if groupItem.isExpanded():
                expandedGroupsKeys.add(group.identifier)
        return expandedGroupsKeys

    def getPresetsFromGroup(self,_group):
        presets = []
        for preset in self._rootDict.values():
            if preset.group == _group.identifier:
                presets.append(preset)
        return presets

    def refreshTree(self, progressBar=None, lbProgressBar=None):
        self.loaded = False
        self.createTree(progressBar=progressBar, lbProgressBar=lbProgressBar)

    def filterTree(self, filterName = ""):
        if (filterName != ""):
            for presetItem in self._rootDict.keys():
                if (str.lower(filterName) in str.lower(presetItem.text(0))):
                    presetItem.setHidden(False)
                else:
                    presetItem.setHidden(True)
        else:
            for presetItem in self._rootDict.keys():
                presetItem.setHidden(False)

        for groupItem in self._groupDict.keys():
            hide = self.areAllChildrenHidden(groupItem)
            groupItem.setHidden(hide)
    
    def removeItems(self, presets=[], groups=[]):
        yesAll = False
        for preset in presets:
            if not yesAll:
                popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                    title="Delete Preset ?", 
                    text="Are you sure you want to delete the preset {0}".format(preset.name)
                )
                if popup == QMessageBox.NoToAll:
                    return
                if popup == QMessageBox.YesToAll:
                    yesAll = True
                if popup == QMessageBox.No:
                    continue
            
            presetItem = self.getQtPresetItemFromIdentifier(preset.identifier)
            self.removeItem(presetItem)
            preset.delete()
            try:
                self._rootDict.pop(presetItem)
            except KeyError as exception:
                print("There is no such key : " + exception)

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
            
            groupItem = self.getQtGroupItemFromIdentifier(group.identifier)
            self.removeItem(groupItem)
            group.delete()
            try:
                self._groupDict.pop(groupItem)
            except KeyError as exception:
                print("There is no such key : " + exception)

    #TODO here: add visibleInList option !  
    def getAllPresetsList(self, visibleInList=False):
        return list(self._rootDict.values())

    def getSelectedPresets(self):
        selectedPresets = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            if item not in self._rootDict:
                continue
            preset = self._rootDict[item]
            selectedPresets.append(preset)
        return selectedPresets

    def getSelectedPresetsAndGroupsContent(self, visibleInList=False):
        selectedPresets = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            hierarchy = self.getQtItemsDescendants(item)
            for childItem in hierarchy:
                if childItem not in self._rootDict:
                    continue
                preset = self._rootDict[childItem]
                if preset not in selectedPresets:
                    selectedPresets.append(preset)
        return selectedPresets

    def getSelectedGroups(self):
        selectedGroups = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            if item not in self._groupDict:
                continue
            group = self._groupDict[item]
            selectedGroups.append(group)
        return selectedGroups

    def getCheckedPresets(self, visibleInList=False):
        checkedPresets = []
        for presetItem, preset in self._rootDict.items():
            if presetItem.checkState(0) == Qt.Checked:
                checkedPresets.append(preset)
        return checkedPresets

    def getQtPresetItemFromIdentifier(self, identifier):
        for presetItem, preset in self._rootDict.items():
            if preset.identifier == identifier:
                return presetItem
        return None

    def getQtGroupItemFromIdentifier(self, identifier):
        for groupItem, group in self._groupDict.items():
            if group.identifier == identifier:
                return groupItem
        return None
    
    def getOptionPresetOfQtItem(self, qtItem):
        parent = qtItem.parent()
        optionPreset = None
        if parent is not None:
            group = self._groupDict[parent]
            if group.optionPreset is not None:
                optionPreset = OptionPresetObject(identifier=group.optionPreset)
            else:
                optionPreset = getDefaultExportPresetOptions()
        else:
            optionPreset = getDefaultExportPresetOptions()
        return optionPreset

    def getOptionPresetFromIdentifier(self, identifier):
        qtItem = self.getQtPresetItemFromIdentifier(identifier)
        return self.getOptionPresetOfQtItem(qtItem)

    def joinOptionsToPresets(self, presets):
        """
        Takes a list of preset as input and returns a list of tuple(preset, optionPreset)

        in: list(PresetObject)
        out: list(tuple(PresetObject,OptionPresetObject))
        """
        result = []
        for preset in presets:
            optionPreset = self.getOptionPresetFromIdentifier(preset.identifier)
            result.append((preset, optionPreset))
        return result

    def getSelectedPresetsWithOptions(self, visibleInList=False):
        selectedPresets = self.getSelectedPresetsAndGroupsContent(visibleInList=visibleInList)
        return self.joinOptionsToPresets(selectedPresets)

    def getAllPresetsListWithOption(self, visibleInList=False):
        allPresets = self.getAllPresetsList(visibleInList=visibleInList)
        return self.joinOptionsToPresets(allPresets)

    def getCheckedPresetsWithOptions(self, visibleInList=False):
        checkedPresets = self.getCheckedPresets(visibleInList=visibleInList)
        return self.joinOptionsToPresets(checkedPresets)

    def getPresetsWithOptions(self, exportType = const.EXPORT_OPTION.NONE, visibleInList=False):
        presets = []

        if exportType == const.EXPORT_OPTION.SELECTED:
            presets = self.getSelectedPresetsAndGroupsContent(visibleInList=visibleInList)
        elif exportType == const.EXPORT_OPTION.CHECKED:
            presets = self.getCheckedPresets(visibleInList=visibleInList)
        elif exportType == const.EXPORT_OPTION.ALL:
            presets = self.getAllPresetsList(visibleInList=visibleInList)

        return self.joinOptionsToPresets(presets)
        
    def resfreshQtPresetItemFromID(self, id, obj):
        PresetItem = self.getQtPresetItemFromIdentifier(id)
        self._updateWidget(obj = obj, qTreeWidget = PresetItem)

    def resfreshQtGroupItemFromID(self, id, obj):
        GroupItem = self.getQtGroupItemFromIdentifier(id)
        self._updateWidget(obj = obj, qTreeWidget = GroupItem)