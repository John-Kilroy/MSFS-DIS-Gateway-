# Copyright 2023-2024 The glTF-Blender-IO-MSFS2024 authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum

#region properties
class MSFS2024_MaterialTypes(Enum):
    standard = "msfs_standard"
    decal = "msfs_decal"
    windshield = "msfs_windshield"
    porthole = "msfs_porthole"
    glass = "msfs_glass"
    geoDecalFrosted = "msfs_geo_decal_frosted"
    clearcoat = "msfs_clearcoat"
    parallaxWindow = "msfs_parallax_window"
    anisotripic = "msfs_anisotropic"
    hair = "msfs_hair"
    subSurfaceScattering = "msfs_sss"
    invisible = "msfs_invisible"
    fakeTerrain = "msfs_fake_terrain"
    fresnelFade ="msfs_fresnel_fade"
    environmentOccluder = "msfs_environment_occluder"
    ghost = "msfs_ghost"
    geoDecalBlendMasked = "msfs_geo_decal_blendmasked"
    sail = "msfs_sail"
    propeller = "msfs_propeller"
    tree = "msfs_tree"
    vegetation = "msfs_vegetation"

class MSFS2024_MaterialProperties(Enum):
    """
        Enum describing the parameters of materials contains Tuples of:
        ( 
            The name that appears in the UI, 
            Default Value, 
            attribute name of the property, 
            name that appear in the extension when it's exported/imported
        )
    """

    ## Parameters
    materialType = "Material Type", "NONE", "msfs_material_type", None
    alphaMode = "Alpha Mode", "OPAQUE", "msfs_alpha_mode", None

    baseColor = "Base Color", [1.0, 1.0, 1.0, 1.0], "msfs_base_color_factor", None
    emissiveColor = "Emissive Color", [0.0, 0.0, 0.0], "msfs_emissive_factor", None
    sssColor = "Sub-Surface Scattering Color", [1.0, 1.0, 1.0, 1.0], "msfs_sss_color", "SSSColor"
    metallicScale = "Metallic Factor", 1.0, "msfs_metallic_factor", None
    roughnessScale = "Roughness Factor", 1.0, "msfs_roughness_factor", None
    normalScale = "Normal Scale", 1.0, "msfs_normal_scale", None
    emissiveScale = "Emissive Scale", 1.0, "msfs_emissive_scale", None
    occlusionStrength = "Occlusion Strength", 1.0, "msfs_occlusion_strength", "strength"
    alphaCutoff = "Alpha Cutoff", 0.5, "msfs_alpha_cutoff", None

    baseColorBlendFactor = "Base Color Blend Factor", 1.0, "msfs_base_color_blend_factor", "baseColorBlendFactor"
    metallicBlendFactor = "Metallic Blend Factor", 1.0, "msfs_metallic_blend_factor", "metallicBlendFactor"
    roughnessBlendFactor = "Roughness Blend Factor", 1.0, "msfs_roughness_blend_factor", "roughnessBlendFactor"
    normalBlendFactor = "Normal Blend Factor", 1.0, "msfs_normal_blend_factor", "normalBlendFactor"
    emissiveBlendFactor = "Emissive Blend Factor", 1.0, "msfs_emissive_blend_factor", "emissiveBlendFactor"
    occlusionBlendFactor = "Occlusion Blend Factor", 1.0, "msfs_occlusion_blend_factor", "occlusionBlendFactor"
    normalOverrideFactor = "Normal Mode Tangent/Override", 1.0, "msfs_normal_override_blend_factor", "normalOverrideFactor"
    decalblendSharpness = "Decal Blend Mask Sharpness", 1.0, "msfs_decal_blend_sharpness", "blendSharpnessFactor"
    decalblendMaskedThreshold = "Decal Blend Mask Threshold", 0.0, "msfs_decal_blend_masked_threshold", ""
    decalFreezeFactor = "Freeze Factor", 0.0, "msfs_decal_freeze_factor", ""
    decalMode = "Decal Mode", "default", "msfs_decal_mode", "mode"
    underClearCoat = "Render Under Clearcoat", True, "msfs_under_clearcoat", "underClearcoat"

    drawOrderOffset = "Draw Order Offset", 0, "msfs_draw_order_offset", "drawOrderOffset"
    noCastShadow = "Don't Cast Shadows", False, "msfs_no_cast_shadow", "noCastShadow"
    dayNightCycle = "Day Night Cycle", False, "msfs_day_night_cycle", None
    disableMotionBlur = "Disable Motion Blur", False, "msfs_disable_motion_blur", "enabled"
    doubleSided = "Double Sided", False, "msfs_double_sided", None
    flipBackFaceNormal = "Flip Back Face Normal", False, "msfs_flip_back_face_normal", None
    
    clampUVX = "Clamp UV U", False, "msfs_clamp_uv_x", "clampUVX"
    clampUVY = "Clamp UV V", False, "msfs_clamp_uv_y", "clampUVY"
    uvOffsetU = "UV Offset U", 0.0, "msfs_uv_offset_u", "UVOffsetU"
    uvOffsetV = "UV Offset V", 0.0, "msfs_uv_offset_v", "UVOffsetV"
    uvTilingU = "UV Tiling U", 1.0, "msfs_uv_tiling_u", "UVTilingU" 
    uvTilingV = "UV Tiling V", 1.0, "msfs_uv_tiling_v", "UVTilingV"
    uvRotation = "UV Rotation", 0.0, "msfs_uv_rotation", "UVRotation"
    
    detailUVScale = "Detail UV Scale", 1.0, "msfs_detail_uv_scale", "UVScale"
    detailBlendThreshold = "Blend Mask Threshold", 0.001, "msfs_detail_blend_threshold", "blendThreshold"
    detailNormalScale = "Detail Normal Scale", 1.0, "msfs_detail_normal_scale", "scale"

    wearOverlayUVScale = "Wear Overlay UV Scale", 1.0, "msfs_wear_overlay_uv_scale", "dirtUvScale"
    wearBlendSharpness = "Wear Blend Sharpness", 0.0, "msfs_wear_blend_sharpness", "dirtBlendSharpness"
    wearAmount = "Wear Amount", 0.0, "msfs_wear_amount", "dirtBlendAmount"

    collisionMaterial = "Collision Material", False, "msfs_collision_material"
    roadCollisionMaterial = "Road Collision Material", False, "msfs_road_collision_material"

    ghostBias = "Ghost Bias", 1.0, "msfs_ghost_bias", "bias"
    ghostScale = "Ghost Scale", 0.0, "msfs_ghost_scale", "scale"
    ghostPower = "Ghost Power", 0.0, "msfs_ghost_power", "power"

    sailLightAbsorption = "Light Absorption", 1.0, "msfs_sail_light_absorption", "sailLightAbsorption"

    receiveRain = "Receive Rain", False, "msfs_receive_rain", None
    rainDropTiling = "Rain Drop Tiling", 1.0, "msfs_rain_drop_tiling", "rainDropScale"
    rainOnBackFace = "Rain On BackFace", False, "msfs_rain_on_backface", "rainDropSide"

    usePearlEffect = "Use Pearl Effect", False, "msfs_use_pearl", None
    pearlColorShift = "Pearl Color Shift", 0.0, "msfs_pearl_shift", "pearlShift"
    pearlColorRange = "Pearl Color Range", 0.0, "msfs_pearl_range", "pearlRange"
    pearlColorBrightness = "Pearl Color Brightness", 0.0, "msfs_pearl_brightness", "pearlBrightness"

    fresnelFactor = "Fresnel Factor", 1.0, "msfs_fresnel_factor", "fresnelFactor"
    fresnelOpacityBias = "Fresnel Opacity Bias", 1.0, "msfs_fresnel_opacity_offset", "fresnelOpacityOffset"

    parallaxRoomSizeX = "Room Scale X", 0.5, "msfs_parallax_room_size_x", "roomSizeXScale"
    parallaxRoomSizeY = "Room Scale Y", 0.5, "msfs_parallax_room_size_y", "roomSizeYScale"
    parallaxRoomSizeZ = "Room Scale Z", 0.0, "msfs_parallax_room_size_z", "parallaxScale"
    parallaxRoomCount = "Room Count", 5, "msfs_parallax_room_count_xy", "roomNumberXY"
    parallaxCorridor = "Corridor", False, "msfs_parallax_corridor", "corridor"

    glassWidth = "Glass Width (mm)", 0.0, "msfs_glass_width", "glassWidth"

    clearcoatRoughnessFactor = "Clearcoat Roughness Factor", 1.0, "msfs_clearcoat_roughness_factor", "clearcoatRoughnessFactor"
    clearcoatNormalFactor = "Clearcoat Normal Factor", 1.0, "msfs_clearcoat_normal_factor", "clearcoatNormalFactor"
    clearcoatColorRoughnessTiling = "Clearcoat Color/Roughness Tiling", 1.0, "msfs_clearcoat_color_roughness_tiling", "clearcoatColorRoughnessTiling"
    clearcoatNormalTiling = "Clearcoat Normal Tiling", 1.0, "msfs_clearcoat_normal_tiling", "clearcoatColorNormalTiling"
    clearcoatInverseRoughness = "Clearcoat Inverse Roughness", False, "msfs_clearcoat_inverse_roughness", "clearcoatInverseRoughness"
    clearcoatBaseRoughness = "Base Roughness", 0.5, "msfs_clearcoat_base_roughness", "clearcoatBaseRoughness"

    windshieldDetailRoughness1 = "Detail 1 (R) Roughness", 0.1, "msfs_windshield_detail_rough_1", "detail1Rough"
    windshieldDetailRoughness2 = "Detail 2 (B) Roughness", 0.1, "msfs_windshield_detail_rough_2", "detail2Rough"
    windshieldDetailOpacity1 = "Detail 1 (R) Opacity", 0.5, "msfs_windshield_detail_opacity_1", "detail1Opacity"
    windshieldDetailOpacity2 = "Detail 2 (B) Opacity", 0.5, "msfs_windshield_detail_opacity_2", "detail2Opacity"
    windshieldMicroScratchTiling = "Micro-Scratches Tiling", 1.0, "msfs_windshield_micro_scratches_tiling", "microScratchesTiling"
    windshieldMicroScratchStrength = "Micro-Scratches Strength", 1.0, "msfs_windshield_micro_scratches_strength", "microScratchesStrength"
    windshieldDetailNormalRefractScale = "Detail Normal Refraction Strength", 1.0, "msfs_windshield_detail_normal_refract_scale", "detailNormalRefractScale"
    windshieldWiperLines = "Wiper Lines", False, "msfs_windshield_wiper_lines", "wiperLines"
    windshieldWiperLinesTiling = "Wiper Lines Tiling", 1.0, "msfs_windshield_wiper_lines_tiling", "wiperLinesTiling"
    windshieldWiperLinesStrength = "Wiper Lines Strength", 1.0, "msfs_windshield_wiper_lines_strength", "microScratchesStrength"
    windshieldWiper1State = "Wiper 1 State", 0.0, "msfs_windshield_wiper_1_state", "wiper1State"
    windshieldReflectionMaskStrength = "Reflection Mask Strength", 1.0, "msfs_occlusion_strength", "strength"

    useIridescent = "Use Iridescent Parameters", False, "msfs_use_iridescent", None
    iridescentMinThickness = "Min Thickness", 400.0, "msfs_iridescent_min_thickness", "iridescentMinThickness"
    iridescentMaxThickness = "Max Thickness", 400.0, "msfs_iridescent_max_thickness", "iridescentMaxThickness"
    iridescentBrightness = "Brightness", 1.0, "msfs_iridescent_brightness", "iridescentBrightness"

    ## Textures
    baseColorTexture = "Base Color Texture (RGBA)", None, "msfs_base_color_texture", None
    omrTexture = "Occlusion (R), Roughness (G), Metallic (B)", None, "msfs_occlusion_metallic_roughness_texture", None
    normalTexture = "Normal Texture (RGB)", None, "msfs_normal_texture", None
    emissiveTexture = "Emissive Texture (RGB)", None, "msfs_emissive_texture", None

    detailColorTexture = "Detail Color (RGB), Alpha (A)", None, "msfs_detail_color_texture", "detailColorTexture"
    detailOmrTexture = "Detail Occlusion (R), Roughness (G), Metallic (B)", None, "msfs_detail_occlusion_metallic_roughness_texture", "detailMetalRoughAOTexture"
    detailNormalTexture = "Detail Normal Texture", None, "msfs_detail_normal_texture", "detailNormalTexture"

    blendMaskTexture = "Blend Mask Texture", None, "msfs_blend_mask_texture", "blendMaskTexture"
    occlusionUV2 = "Occlusion (UV2)", None, "msfs_occlusion_uv2", "extraOcclusionTexture"
    
    decalBlendMaskTexture = "Decal Blend Mask Texture", None, "msfs_decal_blend_mask_texture", "blendMaskTexture"
    decalSecondaryColorTexture = "Secondary Color (RGBA), Alpha (A)", None, "msfs_detail_color_texture", "detailColorTexture"
    decalSecondaryOmrTexture = "Secondary Occlusion (R), Roughness (G), Metallic (B)", None, "msfs_detail_occlusion_metallic_roughness_texture", "detailMetalRoughAOTexture"
    decalSecondaryTexture = "Secondary Normal", None, "msfs_detail_normal_texture", "detailNormalTexture"
    decalMeltRoughnessMetallicTexture = "Melt Pattern (R) Roughness (G) Metallic (B)", None, "msfs_detail_occlusion_metallic_roughness_texture", "detailMetalRoughAOTexture"

    clearcoatColorRoughnessTexture = "Clearcoat amount (R), Clearcoat rough (G)", None, "msfs_clearcoat_color_roughness_texture", "clearcoatColorRoughnessTexture"
    clearcoatNormalTexture = "Clearcoat Normal", None, "msfs_clearcoat_normal_texture", "clearcoatNormalTexture"

    frontGlassColorTexture = "Front Glass Color Texture", None, "msfs_base_color_texture", None
    frontGlassNormalTexture = "Front Glass Normal Texture", None, "msfs_normal_texture", None
    emissiveInsideWindowTexture = "Emissive Inside Window Texture", None, "msfs_emissive_texture", None
    behindGlassColorTexture = "Behind Glass Color Texture", None, "msfs_behind_glass_color_texture", "behindWindowMapTexture"

    opacityTexture = "Opacity", None, "msfs_opacity_texture", "opacityTexture"

    occAnisoRoughXMetalicTexture = "Occlusion (R), Anisotropic Roughness X (G), Metallic (B)", None, "msfs_occlusion_metallic_roughness_texture", None
    anisoDirectionRoughnessTexture = "Anisotropic Direction (RG), Roughness Y (B)", None, "msfs_anisotropic_direction_roughnessy_texture", "anisoDirectionRoughnessTexture"

    wearAlbedoMaskTexture = "Wear Albedo (RGB), Mask (A)", None, "msfs_wear_albedo_mask", "dirtTexture"
    wearOmrIntensityTexture = "Wear Occlusion (R), Roughness (G), Metallic (B), Intensity (A)", None, "msfs_wear_omr_intensity", "dirtOcclusionRoughnessMetallicTexture"

    windshieldWiperMaskTexture = "Wiper Mask (RGBA)", None, "msfs_windshield_wiper_mask_texture", "wiperMaskTexture"
    windshieldReflectionRoughnessMetallicTexture = "Reflection (R) Roughness (G) Metallic (B)", None, "msfs_occlusion_metallic_roughness_texture", None
    windshiledDetailNormalTexture = "Detail Normal (use Detail UV Tiling)", None, "msfs_windshield_detail_normal_texture", "windshieldDetailNormalTexture"
    windshieldScrachesNormaltexture = "Scratches Normal", None, "msfs_windshield_scratches_normal_texture", "scratchesNormalTexture"
    windshieldInsectsAlbedoTexture = "Insects Albedo (RGBA)", None, "msfs_windshield_insects_albedo_texture", "windshieldInsectsTexture"
    windshieldInsectsMaskTexture = "Insects Mask (A)", None, "msfs_windshield_insects_mask_texture", "windshieldInsectsMaskTexture"
    windshieldSecondaryDetailsTexture = "Secondary Details (RGBA)", None, "msfs_emissive_texture", None
    details1IcingMaskDetails2Texture = "Details 1 (R), Icing Mask (G), Details 2 (B)", None, "msfs_detail_color_texture", "detailColorTexture"
    detailswindshieldReflectionRoughnessMetallicTexture = "Details Reflection (R) Roughness (G) Metallic (B)", None, "msfs_detail_occlusion_metallic_roughness_texture", "detailMetalRoughAOTexture"
    icingNormalTexture = "Icing Normal (use UV Detail Tiling)", None, "msfs_detail_normal_texture", "detailNormalTexture"
    reflectionMaskTexture = "Reflection Mask (UV2)", None, "msfs_occlusion_uv2", "extraOcclusionTexture"
    iridescentThicknessTexture = "Iridescent Thickness (R)", None, "msfs_iridescent_thickness_texture", "iridescentThicknessTexture"

    foliageMaskTexture = "Foliage Mask (R) Transluency (G) WindMask (B)", None, "msfs_foliage_mask_texture", "foliageMaskTexture"

    def name(self):
        assert type(self.value) is tuple and len(self.value) > 0
        if type(self.value) is tuple and len(self.value) > 0:
            return self.value[0]
        return None

    def defaultValue(self):
        assert type(self.value) is tuple and len(self.value) > 1
        if type(self.value) is tuple and len(self.value) > 1:
            return self.value[1]
        return None

    def attributeName(self):
        assert type(self.value) is tuple and len(self.value) > 2
        if type(self.value) is tuple and len(self.value) > 2:
            return self.value[2]
        return None

    def extensionName(self):
        assert type(self.value) is tuple and len(self.value) > 3
        if type(self.value) is tuple and len(self.value) > 3:
            return self.value[3]
        return None
#endregion

#region properties UI
class MSFS2024_MaterialUtilsUI:

    @staticmethod
    def draw_prop(layout, material, property, text="", enabled=True):
        column = layout.column()
        if text:
            column.prop(material, property, text=text)
        else:
            column.prop(material, property)

        column.enabled = enabled
        return column
    
    @staticmethod
    def draw_texture_prop(layout, material, property, text="", enabled=True):
        column = layout.column()
        if text:
            column.label(text=text)

        column.template_ID(material, property, new="image.new", open="image.open")
        column.enabled = enabled
        return column
    
    ## Parameters
    @staticmethod
    def drawBaseColorProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material, 
            property = MSFS2024_MaterialProperties.baseColor.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawEmissiveColorProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material, 
            property = MSFS2024_MaterialProperties.emissiveColor.attributeName(),
            text = text
        )

    @staticmethod
    def drawAlphaModeProp(layout, material, text=""):
        box = layout.box()
        box.label(text="Alpha Mode")

        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.alphaMode.attributeName(),
            text = text
        )

    @staticmethod
    def drawOrderOffsetProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.drawOrderOffset.attributeName(),
            text = text
        )

    @staticmethod
    def drawNoCastShadowProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.noCastShadow.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawDoubleSidedProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.doubleSided.attributeName(),
            text = text
        )

    @staticmethod
    def drawFlipBackFaceNormalProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.flipBackFaceNormal.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawDayNightCycleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.dayNightCycle.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawMotionBlurProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.disableMotionBlur.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawCollisionProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.collisionMaterial.attributeName(),
            text = text
        )

    @staticmethod
    def drawRoadCollisionProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.roadCollisionMaterial.attributeName(),
            text = text
        )

    @staticmethod
    def drawGameplayPanel(layout, material):
        box = layout.box()
        box.label(text="Gameplay Parameters")

        MSFS2024_MaterialUtilsUI.drawCollisionProp(box, material, MSFS2024_MaterialProperties.collisionMaterial.name())
        MSFS2024_MaterialUtilsUI.drawRoadCollisionProp(box, material, MSFS2024_MaterialProperties.roadCollisionMaterial.name())

    @staticmethod
    def drawUVOffsetUProp(layout, material, text=""):
        layout.use_property_decorate = True
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.uvOffsetU.attributeName(),
            text = text
        )

    @staticmethod
    def drawUVOffsetVProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.uvOffsetV.attributeName(),
            text = text
        )

    @staticmethod
    def drawTilingUProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.uvTilingU.attributeName(),
            text = text
        )

    @staticmethod
    def drawTilingVProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.uvTilingV.attributeName(),
            text = text
        )

    @staticmethod
    def drawClampUVXProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.clampUVX.attributeName(),
            text = text
        )

    @staticmethod
    def drawClampUVYProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.clampUVY.attributeName(),
            text = text
        )

    @staticmethod
    def drawUVRotationProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.uvRotation.attributeName(),
            text = text
        )

    @staticmethod
    def drawUVPanel(layout, material):
        box = layout.box()
        box.label(text="UV Options")

        MSFS2024_MaterialUtilsUI.drawUVOffsetUProp(box, material, MSFS2024_MaterialProperties.uvOffsetU.name())
        MSFS2024_MaterialUtilsUI.drawUVOffsetVProp(box, material, MSFS2024_MaterialProperties.uvOffsetV.name())
        MSFS2024_MaterialUtilsUI.drawTilingUProp(box, material, MSFS2024_MaterialProperties.uvTilingU.name())
        MSFS2024_MaterialUtilsUI.drawTilingVProp(box, material, MSFS2024_MaterialProperties.uvTilingV.name())
        MSFS2024_MaterialUtilsUI.drawUVRotationProp(box, material, MSFS2024_MaterialProperties.uvRotation.name())
        MSFS2024_MaterialUtilsUI.drawClampUVXProp(box, material, MSFS2024_MaterialProperties.clampUVX.name())
        MSFS2024_MaterialUtilsUI.drawClampUVYProp(box, material, MSFS2024_MaterialProperties.clampUVY.name())
    
    @staticmethod
    def drawMetallicScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.metallicScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawRoughnessScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.roughnessScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawOcclusionStrengthProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.occlusionStrength.attributeName(),
            text = text
        )

    @staticmethod
    def drawNormalScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.normalScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawEmissiveScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.emissiveScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawAlphaCutoffProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.alphaCutoff.attributeName(),
            text = text
        )

    @staticmethod
    def drawDetailUVScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.detailUVScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawDetailNormalScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.detailNormalScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawBlendThresholdProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.detailBlendThreshold.attributeName(),
            text = text
        )

    @staticmethod
    def drawWearOverlayUVScaleProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.wearOverlayUVScale.attributeName(),
            text = text
        )

    @staticmethod
    def drawWearBlendSharpnessProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.wearBlendSharpness.attributeName(),
            text = text
        )

    @staticmethod
    def drawWearAmountProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.wearAmount.attributeName(),
            text = text
        )

    @staticmethod
    def drawSSSColorProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.sssColor.attributeName(),
            text = text
        )

    @staticmethod
    def drawReceiveRainProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.receiveRain.attributeName(),
            text = text
        )

    @staticmethod
    def drawRainDropTilingProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.rainDropTiling.attributeName(),
            text = text
        )

    @staticmethod
    def drawRainOnBackFaceProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.rainOnBackFace.attributeName(),
            text = text
        )


    ## Textures
    @staticmethod
    def drawBaseColorTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.baseColorTexture.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawOmrTextureProp(layout, material, text =""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.omrTexture.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawNormalTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.normalTexture.attributeName(),
            text = text
        )
    
    @staticmethod
    def drawEmissiveTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout,
            material = material, 
            property = MSFS2024_MaterialProperties.emissiveTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawDetailColorTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout,
            material = material, 
            property = MSFS2024_MaterialProperties.detailColorTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawDetailOmrTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.detailOmrTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawDetailNormalTexture(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.detailNormalTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawBlendMaskTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.blendMaskTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawDecalBlendMaskTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.decalBlendMaskTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawOcclusionUV2TextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.occlusionUV2.attributeName(),
            text = text
        )

    @staticmethod
    def drawWearAlbedoMaskTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.wearAlbedoMaskTexture.attributeName(),
            text = text
        )

    @staticmethod
    def drawWearOmrIntensityTextureProp(layout, material, text=""):
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = layout, 
            material = material, 
            property = MSFS2024_MaterialProperties.wearOmrIntensityTexture.attributeName(),
            text = text
        )
#endregion