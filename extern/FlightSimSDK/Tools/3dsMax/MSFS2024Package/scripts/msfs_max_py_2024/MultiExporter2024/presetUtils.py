"""
This module contains classes and function to handle preset in the multi exporter.

The presets are stored in the root node of the max scene.
"""

import os
import uuid
import MultiExporter2024.constants as const

from maxsdk_2024.globals import RT, MAXVERSION, MAX2021
from maxsdk_2024 import qtUtils, sceneUtils, userprop, utility
from PySide2.QtWidgets import QMessageBox, QFileDialog

class SerializableObject():
    
    """Stores a string "name" in the root node
    """
    def __init__(self, identifier, listStorage = None):
        self.identifier = identifier
        self.defaultName = "New"
        self.listStorage = "defaultSerializableObjectPool" if listStorage is None else listStorage # const.PROP_PRESET_GROUP_LIST
        self.name = self.defaultName
        self._load()

    def get(self):
        self._load()
        return self.name

    def __hash__(self):
        return self.identifier.__hash__()  # hash(self.identifier)

    def __eq__(self, a):
        if MAXVERSION() < MAX2021:
            if isinstance(a, unicode) or isinstance(a, str):
                return self.identifier == a
        else:
            if isinstance(a, str):
                return self.identifier == a

        if(isinstance(a, PresetObject)):
            return self.identifier == a.identifier
        return False

    def edit(self, name):
        self._load()
        self.name = self.name if name is None else name
        self._write()

    def create(self, name):
        self.name = name
        self._write()

    def delete(self):
        self._load()
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if self.identifier in propList:
            propList.remove(self.identifier)
            userprop.removeUserProp(sceneRoot, self.identifier)
        userprop.setUserPropList(sceneRoot, self.listStorage, propList)

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None:
            if self.identifier in propList:
                preset = userprop.getUserProp(sceneRoot, self.identifier)
                self.name = preset

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        if self.name is None:
            newPreset = self.defaultName
        else:
            newPreset = self.name
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserProp(sceneRoot, self.identifier, newPreset)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)


class OptionPresetObject(SerializableObject):
    """Stores a name and a dictionary in the root node
    """
    def __init__(self, identifier, listStorage=const.PROP_OPTIONS_LIST):
        SerializableObject.__init__(self, identifier, listStorage)
        self.listStorage = listStorage
        self.defaultName = "New Option Preset"
        self.name = self.defaultName
        self.dictionary = None
        self._load()

    def get(self):
        self._load()
        return (self.name, self.dictionary)
        
    def edit(self, name=None, dictionary=None):
        self._load()
        self.name = self.name if name is None else name
        self.dictionary = self.dictionary if dictionary is None else dictionary
        self._write()

    def create(self, name, dictionary={}):
        self.name = name
        self.dictionary = dictionary
        self._write()

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None and self.identifier in propList:
            groupTuple = userprop.getUserPropHeadedDict(sceneRoot, self.identifier)
            if isinstance(groupTuple, tuple):
                self.name = groupTuple[0]
                self.dictionary = groupTuple[1]

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        presetList = list()

        if propList is not None:
            presetList = propList

        if self.name is None:
            self.name = self.defaultName

        newGroup = (self.name, self.dictionary)
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserPropHeadedDict(sceneRoot, self.identifier, newGroup)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)

class GroupObject(SerializableObject):
    """Stores a name and an identifier in the root node
    """
    def __init__(self, identifier, listStorage = const.PROP_PRESET_GROUP_LIST):
        SerializableObject.__init__(self, identifier, listStorage)
        self.listStorage = listStorage
        self.defaultName = "New Group"
        self.name = self.defaultName
        self.path = None
        self.optionPreset = None

        self._load()

    def get(self):
        self._load()
        return (self.name, self.optionPreset, self.path)

    def edit(self, name=None, optionPreset=None, path=None):
        self._load()
        if name is not None:
            self.name = name
        if optionPreset is not None:
            self.optionPreset = optionPreset
        if path is not None:
            self.path = path
        self._write()

    def create(self, name, optionPreset=None, path=None):
        self.name = name
        self.optionPreset = optionPreset
        self.path = path
        self._write()

    def delete(self):
        self._load()
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if self.identifier in propList:
            propList.remove(self.identifier)
            userprop.removeUserProp(sceneRoot, self.identifier)
        userprop.setUserPropList(sceneRoot, self.listStorage, propList)

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None:
            if self.identifier in propList:
                preset = userprop.getUserPropList(sceneRoot, self.identifier)
                if len(preset) > const.PROP_GROUP_PARAM_NAME_ID:
                    self.name = preset[const.PROP_GROUP_PARAM_NAME_ID]
                if len(preset) > const.PROP_GROUP_PARAM_PATH_ID:
                    self.path = preset[const.PROP_GROUP_PARAM_PATH_ID]
                if len(preset) > const.PROP_GROUP_PARAM_OPTION_ID:
                    self.optionPreset = preset[const.PROP_GROUP_PARAM_OPTION_ID]
                

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        newGroup = []
        newGroup.insert(const.PROP_GROUP_PARAM_NAME_ID, 
                        str(self.defaultName) if self.name is None else str(self.name))
        newGroup.insert(const.PROP_GROUP_PARAM_PATH_ID,
                         "" if self.path is None else self.path)
        newGroup.insert(const.PROP_GROUP_PARAM_OPTION_ID,
                         None if self.optionPreset is None else self.optionPreset)
        

        if self.identifier not in presetList:
            presetList.append(self.identifier)

        userprop.setUserPropList(sceneRoot, self.identifier, newGroup)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)


class PresetObject(SerializableObject):
    """Stores a name, a group identifier, a path and a list of layer names in the root node
    """
    def __init__(self, identifier, listStorage = const.PROP_PRESET_LIST):
        self.identifier = identifier
        self.listStorage = listStorage
        self.defaultName = "New Preset"
        self.name = self.defaultName
        self.group = None
        self.path = None
        self.layerNames = []
        self._load()
    
    def get(self):
        self._load()
        return (self.name,self.group,self.path,self.layerNames)

    def edit(self, name=None, group=None, path=None, layerNames=None):
        self._load()
        self.name = name if name is not None else self.name
        self.group = group if group is not None else self.group
        self.path = path if path is not None else self.path
        self.layerNames = layerNames if layerNames is not None else self.layerNames
        self._write()

    def create(self, name, group, path, layerNames=[]):
        self.name = name
        self.group = group
        self.path = path
        self.layerNames = layerNames
        self._write()

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None and self.identifier in propList:
            preset = userprop.getUserPropList(sceneRoot, self.identifier)
            if len(preset) > const.PROP_PRESET_PARAM_NAME_ID:
                self.name = preset[const.PROP_PRESET_PARAM_NAME_ID]
            if len(preset) > const.PROP_PRESET_PARAM_GROUP_ID:
                self.group = preset[const.PROP_PRESET_PARAM_GROUP_ID]
            if len(preset) > const.PROP_PRESET_PARAM_PATH_ID:
                self.path = preset[const.PROP_PRESET_PARAM_PATH_ID]
            if len(preset) > const.PROP_PRESET_PARAM_OFFSET:    
                self.layerNames = preset[const.PROP_PRESET_PARAM_OFFSET: len(preset)]

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        newPreset = []
        newPreset.insert(const.PROP_PRESET_PARAM_NAME_ID, str(self.defaultName) if self.name is None else str(self.name))
        newPreset.insert(const.PROP_PRESET_PARAM_GROUP_ID, "-" if self.group is None else self.group)
        newPreset.insert(const.PROP_PRESET_PARAM_PATH_ID, ".\\" if self.path is None else self.path)
        for layer in self.layerNames:
            newPreset.append(layer)
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserPropList(sceneRoot, self.identifier, newPreset)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)


def getDefaultExportPresetOptions():
    defaultPresetId = None
    optionPreset = None

    sceneRoot = sceneUtils.getSceneRootNode()
    optionPresetList = userprop.getUserPropList(sceneRoot, const.PROP_OPTIONS_LIST)
    
    if len(optionPresetList) > 0:
        defaultPresetId = optionPresetList[0]

    if defaultPresetId is not None:
        optionPreset = OptionPresetObject(defaultPresetId)

    return optionPreset

# PRESET AND PRESET GROUP UTILITY
def createNewPreset(labelName=None, group=None, filePath=None, layerNames=None, identifier=None):
    """
    Creates a new preset, writes it to the root node and return a reference to the PresetObject Wrapper

    \nin:
    labelName=str
    group=str : GroupObject.identifier
    filePath=str
    layerNames=list(str)

    \nout:
    PresetObject
    """
    presetID = identifier
    if presetID is None:     
        presetHash = uuid.uuid4()
        presetID = const.PROP_PRESET_ENTRY_PREFIX.format(presetHash)
    storage = const.PROP_PRESET_LIST
    preset = PresetObject(presetID, storage)
    preset.create(name=labelName,group=group, path=filePath, layerNames=[] if layerNames is None else layerNames)
    return preset


def createNewGroup(groupName=None,optionPreset=None, filePath=None, identifier=None):
    """
    Creates a new preset group, writes it to the root node and return a reference to the GroupObject Wrapper

    \nin:
    groupName=str
    optionPreset=str : OptionPresetObject.identifier

    \nout:
    GroupObject
    """
    groupID = identifier
    if groupID is None:
        groupHash = uuid.uuid4()
        groupID = const.PROP_PRESET_GROUP_ENTRY_PREFIX.format(groupHash)
    storage = const.PROP_PRESET_GROUP_LIST
    group = GroupObject(groupID, storage)
    group.create(name=groupName,optionPreset=optionPreset, path=filePath)
    return group


def confirmAndRemove(groups=[], presets=[], refreshFunc=None, prompt=True):
    """Opens a dialog to confirm the user wants to delete passed groups and presets.
    """
    passAll = False
    if (prompt == False):
        passAll = True

    for preset in presets:
        if (passAll == False):
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Delete Preset ?", text="Are you sure you want to delete the preset {0}".format(preset.name))
            if popup == QMessageBox.NoToAll:
                return
            if popup == QMessageBox.YesToAll:
                passAll = True
            if popup == QMessageBox.No:
                continue
        preset.delete()
        if refreshFunc is not None:
            refreshFunc()
    for group in groups:
        if (passAll == False):
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Delete Group ?", text="Are you sure you want to delete the group {0}".format(group.name))
            if popup == QMessageBox.NoToAll:
                return
            if popup == QMessageBox.YesToAll:
                passAll = True
            if popup == QMessageBox.No:
                continue
        group.delete()
        if refreshFunc is not None:
            refreshFunc()


def getExportPath(presetID):
    rootNode = sceneUtils.getSceneRootNode()
    presetParam = userprop.getUserPropList(rootNode, presetID)
    return presetParam[const.PROP_PRESET_PARAM_PATH_ID]


def getAbsoluteExportPath(preset):
    expPath = preset.path
    if expPath is None:
        return None

    assetFilePath = utility.convertRelativePathToAbsolute(expPath, RT.pathConfig.getCurrentProjectFolder())
    if not os.path.exists(os.path.dirname(assetFilePath)):
        assetFilePath = utility.convertRelativePathToAbsolute(expPath, RT.maxFilePath)
        
    return assetFilePath

def addExportPathToPresets(presets):
    for preset in presets:
        initDir = os.path.split(getAbsoluteExportPath(preset))[0]
        expPath = askForNewPathToPresets("Export Path for {}".format(preset.name), initDir=initDir)
        if(expPath != None):
            expPath = utility.convertAbsolutePathToRelative(
            expPath, RT.pathConfig.getCurrentProjectFolder())
            preset.edit(path=expPath)

def changeExportPathForPresets(presets):
    for preset in presets:
        expPath = preset.path
        initDir = os.path.dirname(getAbsoluteExportPath(preset))

        expPath = askForNewDirectoryPath("Export Path for {}".format(preset.name), initDir=initDir)
        if expPath is None:
            continue

        if expPath == "":
            continue

        expPath = utility.convertAbsolutePathToRelative(expPath, RT.pathConfig.getCurrentProjectFolder())
        expPath += '\\' + preset.name + '.gltf'
        preset.edit(path=expPath, name=preset.name)

        return expPath

def addExportPathToGroups(groups):
    for group in groups:
        expPath = group.path
        initDir = os.path.dirname(getAbsoluteExportPath(group)) if group.path is not None else RT.pathConfig.getCurrentProjectFolder()
            
        expPath = askForNewDirectoryPath("Export Path for {}".format(group.name), initDir=initDir)
        if expPath is None:
            continue

        if expPath == "":
            continue

        expPath = utility.convertAbsolutePathToRelative(expPath, RT.pathConfig.getCurrentProjectFolder())
        group.edit(path=expPath)


def askForExistingPath(title="", initDir=""):
    """Opens a dialog to get a existing file paths from the user
    """
    if initDir == None :
        initDir = ""

    initDir = utility.convertRelativePathToAbsolute(initDir, RT.pathConfig.getCurrentProjectFolder())
    expPaths = qtUtils.openSaveFileNamesDialog(caption=title,  _filter="GLTF(*.gltf)", _dir=initDir)
    return expPaths

def askForCustomSavePath(title="", initDir="", fileMode=QFileDialog.FileMode.AnyFile, relative=False):
    """Opens a dialog to get custom file path
    """
    if initDir == None :
        initDir = ""

    initDir = utility.convertRelativePathToAbsolute(initDir, RT.pathConfig.getCurrentProjectFolder())
    acceptMode = QFileDialog.AcceptOpen.AcceptSave
    if fileMode == QFileDialog.FileMode.ExistingFiles:
        # This is poorly made, thanks to Qt
        acceptMode = QFileDialog.AcceptOpen.AcceptOpen
    filePaths = qtUtils.openCustomFileNamesDialog(caption=title,  _filter="GLTF(*.gltf)", _dir=initDir, fileMode=fileMode, acceptMode=acceptMode)

    if filePaths == None:
        return None
    
    if relative:
        for i in range(len(filePaths)-1, -1, -1):
            if filePaths[i] == None:
                filePaths.pop(i)
            else:
                filePaths[i] = utility.convertAbsolutePathToRelative(filePaths[i], RT.pathConfig.getCurrentProjectFolder())
                if filePaths[i] == ".":
                    filePaths.pop(i)
    else:
        for i in range(len(filePaths)-1, -1, -1):
            if filePaths[i] == None or filePaths[i] == "":
                filePaths.pop(i)
    
    if (fileMode == QFileDialog.FileMode.ExistingFiles):
        return filePaths
    return filePaths[0]

def askForNewDirectoryPath(title="", initDir=""):
    """Opens a dialog to get a new directory path from the user
    """
    if initDir is None :
        initDir = ""

    initDir = utility.convertRelativePathToAbsolute(initDir, RT.pathConfig.getCurrentProjectFolder())
    expPath = qtUtils.openSaveFolderPathDialog(_caption=title,  _dir=initDir)
    return expPath


def askForNewPathToPresets(title="", initDir=""):
    """Opens a dialog to get a new file path from the user
    """
    if initDir is None :
        initDir = ""

    initDir = utility.convertRelativePathToAbsolute(initDir, RT.pathConfig.getCurrentProjectFolder())
    expPath = qtUtils.newFile(_caption=title, _dir=initDir, _filter="(*.gltf)")
    
    if expPath is not None:
        expPath = utility.convertAbsolutePathToRelative(expPath, RT.pathConfig.getCurrentProjectFolder())

    return expPath
