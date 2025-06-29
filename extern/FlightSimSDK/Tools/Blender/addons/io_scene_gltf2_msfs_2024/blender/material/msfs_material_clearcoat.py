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

from ..utils.msfs_material_nodes_utils import *
from ..utils.msfs_material_utils import (MSFS2024_MaterialProperties,
                                         MSFS2024_MaterialUtilsUI)
from .msfs_material import MSFS2024_Material


class MSFS2024_Clearcoat(MSFS2024_Material):

    attributes = [
        MSFS2024_MaterialProperties.baseColor,
        MSFS2024_MaterialProperties.emissiveColor,
        MSFS2024_MaterialProperties.emissiveScale,
        MSFS2024_MaterialProperties.alphaMode,
        MSFS2024_MaterialProperties.drawOrderOffset,
        MSFS2024_MaterialProperties.noCastShadow,
        MSFS2024_MaterialProperties.doubleSided,
        MSFS2024_MaterialProperties.dayNightCycle,
        MSFS2024_MaterialProperties.disableMotionBlur,
        MSFS2024_MaterialProperties.flipBackFaceNormal,

        MSFS2024_MaterialProperties.metallicScale,
        MSFS2024_MaterialProperties.roughnessScale,
        MSFS2024_MaterialProperties.occlusionStrength,
        MSFS2024_MaterialProperties.normalScale,
        MSFS2024_MaterialProperties.alphaCutoff,
        MSFS2024_MaterialProperties.detailUVScale,
        MSFS2024_MaterialProperties.detailNormalScale,
        MSFS2024_MaterialProperties.detailBlendThreshold,
        MSFS2024_MaterialProperties.wearOverlayUVScale,
        MSFS2024_MaterialProperties.wearBlendSharpness,
        MSFS2024_MaterialProperties.wearAmount,

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

        MSFS2024_MaterialProperties.clearcoatRoughnessFactor,
        MSFS2024_MaterialProperties.clearcoatNormalFactor,
        MSFS2024_MaterialProperties.clearcoatColorRoughnessTiling,
        MSFS2024_MaterialProperties.clearcoatNormalTiling,
        MSFS2024_MaterialProperties.clearcoatBaseRoughness,

        MSFS2024_MaterialProperties.baseColorTexture,
        MSFS2024_MaterialProperties.omrTexture,
        MSFS2024_MaterialProperties.normalTexture,
        MSFS2024_MaterialProperties.emissiveTexture,
        MSFS2024_MaterialProperties.detailColorTexture,
        MSFS2024_MaterialProperties.detailOmrTexture,
        MSFS2024_MaterialProperties.detailNormalTexture,
        MSFS2024_MaterialProperties.blendMaskTexture,
        MSFS2024_MaterialProperties.occlusionUV2,
        MSFS2024_MaterialProperties.clearcoatColorRoughnessTexture,
        MSFS2024_MaterialProperties.clearcoatNormalTexture,
        MSFS2024_MaterialProperties.wearAlbedoMaskTexture,
        MSFS2024_MaterialProperties.wearOmrIntensityTexture
    ]

    def __init__(self, material, buildTree = False):
        super().__init__(material, buildTree = buildTree)
        if buildTree:
            self.setDefaultProperties()
            self.forceUpdateNodes()

    def customShaderTree(self):
        super(MSFS2024_Clearcoat, self).defaultShadersTree()
        self.clearcoatShaderTree()

    def setDefaultProperties(self):
        super().setDefaultProperties(self.attributes)

    def forceUpdateNodes(self):
        super().forceUpdateNodes()

    def clearcoatShaderTree(self):
        ## Clearcoat Frame
        clearcoatFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.clearcoatFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.6, 0.2, 0.1)
        )

        ## Clearcoat Texture
        # Out[0] : ClearcoatSeparate -> In[0]
        clearcoatTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.clearcoatTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (100.0, -800.0),
            frame = clearcoatFrame
        )

        ## Clearcoat separate
        # In[0] : ClearcoatTexture -> Out[0]
        # Out[0] : BSDF -> Clearcoat
        # Out[1] : BSDF -> ClearcoatRoughness
        clearcoatSeparateNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.clearcoatSeparate.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (300.0, -800.0),
            frame = clearcoatFrame
        )

        ## Clearcoat Normal
        # Out[0] : BSDF -> ClearcoatNormal
        addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.clearcoatNormalTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (300.0, -900.0),
            frame = clearcoatFrame
        )

        link(self.links, clearcoatTexNode.outputs[0], clearcoatSeparateNode.inputs[0])

    def setClearcoatTexture(self, tex): ## TODO - Update shader node tree for clearcoat -> Lucas ?
        clearcoatNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.clearcoatTex.value)
        clearcoatSeparateNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.clearcoatSeparate.value)
        principledBSDFNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.principledBSDF.value)

        if tex:
            clearcoatNode.image = tex
            clearcoatNode.image.colorspace_settings.name = "Non-Color"

            link(self.links, clearcoatSeparateNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.clearcoat.value])
            link(self.links, clearcoatSeparateNode.outputs[1], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.clearcoatRoughness.value])
        else:
            unLinkNodeInput(self.links, principledBSDFNode, MSFS2024_PrincipledBSDFInputs.clearcoat.value)
            unLinkNodeInput(self.links, principledBSDFNode, MSFS2024_PrincipledBSDFInputs.clearcoatRoughness.value)

    def setClearcoatNormalTexture(self, tex): ## TODO - Update shader node tree for clearcoat -> Lucas ?
        clearcoatNormalNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.clearcoatNormalTex.value)
        principledBSDFNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.principledBSDF.value)

        if tex:
            clearcoatNormalNode.image = tex

            link(self.links, clearcoatNormalNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.clearcoatNormal.value])
        else:
            unLinkNodeInput(self.links, principledBSDFNode, MSFS2024_PrincipledBSDFInputs.clearcoatNormal.value)

    @staticmethod
    def drawPanel(layout, material):
        MSFS2024_Clearcoat.drawParametersPanel(layout, material)
        MSFS2024_Clearcoat.drawTexturesPanel(layout, material)

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

        ## Alpha mode
        MSFS2024_MaterialUtilsUI.drawAlphaModeProp(
            layout = layout,
            material = material,
            text = MSFS2024_MaterialProperties.alphaMode.name()
        )

        #### Render Parameters ####
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

        ## Day Night Cycle
        MSFS2024_MaterialUtilsUI.drawDayNightCycleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.dayNightCycle.name()
        )

        ## Motion Blur
        MSFS2024_MaterialUtilsUI.drawMotionBlurProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.disableMotionBlur.name()
        )
        #### End Render Parameters ####

        #### General Parameters ####
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
            text = MSFS2024_MaterialProperties.occlusionStrength.name()
        )

        ## Normal Scale
        MSFS2024_MaterialUtilsUI.drawNormalScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.normalScale.name()
        )

        ## Alpha Cutoff
        if getattr(material, MSFS2024_MaterialProperties.alphaMode.attributeName()) == "MASK":
            MSFS2024_MaterialUtilsUI.drawAlphaCutoffProp(
                layout = box,
                material = material,
                text = MSFS2024_MaterialProperties.alphaCutoff.name()
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

        ## Wear Overlay UV Scale
        MSFS2024_MaterialUtilsUI.drawWearOverlayUVScaleProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.wearOverlayUVScale.name()
        )

        ## Wear Blend Sharpness
        MSFS2024_MaterialUtilsUI.drawWearBlendSharpnessProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.wearBlendSharpness.name()
        )

        ## Wear Amount
        MSFS2024_MaterialUtilsUI.drawWearAmountProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.wearAmount.name()
        )
        #### End General Parameters ####

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

        if material.msfs_receive_rain:
            ## Rain Drop Tiling
            MSFS2024_MaterialUtilsUI.drawRainDropTilingProp(
                layout = box,
                material = material,
                text = MSFS2024_MaterialProperties.rainDropTiling.name()
            )
        #### End Rain Options ####

        ### Clearcoat Parameters ####
        box = layout.box()
        box.label(text="Clearcoat Parameters")

        ## Clearcoat Roughness Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.clearcoatRoughnessFactor.attributeName()
        )

        ## Clearcoat Normal Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.clearcoatNormalFactor.attributeName()
        )

        ## Clearcoat Color/Roughness Tlining
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.clearcoatColorRoughnessTiling.attributeName()
        )

        ## Clearcoat Normal Tlining
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.clearcoatNormalTiling.attributeName()
        )

        if material.msfs_clearcoat_color_roughness_texture is None:
            ## Clearcoat Base Roughness
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.clearcoatBaseRoughness.attributeName()
            )
        ### End Clear Coat Parameters ####
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

        ## Occlusion (R), Roughness (G), Metallic (B) Texture
        MSFS2024_MaterialUtilsUI.drawOmrTextureProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.omrTexture.name()
        )

        ## Normal Texture
        MSFS2024_MaterialUtilsUI.drawNormalTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.normalTexture.name()
        )

        ## Emissive Texture
        MSFS2024_MaterialUtilsUI.drawEmissiveTextureProp(
            layout = box,
            material = material, 
            text = MSFS2024_MaterialProperties.emissiveTexture.name()
        )

        ## Detail Color Texture
        MSFS2024_MaterialUtilsUI.drawDetailColorTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.detailColorTexture.name()
        )

        ## Detail Occlusion (R), Roughness (G), Metallic (B) Texture
        MSFS2024_MaterialUtilsUI.drawDetailOmrTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.detailOmrTexture.name()
        )
        
        ## Detail Normal Texture
        MSFS2024_MaterialUtilsUI.drawDetailNormalTexture(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.detailNormalTexture.name()
        )

        ## Blend Mask Texture
        MSFS2024_MaterialUtilsUI.drawBlendMaskTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.blendMaskTexture.name()
        )

        ## Occlusion (UV2)
        MSFS2024_MaterialUtilsUI.drawOcclusionUV2TextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.occlusionUV2.name()
        )

        ## Clearcoat Color (RGB), Clearcoat Roughness (A)
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.clearcoatColorRoughnessTexture.attributeName(),
            text = MSFS2024_MaterialProperties.clearcoatColorRoughnessTexture.name()
        )

        ## Clearcoat Normal
        MSFS2024_MaterialUtilsUI.draw_texture_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.clearcoatNormalTexture.attributeName(),
            text = MSFS2024_MaterialProperties.clearcoatNormalTexture.name()
        )
        
        ## Wear Albedo (RGB) Mask (A)
        MSFS2024_MaterialUtilsUI.drawWearAlbedoMaskTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.wearAlbedoMaskTexture.name()
        )

        ## Wear OMR Intensity (A)
        MSFS2024_MaterialUtilsUI.drawWearOmrIntensityTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.wearOmrIntensityTexture.name()
        )