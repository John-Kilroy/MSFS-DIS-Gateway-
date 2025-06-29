from enum import Enum
from os.path import basename

from pymxs import runtime as rt

from TextureTool2024.TextureLib.BitmapConfig import BitmapConfig

import TextureTool2024.textureUtils as TextureUtils


class MaterialExtensionTypes(Enum):
    Standard = 1
    Decal = 2
    Windshield = 3
    GeoDecalFrosted = 6
    ClearCoat = 7
    ParralaxWindow = 8
    GeoDecal_Dirt = 17
    Tire = 23


class TextureConfig:
    def __init__(self, bitmapConfig = BitmapConfig(), path = "", id = -1):
        self.bitmapConfig = bitmapConfig
        self.path = path
        self.id = id
        
def GetMatConfigFromScene(mat) :
    """
        Materials
    """
    ret = dict()
    ## PBR
    baseColorTexture = mat.BaseColorTex if hasattr(mat, "BaseColorTex") else None
    if (baseColorTexture and baseColorTexture != '') :
        path = TextureUtils.convertAbsolutePathToRelative(baseColorTexture)
        name = basename(path)
        # MTL_BITMAP_DECAL0
        ret[name] = TextureConfig(BitmapConfig(1, "", False), path)
        
    metallicRoughnessTexture = mat.OcclusionRoughnessMetallicTex if hasattr(mat, "OcclusionRoughnessMetallicTex") else None
    if (metallicRoughnessTexture and metallicRoughnessTexture != ''):        
        path = TextureUtils.convertAbsolutePathToRelative(metallicRoughnessTexture)
        name = basename(path)
        # MTL_BITMAP_METAL_ROUGH_AO
        ret[name] = TextureConfig(BitmapConfig(11, "", True), path)
    
    occlusionTexture = mat.OcclusionTex if hasattr(mat, "OcclusionTex") else None
    if (occlusionTexture and occlusionTexture != '') :
        path = TextureUtils.convertAbsolutePathToRelative(occlusionTexture)
        name = basename(path)
        ret[name] = TextureConfig(BitmapConfig(14, "", True), path)

    normalTexture = mat.NormalTex if hasattr(mat, "NormalTex") else None
    if (normalTexture and normalTexture != '') :
        path = TextureUtils.convertAbsolutePathToRelative(normalTexture)
        name = basename(path)
        # MTL_BITMAP_NORMAL
        ret[name] = TextureConfig(BitmapConfig(3, "", False), path)

    emissiveTexture = mat.EmissiveTex if hasattr(mat, "EmissiveTex") else None
    if (emissiveTexture and emissiveTexture != ''):
        path = TextureUtils.convertAbsolutePathToRelative(emissiveTexture)
        name = basename(path)
        # MTL_BITMAP_EMISSIVE
        ret[name] = TextureConfig(BitmapConfig(7, "", False), path)

    """ 
        Extensions 
    """

    """ Tree """
    foliageMaskTexture = mat.FoliageMaskTex if hasattr(mat, "FoliageMaskTex") else None
    foliageMaskTexBool = foliageMaskTexture and foliageMaskTexture != ''
    if (foliageMaskTexBool):
        path = TextureUtils.convertAbsolutePathToRelative(foliageMaskTexture)
        name = basename(path)
        # MTL_BITMAP_ALPHABLENDMASK
        ret[name] = TextureConfig(BitmapConfig(21, "", False), path)

    """ Iridescent """
    iridescentThicknessTexture = mat.IridescentThicknessTex if hasattr(mat, "iridescentThicknessTex") else None
    iridescentThicknessTexBool = iridescentThicknessTexture and iridescentThicknessTexture != ''
    if (iridescentThicknessTexBool):
        path = TextureUtils.convertAbsolutePathToRelative(iridescentThicknessTexture)
        name = basename(path)
        # MTL_BITMAP_IRIDESCENTTHICKNESS
        ret[name] = TextureConfig(BitmapConfig(22, "", False), path)
    
    """ Detail Map """ 
    blendMaskTexture = mat.BlendMaskTex if hasattr(mat, "BlendMaskTex") else None
    detailColorTexture = mat.DetailColorTex if hasattr(mat, "DetailColorTex") else None
    detailNormalTexture = mat.DetailNormalTex if hasattr(mat, "DetailNormalTex") else None
    detailMetalRoughAOTexture = mat.DetailOcclusionRoughnessMetallicTex if hasattr(mat, "DetailOcclusionRoughnessMetallicTex") else None
    
    blendMaskTextureBool = blendMaskTexture and blendMaskTexture != ''
    if (blendMaskTextureBool):
        path = TextureUtils.convertAbsolutePathToRelative(blendMaskTexture)
        name = basename(path)
        # MTL_BITMAP_BLENDMASK
        ret[name] = TextureConfig(BitmapConfig(2, "", False), path)
        
    if (detailColorTexture and detailColorTexture != ''):
        path = TextureUtils.convertAbsolutePathToRelative(detailColorTexture)
        name = basename(path)
        if (blendMaskTextureBool):
            # MTL_BITMAP_ADD_DECAL0
            ret[name] = TextureConfig(BitmapConfig(5, "", False), path)
        else:
            # MTL_BITMAP_DETAILDIFFUSE
            ret[name] = TextureConfig(BitmapConfig(8, "", False), path)
    
    if (detailNormalTexture and detailNormalTexture != ''):
        path = TextureUtils.convertAbsolutePathToRelative(detailNormalTexture)
        name = basename(path)
        if (blendMaskTextureBool):
            # MTL_BITMAP_ADD_NORMAL
            ret[name] = TextureConfig(BitmapConfig(6, "", False), path)
        else:
            # MTL_BITMAP_DETAILNORMAL
            ret[name] = TextureConfig(BitmapConfig(9, "", False), path)
    
    if (detailMetalRoughAOTexture and detailMetalRoughAOTexture != ''):
        path = TextureUtils.convertAbsolutePathToRelative(detailMetalRoughAOTexture)
        name = basename(path)
        if (blendMaskTextureBool):
            # MTL_BITMAP_ADD_METAL_ROUGH_AO
            ret[name] = TextureConfig(BitmapConfig(13, "", True), path)
        else:
            # MTL_BITMAP_DETAIL_METAL_ROUGH_AO
            ret[name] = TextureConfig(BitmapConfig(12, "", True), path)
            
    """ Anisotropic """
    anisotropicTexture = mat.AnisoDirectionRoughnessTex if hasattr(mat, "AnisoDirectionRoughnessTex") else None
    if (anisotropicTexture and anisotropicTexture != ''):
        path = TextureUtils.convertAbsolutePathToRelative(anisotropicTexture)
        name = basename(path)
        # MTL_BITMAP_ANISO_DIR_ROUGH
        ret[name] = TextureConfig(BitmapConfig(17, "", True), path)
    
    matExtension = mat.materialType if hasattr(mat, "materialType") else None
    if (matExtension is not None):
        if (matExtension == MaterialExtensionTypes.ParralaxWindow.value): 
            """ ParralaxWindow """
            parallaxWindow = mat.DetailColorTex if hasattr(mat, "DetailColorTex") else None
            if (parallaxWindow and parallaxWindow != '') :
                path = TextureUtils.convertAbsolutePathToRelative(parallaxWindow)
                name = basename(path)
                # MTL_BITMAP_ADD_DECAL0
                ret[name] = TextureConfig(BitmapConfig(5, "", False), path)
        
        if (matExtension == MaterialExtensionTypes.Windshield.value):
            """ Windshield """
            wiperMaskTexture = mat.WiperMaskTex if hasattr(mat, "WiperMaskTex") else None
            if (wiperMaskTexture and wiperMaskTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(wiperMaskTexture)
                name = basename(path)
                # MTL_BITMAP_WIPERMASK
                ret[name] = TextureConfig(BitmapConfig(18, "", False), path)

            windshieldDetailNormalTexture = mat.WindshieldDetailNormalTex if hasattr(mat, "WindshieldDetailNormalTex") else None
            if (windshieldDetailNormalTexture and windshieldDetailNormalTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(windshieldDetailNormalTexture)
                name = basename(path)
                # MTL_BITMAP_WINDSHIELDDETAILNORMAL
                ret[name] = TextureConfig(BitmapConfig(19, "", False), path)

            scratchesNormalTexture = mat.ScratchesNormalTex if hasattr(mat, "ScratchesNormalTex") else None
            if (scratchesNormalTexture and scratchesNormalTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(scratchesNormalTexture)
                name = basename(path)
                # MTL_BITMAP_SCRATCHESNORMAL
                ret[name] = TextureConfig(BitmapConfig(20, "", False), path)

            windshieldInsectsTexture = mat.WindshieldInsectsTex if hasattr(mat, "WindshieldInsectsTex") else None
            if (windshieldInsectsTexture and windshieldInsectsTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(windshieldInsectsTexture)
                name = basename(path)
                # MTL_BITMAP_WINDSHIELDINSECTS
                ret[name] = TextureConfig(BitmapConfig(23, "", False), path)

            windshieldInsectsMaskTexture = mat.WindshieldInsectsMaskTex if hasattr(mat, "WindshieldInsectsMaskTex") else None
            if (windshieldInsectsMaskTexture and windshieldInsectsMaskTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(windshieldInsectsMaskTexture)
                name = basename(path)
                # MTL_BITMAP_WINDSHIELDINSECTSMASK
                ret[name] = TextureConfig(BitmapConfig(24, "", False), path)
                
        if (matExtension == MaterialExtensionTypes.ClearCoat.value):
            """" ClearCoat """
            clearcoatColorRoughnessTexture = mat.ClearcoatColorRoughnessTex if hasattr(mat, "ClearcoatColorRoughnessTex") else None
            if (clearcoatColorRoughnessTexture and clearcoatColorRoughnessTexture != ''):
                # MTL_BITMAP_CLEARCOATCOLORROUGHNESS
                path = TextureUtils.convertAbsolutePathToRelative(clearcoatColorRoughnessTexture)
                name = basename(path)
                ret[name] = TextureConfig(BitmapConfig(15, "", False), path)
                
            clearcoatNormalTexture = mat.ClearcoatNormalTex if hasattr(mat, "ClearcoatNormalTex") else None
            if (clearcoatNormalTexture and clearcoatNormalTexture != ''):
                # MTL_BITMAP_CLEARCOATNORMAL
                path = TextureUtils.convertAbsolutePathToRelative(clearcoatNormalTexture)
                name = basename(path)
                ret[name] = TextureConfig(BitmapConfig(16, "", False), path)
                
        if (matExtension == MaterialExtensionTypes.Decal.value \
           or matExtension == MaterialExtensionTypes.GeoDecalFrosted.value \
           or matExtension == MaterialExtensionTypes.GeoDecal_Dirt.value): 
            """ Decal, GeoDecalFrosted, GeoDecal_Dirt """            
            dirtMaskTexture = mat.DirtTex if hasattr(mat, "DirtTex") else None
            if (dirtMaskTexture and dirtMaskTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(dirtMaskTexture)
                name = basename(path)
                # MTL_BITMAP_DIRT
                ret[name] = TextureConfig(BitmapConfig(4, "", False), path)

        if(matExtension == MaterialExtensionTypes.Standard.value \
            or matExtension == MaterialExtensionTypes.ClearCoat.value ): 
            """ Standard, ClearCoat """
            dirtTexture = mat.DirtTex if hasattr(mat, "DirtTex") else None
            if (dirtTexture is not None and dirtTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(dirtTexture)
                name = basename(path)
                # MTL_BITMAP_DIRTOVERLAY
                ret[name] = TextureConfig(BitmapConfig(28, "", False), path)

            dirtOcclusionRoughnessMetallicTexture = mat.DirtOcclusionRoughnessMetallicTex if hasattr(mat, "DirtOcclusionRoughnessMetallicTex") else None
            if (dirtOcclusionRoughnessMetallicTexture is not None and dirtOcclusionRoughnessMetallicTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(dirtOcclusionRoughnessMetallicTexture)
                name = basename(path)
                # MTL_BITMAP_DIRT_METAL_ROUGH_AO
                ret[name] = TextureConfig(BitmapConfig(25, "", False), path)

        if(matExtension == MaterialExtensionTypes.Tire.value): 
            """ Tire """            
            tireDetailsTexture = mat.TireDetailsTex if hasattr(mat, "TireDetailsTex") else None
            if (tireDetailsTexture is not None and tireDetailsTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(tireDetailsTexture)
                name = basename(path)
                # MTL_BITMAP_TIREDERAILS
                ret[name] = TextureConfig(BitmapConfig(26, "", False), path)
            tireMudNormalTexture = mat.TireMudNormalTex if hasattr(mat, "TireMudNormalTex") else None
            if (tireMudNormalTexture is not None and tireMudNormalTexture != ''):
                path = TextureUtils.convertAbsolutePathToRelative(tireMudNormalTexture)
                name = basename(path)
                # MTL_BITMAP_TIREMUDNORMAL
                ret[name] = TextureConfig(BitmapConfig(27, "", False), path)

    return ret