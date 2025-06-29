import uuid
import os

from TextureTool2024 import constants as const
from pymxs import runtime as rt

from maxsdk_2024 import qtUtils, sceneUtils, userprop, utility
from maxsdk_2024.globals import *

from .TextureLib.BitmapConfig import BitmapConfig

class SerializableObject():
    """Stores a string "name" in the root node
    """
    def __init__(self, identifier, listStorage = None):
        self.identifier = identifier
        self.defaultName = "New"
        self.listStorage = "defaultSerializableObjectPool" if listStorage is None else listStorage
        self.name = None
        self._load()

    def __hash__(self):
        return self.identifier.__hash__()  # hash(self.identifier)

    def __eq__(self, a):
        if MAXVERSION() < MAX2021:
            if isinstance(a, unicode) or isinstance(a, str):
                return self.identifier == a
        else:
            if isinstance(a, str):
                return self.identifier == a

        if(isinstance(a, TextureObject)):
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
            textureList = propList
        if self.name is None:
            newTexture = self.defaultName
        else:
            newTexture = self.name
        if self.identifier not in textureList:
            textureList.append(self.identifier)
        userprop.setUserProp(sceneRoot, self.identifier, newTexture)
        userprop.setUserPropList(sceneRoot, self.listStorage, textureList)

class TextureObject(SerializableObject):
    """
        Stores a name, a path identifier and a list of flags in the root node
    """
    def __init__(self, identifier, listStorage = const.PROP_TEXTURE_LIST, sceneRoot = None, propList = None):
        self.identifier = identifier
        self.listStorage = listStorage
        self.defaultName = "New Texture"
        self.name = None
        self.path = None
        self.flags = []
        self.config = None
        self.groupID = None
        self._load(sceneRoot=sceneRoot, propList=propList)
    
    def edit(self, name = None, path = None, flags=[], config = None, groupID = None, sceneRoot = None, propList = None):
        self._load(sceneRoot=sceneRoot, propList=propList)
        self.name = self.name if name is None else name
        self.path = self.path if path is None else path
        self.flags = self.flags if len(flags) <= 0 else flags
        self.config = self.config if config is None else config
        self.groupID = self.groupID if groupID is None else groupID
        self._write(sceneRoot=sceneRoot, propList=propList)
        
    def create(self, name, path, flags = [], config = None, groupID = None, sceneRoot = None, propList = None):
        self.name = name
        self.path = path
        self.flags = flags
        self.config = config
        self.groupID = groupID
        self._write(sceneRoot=sceneRoot, propList=propList)
    
    def _load(self, sceneRoot = None, propList = None):
        if sceneRoot is None:
            sceneRoot = sceneUtils.getSceneRootNode() 

        if propList is None:
            propList = userprop.getUserPropList(sceneRoot, self.listStorage)
            if propList is None:
                return

        if self.identifier not in propList:
            return

        texture = userprop.getUserPropList(sceneRoot, self.identifier)
        if texture is None:
            return

        self.name = texture[const.PROP_TEXTURE_PARAM_NAME_ID] if len(texture) > 0 else None
        self.path = texture[const.PROP_TEXTURE_PARAM_PATH_ID] if len(texture) > 1 else None
        self.groupID = texture[const.PROP_TEXTURE_PARAM_GROUP_ID] if len(texture) > 2 else None
        
        forcenoalpha = texture[const.PROP_TEXTURE_PARAM_FORCENOALPHA_ID] if len(texture) > 3 else False
        forcenoalpha = True if forcenoalpha == "True" else False
        
        materialbitmap = texture[const.PROP_TEXTURE_PARAM_MATERIALBITMAP_ID] if len(texture) > 4 else 0
        if materialbitmap is not None:
            try:
                materialbitmap = int(materialbitmap)
                self.config = BitmapConfig(materialbitmap, "", forcenoalpha)
            except:
                print("Type conversion incorrect")
        else:
            self.config = None
            
        self.flags = texture[const.PROP_TEXTURE_PARAM_OFFSET: len(texture)] if len(texture) > 5 else []
                
    def _write(self, sceneRoot = None, propList = None):
        if sceneRoot is None:
            sceneRoot = sceneUtils.getSceneRootNode()

        if propList is None:
            propList = userprop.getUserPropList(sceneRoot, self.listStorage)

        if propList is None:
            propList = list()

        newTexture = []
        newTexture.insert(const.PROP_TEXTURE_PARAM_NAME_ID, 
                         str(self.defaultName) if self.name is None else str(self.name))
        newTexture.insert(const.PROP_TEXTURE_PARAM_PATH_ID,
                         ".\\" if self.path is None else self.path)
        newTexture.insert(const.PROP_TEXTURE_PARAM_GROUP_ID,
                         "-" if self.groupID is None else self.groupID)
        newTexture.insert(const.PROP_TEXTURE_PARAM_FORCENOALPHA_ID,
                        "False" if self.config is None else str(self.config.forceNoAlpha) if self.config.forceNoAlpha is not None else "False")
        newTexture.insert(const.PROP_TEXTURE_PARAM_MATERIALBITMAP_ID,
                        "0" if self.config is None else str(self.config.materialBitmap) if self.config.materialBitmap is not None else "0")
        
        for flag in self.flags:
            newTexture.append(flag)
            
        if self.identifier not in propList:
            propList.append(self.identifier)

        userprop.setUserPropList(sceneRoot, self.identifier, newTexture)
        userprop.setUserPropList(sceneRoot, self.listStorage, propList)

class GroupObject(SerializableObject):
    """
        Stores a name and a list of flags in the root node
    """
    def __init__(self, identifier, listStorage = const.PROP_TEXTURE_GROUP_LIST, sceneRoot = None, propList = None):
        self.identifier = identifier
        self.listStorage = listStorage
        self.defaultName = "New Group"
        self.name = None
        self.flags = []
        self._load(sceneRoot=sceneRoot, propList=propList)
    
    def edit(self, name = None, flags = [], sceneRoot = None, propList = None):
        self._load(sceneRoot, propList)
        self.name = self.name if name is None else name
        self.flags = self.flags if len(flags) <= 0 else flags
        self._write(sceneRoot=sceneRoot, propList=propList)
        
    def create(self, name = None, flags = [], sceneRoot = None, propList = None):
        self.name = name
        self.flags = flags
        self._write(sceneRoot=sceneRoot, propList=propList)
    
    def _load(self, sceneRoot = None, propList = None):
        if sceneRoot is None:
            sceneRoot = sceneUtils.getSceneRootNode()

        if propList is None:
            propList = userprop.getUserPropList(sceneRoot, self.listStorage)

        if propList is None:
            return

        if self.identifier in propList:
            group = userprop.getUserPropList(sceneRoot, self.identifier)
            self.name = group[const.PROP_TEXTURE_GROUP_PARAM_NAME_ID] if len(group) > 0 else None
            self.flags = group[const.PROP_TEXTURE_GROUP_PARAM_OFFSET: len(group)] if len(group) > 2 else []
                
    def _write(self, sceneRoot = None, propList = None):
        if sceneRoot is None:
            sceneRoot = sceneUtils.getSceneRootNode()
        if propList is None:
            propList = userprop.getUserPropList(sceneRoot, self.listStorage)

        if propList is None:
            propList = list()

        newGroup = []
        newGroup.insert(const.PROP_TEXTURE_GROUP_PARAM_NAME_ID, str(self.defaultName) if self.name is None else str(self.name))

        for flag in self.flags:
            newGroup.append(flag)
            
        if self.identifier not in propList:
            propList.append(self.identifier)

        userprop.setUserPropList(sceneRoot, self.identifier, newGroup)
        userprop.setUserPropList(sceneRoot, self.listStorage, propList)
        
def createNewTexture(labelName = None, filePath = None, flags = None, groupID = None, config = None, sceneRoot = None, textureList = None):
    """
    Creates a new texture, writes it to the root node and return a reference to the textureObject Wrapper

    \nin:
    labelName=str
    filePath=str
    flags=list[str]
    groupID=str
    config=BitmapObject

    \nout:
    textureObject
    """
    textureID = uuid.uuid4()      
    textureName = const.PROP_TEXTURE_ENTRY_PREFIX.format(textureID)
    storage = const.PROP_TEXTURE_LIST
    texture = TextureObject(textureName, storage)
    texture.create(
        name = labelName, 
        path = filePath, 
        flags = [] if flags is None else flags, 
        config = None if config is None else config,
        groupID = None if groupID is None else groupID,
        sceneRoot=sceneRoot,
        propList=textureList
    )
    return texture

def createNewGroup(labelName=None, flags=None, sceneRoot = None, groupList = None):
    """
    Creates a new group, writes it to the root node and return a reference to the groupObject Wrapper

    \nin:
    labelName=str
    flags=list[str]
    config = BitmapObject

    \nout:
    groupObject
    """
    groupID = uuid.uuid4()      
    groupName = const.PROP_TEXTURE_GROUP_ENTRY_PREFIX.format(groupID)
    storage = const.PROP_TEXTURE_GROUP_LIST
    group = GroupObject(groupName, storage)
    group.create(
        name = labelName, 
        flags = [] if flags is None else flags,
        sceneRoot = sceneRoot,
        propList = groupList
    )
    return group

def askForExistingPath(title = "", initDir = ""):
    """Opens a dialog to get a new path from the user
    """
    filters = "All files (*.*);;BMP (*.bmp);;JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png);;TGA (*.tga);;TIF (*.tif);;TIFF (*.tiff);;HDR (*.hdr);;DDS (*.dds)" 
    expPath = qtUtils.openSaveFileNamesDialog(caption=title,  _filter=filters, _dir=initDir)
    return expPath

def convertRelativePathToAbsolute(path):
    absTexturePath = utility.convertRelativePathToAbsolute(path, rt.pathConfig.getCurrentProjectFolder())
    if not os.path.exists(absTexturePath):
        absTexturePath = utility.convertRelativePathToAbsolute(path, rt.maxFilePath)
        if not os.path.exists(os.path.dirname(absTexturePath)):
            return None

    if absTexturePath == '':
        absTexturePath = None

    return absTexturePath

def convertAbsolutePathToRelative(path):
    return utility.convertAbsolutePathToRelative(path, rt.pathConfig.getCurrentProjectFolder())