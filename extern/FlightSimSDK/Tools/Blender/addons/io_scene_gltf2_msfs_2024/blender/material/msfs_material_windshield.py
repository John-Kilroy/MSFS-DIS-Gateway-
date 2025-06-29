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
from ..utils.msfs_material_utils import (MSFS2024_MaterialProperties,
                                         MSFS2024_MaterialUtilsUI)
from .msfs_material import MSFS2024_Material


class MSFS2024_Windshield(MSFS2024_Material):

    attributes = [
        MSFS2024_MaterialProperties.baseColor,
        MSFS2024_MaterialProperties.emissiveColor,
        MSFS2024_MaterialProperties.emissiveScale,
        MSFS2024_MaterialProperties.drawOrderOffset,
        MSFS2024_MaterialProperties.noCastShadow,
        MSFS2024_MaterialProperties.doubleSided,
        MSFS2024_MaterialProperties.disableMotionBlur,
        MSFS2024_MaterialProperties.flipBackFaceNormal,
        MSFS2024_MaterialProperties.metallicScale,
        MSFS2024_MaterialProperties.roughnessScale,
        MSFS2024_MaterialProperties.occlusionStrength,
        MSFS2024_MaterialProperties.normalScale,
        MSFS2024_MaterialProperties.detailUVScale,
        MSFS2024_MaterialProperties.detailNormalScale,
        MSFS2024_MaterialProperties.detailBlendThreshold,

        MSFS2024_MaterialProperties.uvOffsetU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvTilingU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvRotation,
        MSFS2024_MaterialProperties.clampUVX,
        MSFS2024_MaterialProperties.clampUVY,

        MSFS2024_MaterialProperties.collisionMaterial,
        MSFS2024_MaterialProperties.roadCollisionMaterial,

        MSFS2024_MaterialProperties.receiveRain,
        MSFS2024_MaterialProperties.rainDropTiling,
        MSFS2024_MaterialProperties.rainOnBackFace,

        MSFS2024_MaterialProperties.windshieldDetailRoughness1,
        MSFS2024_MaterialProperties.windshieldDetailRoughness2,
        MSFS2024_MaterialProperties.windshieldDetailOpacity1,
        MSFS2024_MaterialProperties.windshieldDetailOpacity2,
        MSFS2024_MaterialProperties.windshieldMicroScratchTiling,
        MSFS2024_MaterialProperties.windshieldMicroScratchStrength,
        MSFS2024_MaterialProperties.windshieldDetailNormalRefractScale,

        MSFS2024_MaterialProperties.useIridescent,
        MSFS2024_MaterialProperties.iridescentMinThickness,
        MSFS2024_MaterialProperties.iridescentMaxThickness,
        MSFS2024_MaterialProperties.iridescentBrightness,

        MSFS2024_MaterialProperties.baseColorTexture,
        MSFS2024_MaterialProperties.windshieldReflectionRoughnessMetallicTexture,
        MSFS2024_MaterialProperties.normalTexture,
        MSFS2024_MaterialProperties.windshieldSecondaryDetailsTexture,
        MSFS2024_MaterialProperties.details1IcingMaskDetails2Texture,
        MSFS2024_MaterialProperties.detailswindshieldReflectionRoughnessMetallicTexture,
        MSFS2024_MaterialProperties.icingNormalTexture,
        MSFS2024_MaterialProperties.reflectionMaskTexture,
        MSFS2024_MaterialProperties.windshieldWiperMaskTexture,
        MSFS2024_MaterialProperties.detailNormalTexture,
        MSFS2024_MaterialProperties.windshieldScrachesNormaltexture,
        MSFS2024_MaterialProperties.iridescentThicknessTexture,
        MSFS2024_MaterialProperties.windshieldInsectsAlbedoTexture,
        MSFS2024_MaterialProperties.windshieldInsectsMaskTexture
    ]

    def __init__(self, material, buildTree = False):
        super().__init__(material, buildTree)
        if buildTree:
            self.setDefaultProperties()
            self.forceUpdateNodes()

    def customShaderTree(self):
        super(MSFS2024_Windshield, self).defaultShadersTree()

    def setDefaultProperties(self):
        super().setDefaultProperties(self.attributes)
        setattr(self.material, MSFS2024_MaterialProperties.alphaMode.attributeName(), "BLEND")

    def forceUpdateNodes(self):
        super().forceUpdateNodes()

    def setWiperMaskTex(self, tex):
        ## TODO - Add new windshield shader 
        return NotImplementedError
    
    @staticmethod
    def drawPanel(layout, material):
        MSFS2024_Windshield.drawParametersPanel(layout, material)
        MSFS2024_Windshield.drawTexturesPanel(layout, material)

    @staticmethod
    def drawParametersPanel(layout, material):
        ## Base Color
        MSFS2024_MaterialUtilsUI.drawBaseColorProp(
            layout = layout,
            material = material,
            text = MSFS2024_MaterialProperties.baseColor.name()
        )

        ## Emissive Color
        MSFS2024_MaterialUtilsUI.drawEmissiveColorProp(
            layout = layout,
            material = material,
            text = MSFS2024_MaterialProperties.emissiveColor.name()
        )

        ## Emissive Scale
        MSFS2024_MaterialUtilsUI.drawEmissiveScaleProp(
            layout = layout,
            material = material,
            text = MSFS2024_MaterialProperties.emissiveScale.name()
        )

        #### Render parameters ####
        box = layout.box()
        box.label(text="Render Parameters")

        ## Draw Order Offset
        MSFS2024_MaterialUtilsUI.drawOrderOffsetProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.drawOrderOffset.name()
        )

        ## No Cast Shadow
        MSFS2024_MaterialUtilsUI.drawNoCastShadowProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.noCastShadow.name()
        )

        ## Double Sided
        MSFS2024_MaterialUtilsUI.drawDoubleSidedProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.doubleSided.name()
        )
        
        ## Flip Back Face Normal
        if material.msfs_double_sided:
            MSFS2024_MaterialUtilsUI.drawFlipBackFaceNormalProp(
                layout = box,
                material = material,
                text = MSFS2024_MaterialProperties.flipBackFaceNormal.name()
            )

        ## Motion Blur
        MSFS2024_MaterialUtilsUI.drawMotionBlurProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.disableMotionBlur.name()
        )
        #### End Render parameters ####

        #### General parameters ####
        box = layout.box()
        box.label(text="General Parameters")

        ## Metallic Scale
        MSFS2024_MaterialUtilsUI.drawMetallicScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.metallicScale.name()
        )

        ## Roughness Scale
        MSFS2024_MaterialUtilsUI.drawRoughnessScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.roughnessScale.name()
        )

        ## Occlusion Strength
        MSFS2024_MaterialUtilsUI.drawOcclusionStrengthProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.windshieldReflectionMaskStrength.name()
        )

        ## Normal Scale
        MSFS2024_MaterialUtilsUI.drawNormalScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.normalScale.name()
        )

        ## Detail UV Scale
        MSFS2024_MaterialUtilsUI.drawDetailUVScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.detailUVScale.name()
        )
        
        ## Detail Normal Scale
        MSFS2024_MaterialUtilsUI.drawDetailNormalScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.detailNormalScale.name()
        )

        ## Detail Blend Threshold
        MSFS2024_MaterialUtilsUI.drawBlendThresholdProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.detailBlendThreshold.name()
        )
        #### End General parameters ####

        #### UV options ####
        MSFS2024_MaterialUtilsUI.drawUVPanel(
            layout = layout,
            material = material
        )
        #### End UV options ####

        #### Gameplay Parameters ####
        MSFS2024_MaterialUtilsUI.drawGameplayPanel(
            layout = layout,
            material = material
        )
        #### End Gameplay Parameters ####

        #### Rain Options ####
        box = layout.box()
        box.label(text="Rain Parameters")

        ## Receive Rain
        MSFS2024_MaterialUtilsUI.drawReceiveRainProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.receiveRain.name()
        )

        ## Rain Drop Tiling
        MSFS2024_MaterialUtilsUI.drawRainDropTilingProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.rainDropTiling.name()
        )

        MSFS2024_MaterialUtilsUI.drawRainOnBackFaceProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.rainOnBackFace.name()
        )
        #### End Rain Options ####

        #### Windshield Wipers Parameters ####
        if material.msfs_receive_rain:
            box = layout.box()
            box.label(text="Windshield Wipers Parameters")

            ## Windshield Lines
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.windshieldWiperLines.attributeName(),
                text = MSFS2024_MaterialProperties.windshieldWiperLines.name()
            )

            if material.msfs_windshield_wiper_lines:
                ## Windshield Lines Tiling
                MSFS2024_MaterialUtilsUI.draw_prop(
                    layout = box,
                    material = material,
                    property = MSFS2024_MaterialProperties.windshieldWiperLinesTiling.attributeName(),
                    text = MSFS2024_MaterialProperties.windshieldWiperLinesTiling.name()
                )

                ## Windshield Lines Strength
                MSFS2024_MaterialUtilsUI.draw_prop(
                    layout = box,
                    material = material,
                    property = MSFS2024_MaterialProperties.windshieldWiperLinesStrength.attributeName(),
                    text = MSFS2024_MaterialProperties.windshieldWiperLinesStrength.name()
                )
            
            ## Wiper Animation
            box = layout.box()
            box.label(text="Wiper Animation Parameters")

            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.windshieldWiper1State.attributeName(),
                text = MSFS2024_MaterialProperties.windshieldWiper1State.name()
            )
        #### End Windshield Wipers Parameters ####
        
        #### Windshield Parameters ####
        box = layout.box()
        box.label(text="Windshield Parameters")
        
        ## Windshield Detail 1 Rough
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldDetailRoughness1.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldDetailRoughness1.name()
        )

        ## Windshield Detail 2 Rough
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldDetailRoughness2.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldDetailRoughness2.name()
        )

        ## Windshield Detail 1 Opacity
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldDetailOpacity1.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldDetailOpacity1.name()
        )

        ## Windshield Detail 2 Opacity
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldDetailOpacity2.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldDetailOpacity2.name()
        )

        ## Windshield Micro Scratches Tiling
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldMicroScratchTiling.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldMicroScratchTiling.name()
        )

        ## Windshield Micro Scratches Strength
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldMicroScratchStrength.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldMicroScratchStrength.name()
        )

        ## Windshield Detail Normal Refract Scale
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.windshieldDetailNormalRefractScale.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldDetailNormalRefractScale.name()
        )
        #### End Windshield Parameters ####
        
        #### Iridescent Parameters ####
        box = layout.box()
        box.label(text="Iridescent Parameters")

        ## Use Iridescent
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.useIridescent.attributeName(),
            text = MSFS2024_MaterialProperties.useIridescent.name()
        )

        if material.msfs_use_iridescent:
            ## Iridescent Min Thickness
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.iridescentMinThickness.attributeName(),
                text = MSFS2024_MaterialProperties.iridescentMinThickness.name()
            )

            ## Iridescent Max Thickness
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.iridescentMaxThickness.attributeName(),
                text = MSFS2024_MaterialProperties.iridescentMaxThickness.name()
            )

            ## Iridescent Brightness
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.iridescentBrightness.attributeName(),
                text = MSFS2024_MaterialProperties.iridescentBrightness.name()
            )
        #### End Iridescent Parameters ####
        return

    @staticmethod
    def drawTexturesPanel(layout, material):
        box = layout.box()
        box.label(text="Textures")

        ## Base Color Texture
        MSFS2024_MaterialUtilsUI.drawBaseColorTextureProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.baseColorTexture.name()
        )

        ## Reflection (R), Roughness (G), Metallic (B) Texture
        MSFS2024_MaterialUtilsUI.drawOmrTextureProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.windshieldReflectionRoughnessMetallicTexture.name()
        )

        ## Normal Texture
        MSFS2024_MaterialUtilsUI.drawNormalTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.normalTexture.name()
        )

        ## Secondary Details
        MSFS2024_MaterialUtilsUI.drawEmissiveTextureProp(
            layout = box,
            material = material, 
            text = MSFS2024_MaterialProperties.windshieldSecondaryDetailsTexture.name()
        )

        ## Details 1 (R), Icing Mask (G), Details 2 (B)
        MSFS2024_MaterialUtilsUI.drawDetailColorTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.details1IcingMaskDetails2Texture.name()
        )

        ## Details Reflection (R) Roughness (G) Metallic (B)
        MSFS2024_MaterialUtilsUI.drawDetailOmrTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.detailswindshieldReflectionRoughnessMetallicTexture.name()
        )
        
        ## Icing Normal
        MSFS2024_MaterialUtilsUI.drawDetailNormalTexture(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.icingNormalTexture.name()
        )

        ## Reflection Mask (UV2)
        MSFS2024_MaterialUtilsUI.drawOcclusionUV2TextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.reflectionMaskTexture.name()
        )
        
        ## Wiper Mask (RGBA)
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box, 
            material = material, 
            property = MSFS2024_MaterialProperties.windshieldWiperMaskTexture.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldWiperMaskTexture.name()
        )

        ## Detail Normal (use Detail UV Tiling)
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box, 
            material = material, 
            property = MSFS2024_MaterialProperties.windshiledDetailNormalTexture.attributeName(),
            text = MSFS2024_MaterialProperties.windshiledDetailNormalTexture.name()
        )

        ## Scratches Normal
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box, 
            material = material, 
            property = MSFS2024_MaterialProperties.windshieldScrachesNormaltexture.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldScrachesNormaltexture.name()
        )

        if material.msfs_use_iridescent:
            ## Iridescent Thickness (R)
            MSFS2024_MaterialUtilsUI.draw_texture_prop(
                layout = box, 
                material = material, 
                property = MSFS2024_MaterialProperties.iridescentThicknessTexture.attributeName(),
                text = MSFS2024_MaterialProperties.iridescentThicknessTexture.name()
            )

        ## Insects Albedo
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box, 
            material = material, 
            property = MSFS2024_MaterialProperties.windshieldInsectsAlbedoTexture.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldInsectsAlbedoTexture.name()
        )

        ## Insects Mask
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box, 
            material = material, 
            property = MSFS2024_MaterialProperties.windshieldInsectsMaskTexture.attributeName(),
            text = MSFS2024_MaterialProperties.windshieldInsectsMaskTexture.name()
        )
        return
