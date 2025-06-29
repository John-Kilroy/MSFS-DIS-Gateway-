"""
This module contains the function to setup and export groups of object and preset ( as defined in presetUtils )
"""
import os
import uuid
import xml.etree.ElementTree as ET
import logging
import pymxs

import MultiExporter2024.constants as const
import MultiExporter2024.BabylonPYMXS2024 as babylonPYMXS2024

from typing import NamedTuple
from xml.dom import minidom

from PySide2.QtWidgets import QMessageBox

from maxsdk_2024 import perforce as sdkperforce
from maxsdk_2024 import qtUtils, sceneUtils, sharedGlobals, userprop, utility
from maxsdk_2024.globals import RT
from maxsdk_2024.logger import SignalHandler

handler = SignalHandler()
MSFS2024ExportLogger = logging.getLogger("MSFS2024ExportLogger")
MSFS2024ExportLogger.setLevel(level=logging.INFO)
MSFS2024ExportLogger.addHandler(handler)

class ExportGltf(NamedTuple):
    exportPath: str
    sceneNode: pymxs.MXSWrapperBase
    exportParameters: babylonPYMXS2024.BabylonParameters

def addExportPathToObjects(objects, forcedPath=None, prompt=True):
    """
        Find the root of each object and ask the user for a path. Store this path in the user property of the roots
        in: list(pymxs.MXSWrapperBase)
    """
    selected = objects
    maxPath = RT.maxFilePath
    initialDir = os.path.join((maxPath), "Export")

    if forcedPath != None:
        initialDir = forcedPath

    if not os.path.exists(initialDir):
        initialDir = maxPath

    # Open dialog to get path
    exportPath = RT.getSavePath(caption="Export Path", initialDir=initialDir)
    if exportPath is None:
        return

    selected = sceneUtils.getAllRoots(selected)
    passAll = not prompt

    exportPath = utility.convertAbsolutePathToRelative(exportPath, RT.pathConfig.getCurrentProjectFolder())
    exportPath += "\\"

    for s in selected:
        oldPath = sceneUtils.getSceneNodeUserProp(s, const.PROP_EXPORT_PATH)
        if oldPath is None:
            userprop.setUserProp(s, const.PROP_EXPORT_PATH, exportPath)
            continue

        if not passAll:
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Replace export path?",
                text=(f"Existing export path for:{s.name}Change path?\n \
                       From:\t{oldPath}To:\t{exportPath}"
                )
            )

            if popup == QMessageBox.No:
                continue
            if popup == QMessageBox.NoToAll:
                break
            if popup == QMessageBox.YesToAll:
                passAll = True

        userprop.setUserProp(s, const.PROP_EXPORT_PATH, exportPath)

def removeExportPathToObjects(objects, prompt=True):
    """
        Remove the export path stored in the user property of the objects. If prompt is false, automatically accepts everything and don't open any message box.
        in: 
            list(pymxs.MXSWrapperBase)
            prompt = boolean 
    """
    passAll = not prompt

    selected = sceneUtils.getAllRoots(objects)
    for s in selected:
        oldPath = sceneUtils.getSceneNodeUserProp(s, const.PROP_EXPORT_PATH)
        if oldPath is None:
            userprop.removeUserProp(s, const.PROP_EXPORT_PATH)
            continue
        if not passAll:
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title=(f"Remove export path from {s.name}"),
                text=(f"Are you sure you want to remove the export path of {s.name} ?\n \
                       Current path is :{oldPath}")
            )
            if (popup == QMessageBox.No):
                continue
            if (popup == QMessageBox.NoToAll):
                break
            if (popup == QMessageBox.YesToAll):
                passAll = True
        userprop.removeUserProp(s, const.PROP_EXPORT_PATH)

def collectObjectBundlesForExport(objects, optionPreset=None, progressBar=None, progressWeight=1):
    """Transform a selection of object into a collection of bundle ready to be exported.

    in: 
        objects= list(pymxs.MXSWrapperBase)
        optionPreset= presetUtils.OptionPresetObjects
    out: 
        list(ExportGltf : Tuple(exportPath, sceneNode, exportParameters))
        
    """
    bundles = []

    for i in range(0, len(objects)):
        if sharedGlobals.G_ME_cancelExport:
            break
        
        obj = objects[i]
        
        # Get export path from user property
        exportPath = getExportPath(obj)
        if (exportPath is None or exportPath == ""):
            MSFS2024ExportLogger.error("[GLTF][ERROR] Couldn't export {0}. No export path found.".format(obj.name))
            continue

        exportPathAbs = utility.convertRelativePathToAbsolute(exportPath, RT.pathConfig.getCurrentProjectFolder())

        # if path does not exist check if it's not relative to maxscene file path
        if (not os.path.exists(exportPathAbs)):
            exportPathAbs = utility.convertRelativePathToAbsolute(exportPath, RT.maxFilePath)

        if (not os.path.exists(exportPathAbs)):
            MSFS2024ExportLogger.error("[GLTF][ERROR] Gltf path is invalid for {0} (export path does not exists on disk). Please check export path (Refresh list maybe?)".format(obj.name))
            continue
        
        gltfFilePath = os.path.join(exportPathAbs, obj.name + ".gltf")
        
        # Find all gizmos
        originalHierarchy = sceneUtils.getDescendants(obj)
        gizmos = sceneUtils.filterGizmos(originalHierarchy)

        # Convert them to AsoboGizmos if needed
        try:
            gizmos = sceneUtils.convertGizmosToAsoboGizmos(gizmos)
        except Exception as error:
            MSFS2024ExportLogger.error("[GLTF][ERROR] Couldn't export {0}. Gizmos convert error: {1}".format(obj.name, error))
            continue

        sceneUtils.cleanupGizmosValues(gizmos)
        
        # run babylon exporter
        exportParameters = babylonPYMXS2024.BabylonParameters(gltfFilePath, "gltf")

        if optionPreset is not None:
            exportParameters = babylonPYMXS2024.applyOptionPresetToBabylonParam(optionPreset, exportParameters) ## Overwritten exportParameters

        exportParameters.exportOnlySelected = True

        #region Write Textures
        if exportParameters.writeTextures:
            textureFolder = exportParameters.textureFolder if (exportParameters.textureFolder != "") else os.path.dirname(gltfFilePath)
            exportParameters.textureFolder = utility.convertRelativePathToAbsolute(textureFolder, RT.pathConfig.getCurrentProjectFolder())
            if not os.path.exists(exportParameters.textureFolder):
                MSFS2024ExportLogger.error(f"[MultiExporter][ERROR] Texture Folder {exportParameters.textureFolder} does not exists.")
                return []
        #endregion
            
        bundle = ExportGltf(gltfFilePath, obj, exportParameters)
        bundles.append(bundle)

        if progressBar != None:
            progressBar.setValue(i * progressWeight)
    return bundles

def showCanceledExportPopup():
    qtUtils.popup(title="Export has been canceled", text="Export has been canceled.")

def exportObjects(objects, optionPreset=None, prompt=True, textureLib=False, progressBar=None):
    """Export the objects using the option preset if specified.

    in: 
          objects= list(pymxs.MXSWrapperBase)
          optionPreset= presetUtils.OptionPresetObject
    """
    # Note for LODs autogen: LODs filtering should already be done by now.
    # if LOD0 uses autoLOD -> remove other LODs objects from export, EXCEPT last one if minSize == 0 (override)

    objectsCount = len(objects)

    # We display percentage in progress bar.
    # we scale export processes "weights" to try to give the impression of a linear progression
    progressWeightCollectBundle = 1
    progressWeightGltfExport = 8
    if progressBar != None:
        progressMaxCollectBundle = objectsCount * progressWeightCollectBundle
        progressMaxGltfExport = objectsCount * progressWeightGltfExport * 2 # We multiply by 2 to get 50% progress before AND after process
        progressMax = progressMaxCollectBundle + progressMaxGltfExport
        progressBar.setMaximum(progressMax)

    # bundles : list(ExportGltf : Tuple)
    bundles = collectObjectBundlesForExport(
        objects=objects, 
        optionPreset=optionPreset, 
        progressBar=progressBar, 
        progressWeight=progressWeightCollectBundle
    )

    needsPreProcess = False
    for x in bundles:
        needsPreProcess = needsPreProcess or x.exportParameters.usePreExportProcess
        if needsPreProcess:
            break

    if needsPreProcess:
        if (prompt):
            if not qtUtils.popup_Yes_No(
                title="Your Max File needs to be saved.",
                text="Your max file needs to be saved before exporting.\nDo you want to save now to continue export?"
            ):
                showCanceledExportPopup()
                return []

        MSFS2024ExportLogger.info("[EXPORT][INFO] Saving max scene")
        sceneFileName = RT.maxFilePath + RT.maxFileName
        sceneFilePath = RT.getSaveFileName(
            caption="Save scene as", 
            filename=sceneFileName, 
            types=("3dsmax scene(*.max)|*.max")
        )

        if sceneFilePath == None:
            MSFS2024ExportLogger.error("[EXPORT][ERROR] Scene not saved!")
            showCanceledExportPopup()
            return []
        
        if not RT.saveMaxFile(sceneFilePath):
            MSFS2024ExportLogger.error("[EXPORT][ERROR] Failed to save scene!")
            return []

        MSFS2024ExportLogger.info(f"[EXPORT][INFO] Scene saved as: {sceneFilePath}")

    proceed = True
    bundleProgress = 0
    applyPreprScene = False

    if needsPreProcess:
        MSFS2024ExportLogger.info("[EXPORT][INFO] Saving scene in temp memory before pre-processing...")
        RT.holdMaxFile()
        MSFS2024ExportLogger.info("[EXPORT][INFO] Scene saved in temp memory")

    if needsPreProcess:
        proceed = babylonPYMXS2024.runPreExportProcess()
        if not proceed:
            MSFS2024ExportLogger.error("[EXPORT][ERROR] Pre-process failed")

    exportedGltfs = []
    if proceed:
        for x in bundles:
            applyPreprScene = applyPreprScene or x.exportParameters.applyPreprocessToScene
            if applyPreprScene:
                break

        for bundle in bundles:
            if sharedGlobals.G_ME_cancelExport:
                break

            if progressBar != None:
                bundleProgress += progressWeightGltfExport
                progressBar.setValue(progressMaxCollectBundle + bundleProgress)

            try:
                if exportBundleObjects(bundle): exportedGltfs.append(bundle)
            except Exception as error:
                MSFS2024ExportLogger.error(f"[EXPORT][ERROR] {os.path.split(bundle.exportPath)[1]}: {error}")
                continue

            if progressBar != None:
                bundleProgress += progressWeightGltfExport
                progressBar.setValue(progressMaxCollectBundle + bundleProgress)
                
    if needsPreProcess and not applyPreprScene:
        #TODO: maybe directly reload scene instead...? To benchmark/test
        MSFS2024ExportLogger.info("[EXPORT][INFO] Restoring scene...")
        RT.fetchMaxFile(quiet = True)
        MSFS2024ExportLogger.info("[EXPORT][INFO] Scene restored")

    if progressBar != None:
        progressBar.setValue(progressMax)
    
    return exportedGltfs
       
def exportBundleObjects(exportBundle):
    """
        Export a bundle.
    """
    exportParameters = exportBundle.exportParameters
    exportParameters.exportNode = exportBundle.sceneNode
    # We need to checkout files before export
    extensionLessPath = os.path.splitext(exportBundle.exportPath)[0]
    sdkperforce.P4edit(extensionLessPath + ".bin")
    sdkperforce.P4edit(extensionLessPath + ".gltf")
    return babylonPYMXS2024.runBabylonExporter(exportParameters)

def getExportPath(obj):
    path = userprop.getUserPropString(obj, const.PROP_EXPORT_PATH)
    return path

def markForDeleteObsoleteGLTF(flatName):
    """Given the path of an exported LOD without the LOD suffix, revert or delete the obsolete gltf.     
    When creating example_LOD0.gltf you need to delete example.gltf that use to be the exported asset

    in: flatName= str
    """
    targetGLTFFileName = flatName + ".gltf"
    targetBINFileName = flatName + ".bin"
    if os.path.exists(targetGLTFFileName) or os.path.exists(targetBINFileName):
        print(f"found {flatName} to remove")
        sdkperforce.P4revert(targetBINFileName)
        sdkperforce.P4revert(targetGLTFFileName)
        sdkperforce.P4delete(targetGLTFFileName)
        sdkperforce.P4delete(targetBINFileName)
      
# given a "..._LOD[0-9].gltf" or .bin path returns the xml path
def fromLODPathToMetadataPath(path):
    """Given the path of an exported LOD returns the path to the XML

    in: path= str
    """
    flatPath = os.path.splitext(path)[0]
    flatPath = utility.removeLODSuffix(flatPath)
    return flatPath + ".xml"

def getAbsoluteExportPath(obj):
    """Returns the absolute export path stored in the object user property.

    in: obj= pymxs.MXSWrapperBase
    """
    exportPath = getExportPath(obj)
    if (exportPath == None):
        return None

    assetFilePath = utility.convertRelativePathToAbsolute(exportPath, RT.pathConfig.getCurrentProjectFolder())

    if not os.path.exists(assetFilePath):
        assetFilePath = utility.convertRelativePathToAbsolute(exportPath, RT.maxFilePath)
        
    return assetFilePath

# given a "..._LOD[0-9].gltf" or .bin path returns the xml path
def getMetadataPath(obj):
    """Returns the XML path extrapolated from the export path stored in the object user property.

    in: 
          obj= pymxs.MXSWrapperBase
    out:
          xmlPath= str
    """
    exportPath = getAbsoluteExportPath(obj)
    if (exportPath == None):
        return None
    exportPath =  os.path.join(exportPath, utility.removeLODSuffix(obj.name))
    return exportPath + ".xml"
#
#  for a given set of objects setup as LODs, sort them by lodLevels _LOD0 1 2
# write a single xml file representing the aforementioned set of LODs
# keep the guid if the xml already exist, create a new one otherwise
def createLODMetadata(xmlPath, objects):
    """Create a single xml file for the list of objects. Objects are sorted based on their LOD level and their values are written in the xmlFile

    in: 
          xmlPath= str
          objects= list(pymxs.MXSWrapperBase)
    out:
          None
    """
    if len(objects) < 1:
        return

    exportModelName = objects[0].name
    if (not xmlPath):
        MSFS2024ExportLogger.error(
            f"[XML][ERROR] Can't create XML for {exportModelName}. \
            Make sure you have the rights to write in export folder."
        )
        return

    if (not os.path.exists(os.path.split(xmlPath)[0])):
        MSFS2024ExportLogger.error(
            f"[XML][ERROR] XML path is invalid for {exportModelName} \
            (export path does not exists on disk). \
            Please check export path (Refresh list maybe?)"
        )
        return

    modelInfo = None
    methodUsed = "created"

    if (os.path.exists(xmlPath)):  # if xml already exist parse it
        xml = open(xmlPath, "r")
        xmlData = xml.read()
        xml.close()
        if xmlData != "":
            try:
                xmlRoot = ET.fromstring(xmlData)
                if xmlRoot.tag == "ModelInfo":
                    modelInfo = xmlRoot
                    methodUsed = "updated"
                else:
                    MSFS2024ExportLogger.error(
                        f"[XML][ERROR] Already existing XML file for {exportModelName} with no ModelInfo root. \
                        Please fix before export."
                    )
                    return
            except Exception as e:
                MSFS2024ExportLogger.error(
                    f"[XML][ERROR] Already existing XML file for {exportModelName} is odd-shaped. \
                    Please fix before export.\n \
                    Error: {e}")
                return

    if modelInfo == None:
        modelInfo = ET.Element("ModelInfo")
        # assigned new guid
        modelInfo.set("guid", "{" + str(uuid.uuid4()) + "}")
        modelInfo.set("version", "1.1")

    lods = modelInfo.find("LODS") # find the registered LODs
    if (lods is not None): # if found clear (but not delete to keep declaration order in XML)
        lods.clear()
    else:
        lods = ET.SubElement(modelInfo, "LODS")
    
    lodObjectsOnly = sceneUtils.filterLODLevel(objects, "[0-9]+") # Get only lods, objects are already sorted properly
    lodCount = len(lodObjectsOnly)
    exportedLodCount = 0
    lodsAutoGen = False
    lastLodOverride = False
    if (lodCount > 0):  # if we found LODs register them
        if (sceneUtils.getLODLevelFromSceneNodeName(lodObjectsOnly[0]) != 0):
            MSFS2024ExportLogger.error(f"[XML][ERROR] Can't create metadata if {lodObjectsOnly[0].name} doesn't have a LOD0.")
            return
        lodsAutoGen = sceneUtils.getAutoLOD(lodObjectsOnly[0], const.PROP_AUTO_LOD) #LOD auto generation is checked using first LOD property only
        if (lodsAutoGen):
            firstLodObj = lodObjectsOnly[0]
            lods.set("autoGenerate", "true")
            lod = ET.SubElement(lods, "LOD") #add first LOD with no minSize as it will be automatically set
            lod.set("ModelFile", str(firstLodObj.name) + ".gltf")
            #### Last LOD override:
            if (lodCount > 1):
                lastLodObj = lodObjectsOnly[lodCount - 1]
                lodValue = sceneUtils.getLODValue(lastLodObj, const.PROP_LOD_VALUE)
                if (lodValue != None and lodValue == 0): #last LOD override can be done using minSize=0
                    lod = ET.SubElement(lods, "LOD")
                    lod.set("minSize", str(0))
                    lod.set("ModelFile", str(lastLodObj.name) + ".gltf")
                    lastLodOverride = True
        else:
            for i in range(lodCount):
                obj = lodObjectsOnly[i]
                lod = ET.SubElement(lods, "LOD")

                lodValue = sceneUtils.getLODValue(obj, const.PROP_LOD_VALUE)
                if (lodValue == None):  # if no valid LOD Value found pick a default value
                    lodValue = sceneUtils.getDefaultLODValue(sceneUtils.getLODLevelFromSceneNodeName(obj))
                    MSFS2024ExportLogger.warning(f"[XML][WARNING] Couldn't find LOD min size on {obj.name} it will use the default value {lodValue}")

                if i < lodCount - 1: #Dont write the last minSize value, it will be ignored anyway
                    lod.set("minSize", str(lodValue))

                lod.set("ModelFile", str(obj.name) + ".gltf")

        # if we have LODs in the file we check if there is an old object before the lods and delete it
        flatName = os.path.splitext(xmlPath)[0]
        markForDeleteObsoleteGLTF(flatName)
        exportedLodCount = lodCount

    else: # If no LODs, we may have only ONE object, and export should still be valid
        if len(objects) == 1:
            lod = ET.SubElement(lods, "LOD")
            lod.set("ModelFile", str(objects[0].name) + ".gltf")
            exportedLodCount = 1
        else:
            for obj in objects:
                if not sceneUtils.getAutoLOD(obj, const.PROP_AUTO_LOD):
                    continue
                # in case Auto LODs is checked, 
                # lets throw in a bit of infos so user knows why it is failing. 
                # If it has been unintentionnally set, then this may sparks some good practices habits too.
                MSFS2024ExportLogger.warning(
                    f"[XML][WARNING] for \"Auto LODs\" on {obj.name} to work, \
                    object needs to be properly named (either ends with \"_LOD[nb]\" \
                    or start with \"x[nb]_\")"
                )

    ## Write modelInfo in XML file
    xmlLog = writeXML(xmlPath, modelInfo)
    
    if xmlLog == "" :
        if (lodsAutoGen):
            llo = " with last LOD override" if lastLodOverride else ""
            MSFS2024ExportLogger.info(f"[XML] Successfully {methodUsed} XML file for {exportModelName}. Using auto LODs{llo}", exc_info=1)
        else:
            MSFS2024ExportLogger.info(f"[XML] Successfully {methodUsed} XML file for {exportModelName}. It contains {exportedLodCount} LODs")
    else:
        MSFS2024ExportLogger.error(xmlLog)

def createLODMetadataForSimObject(xmlPath, objects):
    """Create a single xml file for the list of objects. Objects are sorted based on their LOD level and their values are written in the xmlFile

    in: 
          xmlPath= str
          objects= list(pymxs.MXSWrapperBase)
    out:
          None
    """
    if len(objects) < 1:
        return
    
    if (not xmlPath):
        MSFS2024ExportLogger.error(f"[XML][ERROR] Can't create metadata path for {objects[0].name} Check your object's export path.")
        return 

    if (not os.path.exists(os.path.split(xmlPath)[0])):
        MSFS2024ExportLogger.error("[XML][ERROR] The output path for the xml is invalid, you probably need to save your max file and redo the export path.")
        return

    if (os.path.exists(xmlPath)):  # if xml already exist parse it
        xml = open(xmlPath, "r")
        modelInfo = ET.fromstring(xml.read())
        methodUsed = "updated"
    else:  # otherwise create it
        modelInfo = ET.Element("ModelInfo")
        # assigned new guid
        modelInfo.set("guid", "{" + str(uuid.uuid4()) + "}")
        modelInfo.set("version", "1.1")
        methodUsed = "created"

    lods = modelInfo.find("LODS")  # find the registered LODs
    if (lods is not None):  # if found delete them
        modelInfo.remove(lods)

    objectToSort = sceneUtils.filterLODLevel(objects, "[0-9]+")
    sortedObjects = sceneUtils.sortObjectsByLODLevels(objectToSort)  # sort object by lod levels
    lodCount = len(objectToSort)
    flatName = os.path.splitext(xmlPath)[0]
    exportModelName = os.path.split(flatName)[1]

    if (len(sortedObjects) != 0):  # if we found LODs register them
        if (sceneUtils.getLODLevelFromSceneNodeName(sortedObjects[0]) != 0):
            MSFS2024ExportLogger.error(f"[XML][ERROR] Can't create metadata if {sortedObjects[0].name} doesn't have a LOD0.")
            return

        lods = ET.SubElement(modelInfo, "LODS")
        for obj in sortedObjects:
            lod = ET.SubElement(lods, "LOD")
            lodValue = sceneUtils.getLODValue(obj)

            if (lodValue == None):  # if no valid LOD Value found pick a default value
                lodValue = sceneUtils.getDefaultLODValue(sceneUtils.getLODLevelFromSceneNodeName(obj))
                MSFS2024ExportLogger.warning(f"[XML][WARNING] Couldn't find LOD min size on {obj.name} it will use the default value {lodValue}")

            lod.set("minSize", str(lodValue))
            lod.set("ModelFile", str(obj.name) + ".gltf")
        # if we have LODs in the file we check if there is an old object before the lods and delete it
        markForDeleteObsoleteGLTF(flatName)
        
    xmlLog = writeXML(xmlPath, modelInfo)
    if xmlLog != "" :
        MSFS2024ExportLogger.error(xmlLog)
        return

    MSFS2024ExportLogger.info(f"[XML] Successfully {methodUsed} XML file for {exportModelName}. It contains {lodCount} LODs")

def writeXML(xmlPath, root):
    """Write a xml.etree.ElementTree to a xml file.

    in:
          xmlPath= str
          root= xml.etree.ElementTree.Element
    out:
          str
    """
    output = ET.tostring(root)
    xmlstr = minidom.parseString(output).toprettyxml(encoding='utf-8', indent="\t").decode("utf-8")
    dom_string = os.linesep.join([s for s in xmlstr.splitlines() if s.strip()])
    sdkperforce.P4edit(xmlPath)
    try:
        myfile = open(xmlPath, "w+")
        myfile.write(dom_string)
        sdkperforce.P4edit(xmlPath) # in case new file
        return ""
    except IOError:       
        return (f"[XML][ERROR] XML file {xmlPath} is not writable.\n\tPlease make file writable.")
