'''
Wrapper to easily run babylon form pymxs
'''
import datetime
import logging
import os
import time

from maxsdk_2024.globals import RT
from maxsdk_2024.logger import SignalHandler

from enum import Enum

handler = SignalHandler()
MSFS2024ExportLogger = logging.getLogger("MSFS2024ExportLogger")
MSFS2024ExportLogger.setLevel(level=logging.INFO)
MSFS2024ExportLogger.addHandler(handler)

propertyToDefault = {
    "babylonjs_txtCompression" : 100,
    "babylonjs_txtScaleFactor" : 1,
    "flightsim_tangent_space_convention": 0,
    "babylonjs_export_animations_type": "Export",
    "babylonjs_export_materials": True,
    "flightsim_removelodprefix": True,
    "babylonjs_animgroupexportnonanimated": False,
    "babylonjs_bakeAnimationsType": 0,  # after this the values are just usual type default
    "babylonjs_autosave": False,
    "babylonjs_exporthidden" : False,
    "babylonjs_preproces": False,
    "babylonjs_mergecontainersandxref" : False, 
    "babylonjs_applyPreprocess": False,
    "flightsim_flattenNodes": True,    
    "babylonjs_writetextures": False,
    "flightsim_keepInstances": False,    
    "babylonjs_asb_animation_retargeting": False,
    "flightsim_asb_unique_id": True,
    "babylonjs_onlySelected": False,
    "flightsim_exportAsSubmodel": False
}

babylonParameters = [
    "babylonjs_autosave",   
    "babylonjs_exporthidden",
    "flightsim_removelodprefix",
    "babylonjs_export_materials",
    "flightsim_tangent_space_convention",
    "babylonjs_animgroupexportnonanimated",
    "babylonjs_preproces",
    "babylonjs_mergecontainersandxref",
    "babylonjs_applyPreprocess",
    "flightsim_flattenNodes",
    "babylonjs_bakeAnimationsType",
    "babylonjs_asb_animation_retargeting",
    "flightsim_asb_unique_id",
    "babylonjs_txtCompression",
    "babylonjs_writetextures",
    "flightsim_keepInstances",
    "babylonjs_export_animations_type",
    "babylonjs_txtScaleFactor",
    "textureFolderPathProperty",
    "babylonjs_onlySelected",
    "flightsim_exportAsSubmodel"
]

class BabylonParameters:
    exportNode = None
    exportLayers = None
    outputPath = None
    outputFormat = None
    textureFolder = None
    scaleFactor = None #1
    writeTextures = None #False
    animationExportType = None # RT.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").Export')
    enableASBUniqueID = None #True
    exportHiddenObjects = None #True
    exportMaterials = None #False
    exportOnlySelected = None #False
    usePreExportProcess = None #False
    applyPreprocessToScene = None #False
    mergeContainersAndXRef = None #False
    flattenNodes = None #True
    bakeAnimationType = None # RT.execute('(dotnetclass "MSFS2024_Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    removeNamespaces = None #True
    removeLodPrefix = None  #True
    keepInstances = None  #False
    tangentSpaceConvention = None  #0
    exportAsSubmodel = None #False


    def __init__(self, outputPath, outputFormat):
        self.outputPath = outputPath
        self.outputFormat = outputFormat

#region Animation Type
WRITE_TYPE = Enum('WRITE_TYPE', ['INDEX', 'NAME'])

class AnimationExportType(Enum):
    Export = 0
    NotExport = 1
    ExportONLY = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._member_map_ 

class BakeAnimationType(Enum):
    DoNotBakeAnimation = 0
    BakeAllAnimations = 1
    BakeSelective = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._member_map_ 
#endregion

#region PRIVATE
def _runBabylonAction(action, successMsg):
    timeStart = time.time()
    criticalError = None
    try:
        action()
        if not hasattr(RT, "logger"):
            MSFS2024ExportLogger.error("An error as occured, no logs are available.")
            return False
        for msg in RT.logger.GetLogEntries():
            if msg.progress: 
                continue
            message = msg.message
            if msg.level.toString() == "ERROR":
                MSFS2024ExportLogger.error("{0}".format(message))
            if msg.level.toString() == "WARNING":
                MSFS2024ExportLogger.warning("{0}".format(message))
            if msg.level.toString() == "MESSAGE":
                MSFS2024ExportLogger.info("{0}".format(message))
    except Exception as criticalError:
        message =  str.replace(str(criticalError), "MAXScript exception raised.\n-- Runtime error: .NET runtime exception: ", "") ## need to remove this to get a clear error message
        MSFS2024ExportLogger.error(f"[BABYLON][EXPORT] An error as occured during the export process :\n{message}")
        MSFS2024ExportLogger.warning("[BABYLON][EXPORT] Export has been canceled")
        return False

    MSFS2024ExportLogger.info(successMsg)
    delta = round(time.time() - timeStart, 3)
    MSFS2024ExportLogger.info("[BABYLON] Operation completed in {0}s".format(delta))
    MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    return True

def _castStrToDotNetEnum(dotnetenum, string):
    '''
    Find enum value of key string and returns it
    \nin : 
    dotnetenum= str("dotnetenum") 
    string= str  
    \nout : 
    RT.dotNetObject 
    '''
    arg = string.replace(" ","")
    command = '(dotnetclass "{0}").{1}'.format(dotnetenum,arg)
    return RT.execute(command)

def _castIntToDotNetBakeAnimationEnum(dotnetenum, index):
    '''
    Cast python int to dotnetobject enum
    \nin : 
    dotnetenum= str("dotnetenum") 
    index= int 
    \nout : 
    RT.dotNetObject 
    '''
    prop = RT.name(BakeAnimationType(index).name)
    command = '(dotnetclass "{0}").{1}'.format(dotnetenum, prop)
    return RT.execute(command)

def _getBabylonParamFromDict(_dict, _prop):
    if (_prop in _dict):
        return _dict[_prop]
    else:
        if _prop in propertyToDefault:
            return propertyToDefault[_prop]
    return None

def _setRTParameters(babylonParameters):
    if not isinstance(babylonParameters, BabylonParameters):
        return
    
    RT.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
    RT.execute('param.logLevel = (dotNetClass "MSFS2024_Max2Babylon.LogLevel").WARNING')
    RT.execute('logger = dotNetObject "MSFS2024_Max2Babylon.MaxScriptLogger" false')
    RT.execute('logger.logLevel = (dotNetClass "MSFS2024_Max2Babylon.LogLevel").WARNING')
    if (babylonParameters.exportNode):
        RT.param.exportNode =  RT.param.GetNodeByHandle(babylonParameters.exportNode.inode.handle)
    if(babylonParameters.exportLayers):
        RT.param.exportLayers = RT.param.NameToIILayer(babylonParameters.exportLayers)      
    RT.param.outputPath = babylonParameters.outputPath
    RT.param.outputFormat = babylonParameters.outputFormat
    RT.param.scaleFactor = babylonParameters.scaleFactor
    RT.param.animationExportType = babylonParameters.animationExportType
    RT.param.enableASBUniqueID = babylonParameters.enableASBUniqueID
    RT.param.exportHiddenObjects = babylonParameters.exportHiddenObjects
    RT.param.exportMaterials = babylonParameters.exportMaterials
    RT.param.usePreExportProcess = babylonParameters.usePreExportProcess
    RT.param.applyPreprocessToScene = babylonParameters.applyPreprocessToScene
    RT.param.flattenNodes = babylonParameters.flattenNodes
    RT.param.mergeContainersAndXRef = babylonParameters.mergeContainersAndXRef
    RT.param.bakeAnimationType = babylonParameters.bakeAnimationType
    RT.param.removeNamespaces = babylonParameters.removeNamespaces
    RT.param.removeLodPrefix = babylonParameters.removeLodPrefix
    RT.param.keepInstances = babylonParameters.keepInstances
    RT.param.tangentSpaceConvention = babylonParameters.tangentSpaceConvention
    RT.param.exportOnlySelected = babylonParameters.exportOnlySelected
    RT.param.exportAsSubmodel = babylonParameters.exportAsSubmodel
#endregion

#region PUBLIC
def getPropertyDefaultValue(property):
    if property in propertyToDefault:
        return propertyToDefault[property]
    else:
        return None

def applyOptionPresetToBabylonParam(optionPreset, babylonParam):
    """
    Apply the parameters of an OptionPresetObject onto a BabylonParam

    \nin: 
    optionPreset : OptionPresetObject 
    babylonParam : BabylonParameters
    \nout: 
    BabylonParameters (modified)
    """
    properties = optionPreset.dictionary
    babylonParam.writeTextures = _getBabylonParamFromDict(properties,"babylonjs_writetextures")
    babylonParam.animationExportType = _castStrToDotNetEnum("BabylonExport.Entities.AnimationExportType",_getBabylonParamFromDict(properties,"babylonjs_export_animations_type"))
    babylonParam.enableASBUniqueID = _getBabylonParamFromDict(properties,"flightsim_asb_unique_id")
    babylonParam.exportHiddenObjects = _getBabylonParamFromDict(properties,"babylonjs_exporthidden")
    babylonParam.exportMaterials = _getBabylonParamFromDict(properties,"babylonjs_export_materials")
    babylonParam.usePreExportProcess = _getBabylonParamFromDict(properties,"babylonjs_preproces") 
    babylonParam.applyPreprocessToScene = _getBabylonParamFromDict(properties,"babylonjs_applyPreprocess") 
    babylonParam.mergeContainersAndXRef = _getBabylonParamFromDict(properties,"babylonjs_mergecontainersandxref") 
    babylonParam.bakeAnimationType = _castIntToDotNetBakeAnimationEnum("MSFS2024_Max2Babylon.BakeAnimationType", _getBabylonParamFromDict(properties,"babylonjs_bakeAnimationsType")) # RT.execute('(dotnetclass "MSFS2024_Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    babylonParam.removeNamespaces = _getBabylonParamFromDict(properties,"flightsim_removenamespaces")
    babylonParam.removeLodPrefix = _getBabylonParamFromDict(properties,"flightsim_removelodprefix")
    babylonParam.keepInstances = _getBabylonParamFromDict(properties,"flightsim_keepInstances")
    babylonParam.tangentSpaceConvention = _getBabylonParamFromDict(properties,"flightsim_tangent_space_convention")
    babylonParam.textureFolder = _getBabylonParamFromDict(properties, "textureFolderPathProperty")
    babylonParam.flattenNodes = _getBabylonParamFromDict(properties, "flightsim_flattenNodes")
    babylonParam.exportOnlySelected = _getBabylonParamFromDict(properties, "babylonjs_onlySelected")
    babylonParam.exportAsSubmodel = _getBabylonParamFromDict(properties, "flightsim_exportAsSubmodel")

    return babylonParam

def initializeBabylonExport():
    RT.execute('Assembly = dotNetClass "System.Reflection.Assembly"')
    dllPath = os.path.join(RT.symbolicPaths.getPathValue(1),"bin\\assemblies\\MSFS2024_Max2Babylon.dll")
    RT.execute('Assembly.loadfrom "{0}"'.format(dllPath))
    RT.execute('maxScriptManager = dotNetObject "MSFS2024_Max2Babylon.MaxScriptManager"')
    RT.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
    RT.execute('param.logLevel = (dotNetClass "MSFS2024_Max2Babylon.LogLevel").WARNING')
    RT.maxScriptManager.InitializeGuidTable()

def runResolveID():
    MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    MSFS2024ExportLogger.info("[BABYLON][ASOBO_UNIQUE_ID] Resolve Unique ID started at " + str(datetime.datetime.now()))
    action = lambda : RT.maxScriptManager.runResolveUniqueID()
    return _runBabylonAction(action, "[BABYLON][ASOBO_UNIQUE_ID] UniqueID has been resolved. Please save the scene to apply those modifications")

def runBabylonExporter(babylonParameters):
    MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    MSFS2024ExportLogger.info("[BABYLON][EXPORT] New operation started at " + str(datetime.datetime.now()))
    _setRTParameters(babylonParameters)
    action = lambda : RT.maxScriptManager.Export(RT.param, RT.logger)
    return _runBabylonAction(action, "[BABYLON][EXPORT] Operation completed")
        
def runPreExportProcess():
    MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    MSFS2024ExportLogger.info("[BABYLON][PRE-EXPORT] New operation started at " + str(datetime.datetime.now()))
    RT.execute('logger = dotNetObject "MSFS2024_Max2Babylon.MaxScriptLogger" false')
    RT.execute('logger.logLevel = (dotNetClass "MSFS2024_Max2Babylon.LogLevel").WARNING')
    RT.execute('preExportProcess = dotNetObject "MSFS2024_Max2Babylon.PreExport.PreExportProcess" param logger')
    action = lambda: RT.preExportProcess.ApplyPreExport()
    return _runBabylonAction(action, "[BABYLON][PRE-EXPORT] Operation completed")
#endregion