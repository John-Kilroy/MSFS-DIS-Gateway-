import logging
from json import load
from os.path import basename

from maxsdk_2024.logger import SignalHandler

from ..textureConfig import TextureConfig
from .BitmapConfig import BitmapConfig, compatibleBitmapIndex

handler = SignalHandler()
gltfLibLogger = logging.getLogger("MSFS2024ExportLogger")
gltfLibLogger.setLevel(level=logging.INFO)
gltfLibLogger.addHandler(handler)


def getMatConfigFromGLTF(mat) :
    """
    Convert the material definition in a gltf to texture index and flags
    glTFMaterial_G.cpp, line 1362 (conversion function) + line ~300 (infos on custom extension names)
      - GetMatConfig(mat : dict) -> list[TextureConfig]
    """
    ret = list()

    metallicRoughnessTexture = None
    pbrMetallicRoughness = mat.get("pbrMetallicRoughness")
    if (pbrMetallicRoughness is not None) :

        baseColorTexture = pbrMetallicRoughness.get("baseColorTexture")
        if (baseColorTexture is not None) :
            # MTL_BITMAP_DECAL0
            ret.append( TextureConfig(id=baseColorTexture.get("index"), bitmapConfig=BitmapConfig(1, "", False)) )
            
        metallicRoughnessTexture = pbrMetallicRoughness.get("metallicRoughnessTexture")
        if (metallicRoughnessTexture is not None) :
            # MTL_BITMAP_METAL_ROUGH_AO
            ret.append( TextureConfig(id=metallicRoughnessTexture.get("index"), bitmapConfig=BitmapConfig(11, "", True)) )
    
    occlusionTexture = mat.get("occlusionTexture")
    if (occlusionTexture is not None) :
        if (metallicRoughnessTexture is None) or (occlusionTexture.get("index") != metallicRoughnessTexture.get("index")) :
            # MTL_BITMAP_OCCLUSION
            ret.append( TextureConfig(id=occlusionTexture.get("index"), bitmapConfig=BitmapConfig(14, "", True)) )

    normalTexture = mat.get("normalTexture")
    if (normalTexture is not None) :
        # MTL_BITMAP_NORMAL
        ret.append( TextureConfig(id=normalTexture.get("index"), bitmapConfig=BitmapConfig(3, "", False)) )

    emissiveTexture = mat.get("emissiveTexture")
    if (emissiveTexture is not None) :
        # MTL_BITMAP_EMISSIVE
        ret.append( TextureConfig(id=emissiveTexture.get("index"), bitmapConfig=BitmapConfig(7, "", False)) )

    extensions = mat.get("extensions")
    if (extensions is not None) :
        
        detail_map = extensions.get("ASOBO_material_detail_map")
        if (detail_map is not None) :

            blendMaskTexture = detail_map.get("blendMaskTexture")
            if (blendMaskTexture is not None) :
                # MTL_BITMAP_BLENDMASK
                ret.append( TextureConfig(id=blendMaskTexture.get("index"), bitmapConfig=BitmapConfig(2, "", False)) )

            detailColorTexture = detail_map.get("detailColorTexture")
            if (detailColorTexture is not None) :
                if (blendMaskTexture is not None) :
                    # MTL_BITMAP_ADD_DECAL0
                    ret.append( TextureConfig(id=detailColorTexture.get("index"), bitmapConfig=BitmapConfig(5, "", False)) )
                else :
                    # MTL_BITMAP_DETAILDIFFUSE
                    ret.append( TextureConfig(id=detailColorTexture.get("index"), bitmapConfig=BitmapConfig(8, "", False)) )

            detailNormalTexture = detail_map.get("detailNormalTexture")
            if (detailNormalTexture is not None) :
                if (blendMaskTexture is not None) :
                    # MTL_BITMAP_ADD_NORMAL
                    ret.append( TextureConfig(id=detailNormalTexture.get("index"), bitmapConfig=BitmapConfig(6, "", False)) )
                else :
                    # MTL_BITMAP_DETAILNORMAL
                    ret.append( TextureConfig(id=detailNormalTexture.get("index"), bitmapConfig=BitmapConfig(9, "", False)) )

            detailMetalRoughAOTexture = detail_map.get("detailMetalRoughAOTexture")
            if (detailMetalRoughAOTexture is not None) :
                if (blendMaskTexture is not None) :
                    # MTL_BITMAP_ADD_METAL_ROUGH_AO
                    ret.append( TextureConfig(id=detailMetalRoughAOTexture.get("index"), bitmapConfig=BitmapConfig(13, "", True)) )
                else :
                    # MTL_BITMAP_DETAIL_METAL_ROUGH_AO
                    ret.append( TextureConfig(id=detailMetalRoughAOTexture.get("index"), bitmapConfig=BitmapConfig(12, "", True)) )

        anisotropic = extensions.get("ASOBO_material_anisotropic_v2")
        if (anisotropic is not None) :
            anisoDirectionRoughnessTexture = anisotropic.get("anisoDirectionRoughnessTexture")
            if (anisoDirectionRoughnessTexture is not None) :
                # MTL_BITMAP_ANISO_DIR_ROUGH
                ret.append( TextureConfig(id=anisoDirectionRoughnessTexture.get("index"), bitmapConfig=BitmapConfig(17, "", True)) )

        parallax_window = extensions.get("ASOBO_material_parallax_window")
        if (parallax_window is not None) :
            behindWindowMapTexture = parallax_window.get("behindWindowMapTexture")
            if (behindWindowMapTexture is not None) :
                # MTL_BITMAP_ADD_DECAL0
                ret.append( TextureConfig(id=behindWindowMapTexture.get("index"), bitmapConfig=BitmapConfig(5, "", False)) )

        material_windshield_v3 = extensions.get("ASOBO_material_windshield_v3")
        if (material_windshield_v3 is not None) :
            wiperMaskTexture = material_windshield_v3.get("wiperMaskTexture")
            if (wiperMaskTexture is not None) :
                # MTL_BITMAP_WIPERMASK
                ret.append( TextureConfig(id=wiperMaskTexture.get("index"), bitmapConfig=BitmapConfig(18, "", False)) )
            windshieldDetailNormalTexture = material_windshield_v3.get("windshieldDetailNormalTexture")
            if (windshieldDetailNormalTexture is not None) :
                # MTL_BITMAP_WINDSHIELDDETAILNORMAL
                ret.append( TextureConfig(id=windshieldDetailNormalTexture.get("index"), bitmapConfig=BitmapConfig(19, "", False)) )
            scratchesNormalTexture = material_windshield_v3.get("scratchesNormalTexture")
            if (scratchesNormalTexture is not None) :
                # MTL_BITMAP_SCRATCHESNORMAL
                ret.append( TextureConfig(id=scratchesNormalTexture.get("index"), bitmapConfig=BitmapConfig(20, "", False)) )
            windshieldInsectsTexture = material_windshield_v3.get("windshieldInsectsTexture")
            if (windshieldInsectsTexture is not None) :
                # MTL_BITMAP_WINDSHIELDINSECTS
                ret.append( TextureConfig(id=windshieldInsectsTexture.get("index"), bitmapConfig=BitmapConfig(23, "", False)) )
            windshieldInsectsMaskTexture = material_windshield_v3.get("windshieldInsectsMaskTexture")
            if (windshieldInsectsMaskTexture is not None) :
                # MTL_BITMAP_WINDSHIELDINSECTSMASK
                ret.append( TextureConfig(id=windshieldInsectsMaskTexture.get("index"), bitmapConfig=BitmapConfig(24, "", False)) )

        tree = extensions.get("ASOBO_material_foliage_mask")
        if (tree is not None) :
            foliageMaskTexture = tree.get("foliageMaskTexture")
            if (foliageMaskTexture is not None) :
                # MTL_BITMAP_ALPHABLENDMASK
                ret.append(TextureConfig(id=foliageMaskTexture.get("index"), bitmapConfig=BitmapConfig(21, "", False)))

        extra_occlusion = extensions.get("ASOBO_extra_occlusion")
        if (extra_occlusion is not None) :
            extraOcclusionTexture = extra_occlusion.get("extraOcclusionTexture")
            if (extraOcclusionTexture is not None) :
                # MTL_BITMAP_OCCLUSION
                ret.append( TextureConfig(id=extraOcclusionTexture.get("index"), bitmapConfig=BitmapConfig(14, "", False)) )

        clear_coat2 = extensions.get("ASOBO_material_clear_coat_v2")
        if (clear_coat2 is not None) :
            clearcoatColorRoughnessTexture = clear_coat2.get("clearcoatColorRoughnessTexture")
            if (clearcoatColorRoughnessTexture is not None) :
                # MTL_BITMAP_CLEARCOATCOLORROUGHNESS
                ret.append( TextureConfig(id=clearcoatColorRoughnessTexture.get("index"), bitmapConfig=BitmapConfig(15, "", False)) )
            clearcoatNormalTexture = clear_coat2.get("clearcoatNormalTexture")
            if (clearcoatNormalTexture is not None) :
                # MTL_BITMAP_CLEARCOATNORMAL
                ret.append( TextureConfig(id=clearcoatNormalTexture.get("index"), bitmapConfig=BitmapConfig(16, "", False)) )
        dirt_mask = extensions.get("ASOBO_material_geometry_decal")
        if (dirt_mask is not None) :
            maskTexture = dirt_mask.get("blendMaskTexture")
            if (maskTexture is not None) :
                # MTL_BITMAP_BLENDMASK
                ret.append( TextureConfig(id=maskTexture.get("index"), bitmapConfig=BitmapConfig(2, "", False)) )
        iridescent = extensions.get("ASOBO_material_iridescent")
        if (iridescent is not None) :
            iridescentThicknessTexture = iridescent.get("iridescentThicknessTexture")
            if (iridescentThicknessTexture is not None) :
                # MTL_BITMAP_BLENDMASK
                ret.append( TextureConfig(id=iridescentThicknessTexture.get("index"), bitmapConfig=BitmapConfig(22, "", False)) )
                
        dirt = extensions.get("ASOBO_material_dirt")
        if (dirt is not None) :
            dirtTexture = dirt.get("dirtTexture")
            if (dirtTexture is not None) :
                # MTL_BITMAP_DIRT
                ret.append( TextureConfig(id=dirtTexture.get("index"), bitmapConfig=BitmapConfig(4, "", False)) )
            dirtOcclusionRoughnessMetallicTexture = dirt.get("dirtOcclusionRoughnessMetallicTexture")
            if (dirtOcclusionRoughnessMetallicTexture is not None) :
                # MTL_BITMAP_DIRT_METAL_ROUGH_AO
                ret.append( TextureConfig(id=dirtOcclusionRoughnessMetallicTexture.get("index"), bitmapConfig=BitmapConfig(21, "", False)) )

        tire = extensions.get("ASOBO_material_tire")
        if (tire is not None) :
            tireDetailsTexture = tire.get("tireDetailsTexture")
            if (tireDetailsTexture is not None) :
                # MTL_BITMAP_TIREDETAILS
                ret.append( TextureConfig(id=tireDetailsTexture.get("index"), bitmapConfig=BitmapConfig(26, "", False)) )
            tireMudNormalTexture = tire.get("tireMudNormalTexture")
            if (tireMudNormalTexture is not None) :
                # MTL_BITMAP_TIREMUDNORMAL
                ret.append( TextureConfig(id=tireMudNormalTexture.get("index"), bitmapConfig=BitmapConfig(27, "", False)) )

    return ret

def getGltfTextureConfig(gltfPath, textureFolder) :
    """
    Return the texture with bitmap config associated from a gltf
      - getGltfTextureConfig(gltfPath : str) -> dict[str, bitmapConfig=BitmapConfig]
    """
    ret = dict()

    jsonFile = None
    with open(gltfPath, 'r') as file :
        jsonFile = load(file)
    
    materials = jsonFile.get("materials")
    textures = jsonFile.get("textures")
    images = jsonFile.get("images")
    if (materials is None) or (textures is None) or (images is None) :
        gltfLibLogger.info(f"[GLTF] No textures found in {gltfPath}")
        return ret

    for mat in  materials :
        for tex in getMatConfigFromGLTF(mat) :
            imageName = images[textures[tex.id].get("source")].get("uri")
            imageName = basename(imageName)
            if ret.get(imageName) is None :
                ret[imageName] = (tex.bitmapConfig, textureFolder)
            elif not compatibleBitmapIndex(ret[imageName][0].materialBitmap, tex.bitmapConfig.materialBitmap):
                gltfLibLogger.warning(f"[GLTF][WARNING] Same image name for different config : {imageName} \t \
                                        configs : {tex.bitmapConfig.__name__} / {ret[imageName][0].__name__}"
                                    )

    if len(images) > len(ret) :
        gltfLibLogger.warning("[GLTF][WARNING] Some images aren't referenced by any material")
    return ret

def getAllGltfTextureConfig(exportedGltfsParameters) :
    """
    Call getGltfTextureConfig on a list of gltf and merge the results
      - getAllGltfTextureConfig(filenames : list[bundle(glTF)]) -> dict[str, tuple(BitmapConfig, textureFolder)]
    """
    ret = dict()
    textureFolder = ''
    for exportedGltfParameters in exportedGltfsParameters :
        gltfPath = exportedGltfParameters.outputPath
        if exportedGltfParameters.writeTextures:
            textureFolder = exportedGltfParameters.textureFolder
        try :
            textureConfigs = getGltfTextureConfig(gltfPath, textureFolder)
            ret.update(textureConfigs)            
        except :
            gltfLibLogger.error(f"[TEXTURELIB][ERROR] Failed parsing the gltf {gltfPath}")
    return ret
