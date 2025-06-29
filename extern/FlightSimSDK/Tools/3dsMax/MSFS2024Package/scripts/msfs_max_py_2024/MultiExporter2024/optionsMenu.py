"""This module handles the option panel of the multi exporter.

It is connected to the BabylonPYMXS2024 and babylon exporter as it is getting default values for the fields from it. It is possible to run this option menu outside the context of the mutli exporter
"""
import os
import uuid

import MultiExporter2024.ui.settingsWindow_ui as settingsWindowUI

import MultiExporter2024.constants as const
import MultiExporter2024.presetUtils as presetUtils
import MultiExporter2024.BabylonPYMXS2024 as babylonPYMXS2024

from MultiExporter2024.presetUtils import GroupObject

from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (QComboBox, QDialog, QWidget, 
                               QCheckBox, QGroupBox, QLineEdit
                               )

from maxsdk_2024 import qtUtils, sceneUtils, userprop, utility
from maxsdk_2024.globals import RT

APPLY_UPTODATE = "Save"
APPLY_OUTDATED = "Save*"

class ComboBoxOptionPreset(QComboBox):
    """
    QComboBox to handle OptionPreset. 

    \nComboBoxOptionPreset will read, create and store the OptionPreset in the root node of the scene.
    \nIf no option preset are already stored in the scene then intanciating a ComboBoxOptionPreset will set it up.
    """    
    onModifiedData = Signal()

    def __init__(self, menu, parent):
        """
        \nin:
        menu=OptionsMenu
        parent=QWidget
        """
        QComboBox.__init__(self, parent)
        self.menu = menu
        self.presetObjectList = []
        self._intializeContent()
        self.currentIndexChanged.connect(lambda i: self._changedIndex(i))
        self.setEditable(True)
        self.liEd = self.lineEdit()
        self.liEd.editingFinished.connect(self._renamedCurrentOptionPreset)
        self.setInsertPolicy(self.NoInsert)
        self.oldIndex = 0

    def _getInfoByIdentifier(self, identifier):
        for i,presetObj in enumerate(self.presetObjectList):
            if presetObj.identifier == identifier:
                return (i,presetObj)
        return None
    def getOptionPresetByIdentifier(self, identifier):
        try:
            return self._getInfoByIdentifier(identifier)[1]
        except TypeError:
            return None

    def getOptionPresetIndexByIdentifier(self, identifier):
        try:
            return self._getInfoByIdentifier(identifier)[0]
        except TypeError:
            return None            

    def focusOutEvent(self, focusEvent):
        if self.menu is not None:
            if self.menu.madeChanges == True:
                self.hidePopup()               
            else:
                focusEvent.accept()
            return
        else:
            QComboBox.focusOutEvent(self,focusEvent)


    def wheelEvent(self, wheelEvent):
        if self.menu is None:
            return
        if self.menu.madeChanges == True:
            wheelEvent.ignore()
            return
        QComboBox.wheelEvent(self,wheelEvent)

    def updatePreset(self,index,newDict):
        self.presetObjectList[index].edit(dictionary=newDict)        

    def _intializeContent(self):
        self.clear()
        self.presetObjectList = []

        optionPresetList = userprop.getUserPropList(sceneUtils.getSceneRootNode(), const.PROP_OPTIONS_LIST)

        if optionPresetList is None:
            optionPresetList = list()

        if len(optionPresetList) > 0:
            defaultPresetId = optionPresetList[0]
        else:
            defaultPresetId = const.PROP_OPTIONS_ENTRY_PREFIX.format(uuid.uuid4())

        defaultPreset = presetUtils.OptionPresetObject(defaultPresetId, listStorage=const.PROP_OPTIONS_LIST)
        defaultPreset.create("default", getCurrentSettingsAsDict())

        self.presetObjectList.append(defaultPreset)

        for i in range(1, len(optionPresetList)):
            option = optionPresetList[i]
            optionPreset = presetUtils.OptionPresetObject(option, const.PROP_OPTIONS_LIST)
            self.presetObjectList.append(optionPreset)  

        for item in self.presetObjectList:
            self.addItem(item.name, item)

    def refresh(self):
        self._intializeContent()

    def addOptionPreset(self):
        name = "NewOptionPreset" + str(self.count() - 1)
        presetId = const.PROP_OPTIONS_ENTRY_PREFIX.format(uuid.uuid4())
        preset = presetUtils.OptionPresetObject(presetId, listStorage=const.PROP_OPTIONS_LIST)        
        preset.create(name, getCurrentSettingsAsDict())
        self.presetObjectList.append(preset)
        self.addItem(preset.name, preset)
        self.setCurrentIndex(self.count() - 1)
        self.onModifiedData.emit()

    def removeOptionPreset(self):
        curIndex = self.currentIndex()

        if (len(self.presetObjectList) > 0 and curIndex > 0): # if list is not empty and item != default
            
            optionPresetList = userprop.getUserPropList(
            sceneUtils.getSceneRootNode(), const.PROP_OPTIONS_LIST)

            ## update option preset for the removed option preset and set it to default
            groupList = userprop.getUserPropList(sceneUtils.getSceneRootNode(), const.PROP_PRESET_GROUP_LIST)
            groups = []
            if groupList is not None:
                for groupID in groupList:
                    g = GroupObject(groupID)
                    groups.append(g)
                    
            optionPreset = self.itemData(curIndex)
            for i in range (0, len(groups)):
                if(groups[i].optionPreset == optionPreset.identifier):
                    groups[i].edit(optionPreset= optionPresetList[0])
            
                    
            ## pop option preset from the saved option preset list and the items            
            optionPresetList.pop(curIndex)
            userprop.setUserPropList(sceneUtils.getSceneRootNode(), const.PROP_OPTIONS_LIST, optionPresetList)

            self.presetObjectList.pop(curIndex)
            self.removeItem(curIndex)
            self.onModifiedData.emit()
    
    def _renamedCurrentOptionPreset(self):
        currentID = self.currentIndex()
        if (currentID != 0):
            newName = userprop.cleanupStringForPropListStorage(self.liEd.text())
            self.setItemText(currentID, newName)
            current = self.itemData(currentID)
            current.edit(name=newName)
            self.onModifiedData.emit()

    def _changedIndex(self, index):
        pass


class OptionsMenu(QDialog, settingsWindowUI.Ui_settingsWindow):
    """
    QWidget to handle Babylon parameters.
    This widget is an option menu window for the multi exporter, though it stands alone and can read and set babylon export settings.
    \nSignal :
    onClosed : emits when the window is closed
    onModifiedData : emits when the settings change or an option preset is created/renamed. 
    """
    onClosed = Signal()
    onModifiedData = Signal()

    currentTab = None

    def __init__(self,parent=QWidget.find(RT.windows.getMAXHWND())):
        QDialog.__init__(self,parent)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove help button from title bar
        self.setupUi(self)

        self.btnSave.pressed.connect(lambda: self.saveSettings())
        self.btnSave.setText(APPLY_UPTODATE)
        self.btnCancel.pressed.connect(lambda: self.close())
        self.madeChanges = False

        # PRESET BUTTONS
        self.btnAddOptionPreset.clicked.connect(self._clickedAddOptionPreset)
        self.btnRemoveOptionPreset.clicked.connect(self._clickedRemoveOptionPreset)

        self.btnBrowseTexture.clicked.connect(self._browseTexturePath)

        self.cbFlattenNodes.stateChanged.connect(self._changeCheckboxFlattenNodes)
        self.cbKeepInstances.stateChanged.connect(self._changeCheckboxKeepInstances)
        #Add parameters at the end of the list if needed
        
        self.widgetToProperty = {
            self.cbAutosave: "babylonjs_autosave",
            self.cbExportHidden: "babylonjs_exporthidden",
            self.cbSelectionAsSubmodel : "flightsim_exportAsSubmodel",
            self.cbRemoveLODPrefix: "flightsim_removelodprefix",
            self.cbExportMaterials: "babylonjs_export_materials",
            self.gbUsePreExport: "babylonjs_preproces",
            self.cbMergeContainers: "babylonjs_mergecontainersandxref",
            self.cbApplyPreprocessToScene: "babylonjs_applyPreprocess",
            self.cbAsoboUniqueID: "flightsim_asb_unique_id",
            self.gbTextures: "babylonjs_writetextures",
            self.cbKeepInstances: "flightsim_keepInstances",
            self.cbFlattenNodes: "flightsim_flattenNodes"
        }

        # in case there is different behaviours to have for a same QWidget put the second case in here and implement it further down :
        self.specialWidgetToProperty = {
            self.lineTexturePath: "textureFolderPathProperty"
        }

        # enum based (comboBox) cases (this is to be able to change UI frontend names without breaking backend)
        # need same keys in the 3 following dicts
        self.enumBasedWidgetToProperty = {
            self.comboBakeAnimationOptions: "babylonjs_bakeAnimationsType",
            self.comboAnimationExport: "babylonjs_export_animations_type"
        }
        self.enumBasedWidgetWriteType = {
            self.comboBakeAnimationOptions: babylonPYMXS2024.WRITE_TYPE.INDEX,
            self.comboAnimationExport: babylonPYMXS2024.WRITE_TYPE.NAME
        }
        self.enumBasedWidgetEnum = {
            self.comboBakeAnimationOptions: babylonPYMXS2024.BakeAnimationType,
            self.comboAnimationExport: babylonPYMXS2024.AnimationExportType
        }

        self.initializeWidgets()

        widgets = list(self.widgetToProperty.keys()) + list(self.specialWidgetToProperty.keys()) + list(self.enumBasedWidgetToProperty.keys())

        for widget in widgets:
            signal = None
            if(isinstance(widget, QCheckBox)):
                signal = widget.stateChanged
            elif (isinstance(widget, QGroupBox)):
                signal = widget.toggled
            elif (isinstance(widget, QComboBox)):
                signal = widget.activated
            elif (isinstance(widget, QLineEdit)):
                signal = widget.textEdited
            else:
                continue
            signal.connect(lambda: self.changedOption())

        # PRESET COMBO
        presetCombo = ComboBoxOptionPreset(self,self)
        presetCombo.setFixedSize(self.comboOptionPreset.size())
        presetCombo.setEditable(True)
        self.horizontalLayout_8.removeWidget(self.comboOptionPreset)
        self.comboOptionPreset.setHidden(True)
        self.comboOptionPreset = presetCombo
        self.comboOptionPreset.activated.connect(lambda i: self.changedActivePreset(i))
        self.comboOptionPreset.onModifiedData.connect(self.onModifiedData.emit)
        self.horizontalLayout_8.insertWidget(1, self.comboOptionPreset)

    def _adjustUI(self):
        self._adjustUIcbKeepInstances()
        
    def _adjustUIcbKeepInstances(self):
        if self.cbFlattenNodes.checkState() == Qt.Checked:
            self.cbKeepInstances.setChecked(False)
    
    def _initUIPanelSpecifics(self):
        hideForPresetsPanel = (bool)(self.currentTab == const.TAB.PRESETS)
        self.cbFlattenNodes.setHidden(hideForPresetsPanel)

    def _adjustUIcbFlattenNodes(self):
        if self.cbKeepInstances.checkState() == Qt.Checked:
            self.cbFlattenNodes.setChecked(False)

    def _browseTexturePath(self):
        texturePath = os.path.join(RT.pathConfig.getCurrentProjectFolder(), self.lineTexturePath.text())
        path = RT.getSavePath(caption="Export Path", initialDir=texturePath)
        if (path is None):
            return
        path = utility.convertAbsolutePathToRelative(path, RT.pathConfig.getCurrentProjectFolder())
        self.lineTexturePath.setText(path)
        self.lineTexturePath.textEdited.emit("")

    def _clickedAddOptionPreset(self):
        self.comboOptionPreset.addOptionPreset()

    def _clickedRemoveOptionPreset(self):
        self.comboOptionPreset.removeOptionPreset()
        
    def _changeCheckboxFlattenNodes(self):
        self._adjustUIcbKeepInstances()

    def _changeCheckboxKeepInstances(self):
        self._adjustUIcbFlattenNodes()

    def changedOption(self):
        self.madeChanges = True
        self.btnSave.setText(APPLY_OUTDATED)

    def appliedOption(self):
        self.madeChanges = False
        self.btnSave.setText(APPLY_UPTODATE)

    def tryClosing(self):
        if not self.madeChanges:
            return
        popup = qtUtils.popup_Yes_No(
            title="Unapplied changes",
            text="You have unapplied changes, do you want to save them?"
        )
        if popup == True:
            self.saveSettings()

    def saveAndQuit(self):
        self.saveSettings()
        self.onModifiedData.emit()

        self.close()

    def closeEvent(self, event):
        self.tryClosing()
        self.onClosed.emit()
        event.accept()
            
    def changedActivePreset(self, index):
        preset = self.comboOptionPreset.presetObjectList[index]
        self.initializeWidgets(preset.dictionary)
        self.onModifiedData.emit()


    def initializeWidgets(self, dictObj=None):
        """
        Initialize each widgets in the option menu by doing this:
        - Get corresponding UserProperty of a widget in the self.widgetToProperty dictionary
        - Using this userProperty get the value in the input dictObj.
        - if it isn't in the dictObj look in the root node
        - if it isn't stored in the root then get the default value from BabylonPYMXS2024
        - if it isn't in BabylonPYMXS2024 default values use the type default (False, 0, 0.0, "")
        - finally set this value in the widget

        \nin:
        dictObj=dict[str] var
        """
        sceneRoot = sceneUtils.getSceneRootNode()
        for widget, prop in self.widgetToProperty.items():
            state = None

            if dictObj is not None and prop in dictObj:
                state = dictObj[prop]   

            if state is None:
                state = userprop.getUserProp(sceneRoot, prop)

            #INITIALIZE
            if state is None:
                state = babylonPYMXS2024.getPropertyDefaultValue(prop)

            if isinstance(widget, QCheckBox):
                widget.setCheckState(Qt.Checked if state else Qt.Unchecked)

            elif isinstance(widget, QGroupBox):
                if state is None:
                    state = False
                widget.setChecked(state)

            elif isinstance(widget, QComboBox):
                if state is None:
                    state = 0
                widget.setCurrentIndex(state)

            elif isinstance(widget, QLineEdit):
                widget.setText(str(state))

        for widget, prop in self.specialWidgetToProperty.items():
            state = userprop.getUserProp(sceneRoot, prop)

            #INITIALIZE
            if dictObj is not None and prop in dictObj:
                state = dictObj[prop] 

            if state is None:
                state = babylonPYMXS2024.getPropertyDefaultValue(prop)

            if isinstance(widget, QComboBox):
                if state is None:
                    state = widget.itemText(0)
                widget.setCurrentText(state)

            if isinstance(widget, QLineEdit):
                if state is None:
                    state = widget.text()
                widget.setText(state)

        for widget, prop in self.enumBasedWidgetToProperty.items():
            state = userprop.getUserProp(sceneRoot, prop)

            #INITIALIZE
            if dictObj is not None and prop in dictObj:
                state = dictObj[prop]    

            if state is None:
                state = babylonPYMXS2024.getPropertyDefaultValue(prop)

            if state is None:
                widget.setCurrentIndex(-1)
            else:
                index = state #writeType == WRITE_TYPE.INDEX
                writeType = self.enumBasedWidgetWriteType[widget]
                if writeType == babylonPYMXS2024.WRITE_TYPE.NAME:
                    enum = self.enumBasedWidgetEnum[widget]
                    state.replace(" ", "")
                    index = enum[state].value if enum.has_value(state) else -1

                widget.setCurrentIndex(index)

        self._adjustUI()
        self.appliedOption()

    def saveSettings(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        newSettings = dict()
        currentPresetIndex = self.comboOptionPreset.currentIndex()
        for widget, prop in self.widgetToProperty.items():
            if (isinstance(widget, QCheckBox)):
                state = True if widget.checkState() == Qt.Checked else False
            elif (isinstance(widget, QGroupBox)):
                state = widget.isChecked()
            elif (isinstance(widget, QComboBox)):
                state = widget.currentIndex()
            elif (isinstance(widget, QLineEdit)):
                state = widget.text()
            if currentPresetIndex == 0:
                userprop.setUserProp(sceneRoot, prop, str(state))
            newSettings[prop] = state

        for widget, prop in self.specialWidgetToProperty.items():
            if (isinstance(widget, QComboBox)):
                state = widget.currentText()
            if (isinstance(widget, QLineEdit)):
                state = widget.text()
            if currentPresetIndex == 0:
                userprop.setUserProp(sceneRoot, prop, state)
            newSettings[prop] = state

        for widget, prop in self.enumBasedWidgetToProperty.items():
            writeType = self.enumBasedWidgetWriteType[widget]
            index = widget.currentIndex()
            state = index #writeType == WRITE_TYPE.INDEX
            if writeType == babylonPYMXS2024.WRITE_TYPE.NAME:
                enum = self.enumBasedWidgetEnum[widget]
                try:
                    state = enum(index).name
                except TypeError:
                    state = babylonPYMXS2024.getPropertyDefaultValue(prop)
            if currentPresetIndex == 0:
                userprop.setUserProp(sceneRoot, prop, state)
            newSettings[prop] = state
            

        self.comboOptionPreset.updatePreset(currentPresetIndex, newSettings)
        self.btnSave.setText(APPLY_UPTODATE)
        self.madeChanges = False
        self.onModifiedData.emit()

def getCurrentSettingsAsDict():
    """
    Returns the current babylon parameters saved in the root node as a dict

    \nout:
    dictionary  key: pymxs user property string 
                value: var
    """
    sceneRoot = sceneUtils.getSceneRootNode()
    newDict = dict()
    for val in babylonPYMXS2024.babylonParameters:
        newDict[val] = userprop.getUserProp(sceneRoot, val)
    return newDict
