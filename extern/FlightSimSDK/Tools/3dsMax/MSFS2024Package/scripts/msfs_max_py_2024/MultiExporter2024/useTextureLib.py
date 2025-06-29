import logging
from os import path, remove

from pymxs import runtime as rt
from TextureTool2024.TextureLib.BitmapConfig import compatibleBitmapIndex
from TextureTool2024.TextureLib.glTFLib import getAllGltfTextureConfig
from TextureTool2024.TextureLib.textureXmlLib import XmlSerializer

from maxsdk_2024 import sharedGlobals
from maxsdk_2024.logger import SignalHandler
from maxsdk_2024.perforce import P4add, P4edit

handler = SignalHandler()
textureLibLogger = logging.getLogger("MSFS2024ExportLogger")
textureLibLogger.setLevel(level=logging.INFO)
textureLibLogger.addHandler(handler)

def getAllMAXTextures():
    """
    Return all textures currently used in the max scene
    """
    resultSet = set()
    resultList = None
    materials = rt.sceneMaterials
    # materials = rt.mEditMaterials
    for mat in materials :
        for um in rt.usedMaps(mat):
            resultSet.add(um)

    resultList = list(resultSet)
    resultList.sort()
    return resultList

def createXML(texturePath, textureConfig):
    """
    Write a new xml with the textureConfig at the xmlPath location
    Return True when succesfully created
    """
    xmlPath = texturePath + ".xml"
    if not path.exists(texturePath):
        textureLibLogger.error(f"[TEXTURELIB] Texture : '{texturePath}' does not exists.")
        return
        
    serializer = XmlSerializer(xmlPath)
    doesFileAlreadyExists = path.exists(xmlPath)
    if ' ' in texturePath:
        textureLibLogger.error(f"[TEXTURELIB][ERROR] Failed {path.basename(texturePath)} contains whitespace(s), \
                                so the XML will not be generated for it. \
                                Please remove them before regenerating."
        )
        return

    if doesFileAlreadyExists:
        if serializer.Open():
            if serializer.bmpConfig.materialBitmap == textureConfig.materialBitmap and serializer.bmpConfig.forceNoAlpha == textureConfig.forceNoAlpha :
                P4edit(xmlPath) # just in case it's not already tracked
                P4edit(texturePath)
                textureLibLogger.info("[TEXTURELIB] Done (skip)")
                return
        else :
            remove(xmlPath)
        P4edit(xmlPath)
        P4edit(texturePath)

    # Update xml config
    if not doesFileAlreadyExists:
        serializer.bmpConfig = textureConfig
        textureLibLogger.info("[TEXTURELIB] Done (created)")
    elif compatibleBitmapIndex(serializer.bmpConfig.materialBitmap, textureConfig.materialBitmap):
        serializer.bmpConfig.materialBitmap = textureConfig.materialBitmap
        serializer.bmpConfig.forceNoAlpha = textureConfig.forceNoAlpha
        textureLibLogger.info("[TEXTURELIB] Done (overwriting compatible)")
    else :
        serializer.bmpConfig = textureConfig
        textureLibLogger.info("[TEXTURELIB] Done (overwriting)")

    ret = serializer.Save()

    if not ret:
        textureLibLogger.error("[TEXTURELIB][ERROR] Failed (writing went wrong)")
        return

    if not doesFileAlreadyExists:
        P4add(xmlPath)
        P4add(texturePath)

def exportTextureLibWithGltf(exportedGltfsParameters, progressBar=None):
    """
    Use a list of bundle gltf(contains path and all parameters) to parse them and create the xml textures needed next to all textures found in the current max project
    """
    if len(exportedGltfsParameters) == 0 :
        print("[TEXTURELIB][ERROR] No glTF where provided. Ignoring texture lib generation. ")
        return

    textureConfigs = getAllGltfTextureConfig(exportedGltfsParameters)
    texturePaths = getAllMAXTextures()
    
    if progressBar is not None:
        progressBar.setMaximum(len(texturePaths))

    for texturePath in texturePaths :
        if sharedGlobals.G_ME_cancelExport:
            break

        if progressBar is not None:
            progressBar.setValue(progressBar.value() + 1)

        textureName = path.basename(texturePath)
        textureConfig = textureConfigs.pop(textureName, None)
        if textureConfig is None:
            continue

        if textureConfig[1] != '':
            texturePath = path.join(textureConfig[1], path.basename(texturePath))
            
        if not path.exists(texturePath):
            textureLibLogger.error(f"[TEXTURELIB][ERROR] Path : {texturePath} does not exists. ")
        else:
            textureLibLogger.info(f"[TEXTURELIB] Generating XML for texture '{str(texturePath)}' :")
            createXML(texturePath, textureConfig[0])

    if sharedGlobals.G_ME_cancelExport:
        return

    if len(textureConfigs) < 1:
        return

    textureLibLogger.error("[TEXTURELIB][ERROR] An XML couldn't be created for these textures : ")
    for texName in textureConfigs :
        textureLibLogger.error(f"[TEXTURELIB] XML for {texName} couldn't be created. Check if the texture exists in the project. It could be converted to another format while writing.")

