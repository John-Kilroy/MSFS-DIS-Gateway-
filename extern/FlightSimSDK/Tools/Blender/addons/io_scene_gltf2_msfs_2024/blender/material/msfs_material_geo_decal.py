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
from ..utils.msfs_material_nodes_utils import *
from .msfs_material import MSFS2024_Material



class MSFS2024_Geo_Decal(MSFS2024_Material):
    
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

        MSFS2024_MaterialProperties.uvOffsetU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvTilingU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvRotation,
        MSFS2024_MaterialProperties.clampUVX,
        MSFS2024_MaterialProperties.clampUVY,

        MSFS2024_MaterialProperties.collisionMaterial,
        MSFS2024_MaterialProperties.roadCollisionMaterial,

        MSFS2024_MaterialProperties.baseColorBlendFactor,
        MSFS2024_MaterialProperties.roughnessBlendFactor,
        MSFS2024_MaterialProperties.metallicBlendFactor,
        MSFS2024_MaterialProperties.occlusionBlendFactor,
        MSFS2024_MaterialProperties.normalBlendFactor,
        MSFS2024_MaterialProperties.emissiveBlendFactor,
        MSFS2024_MaterialProperties.normalOverrideFactor,
        MSFS2024_MaterialProperties.decalMode,
        MSFS2024_MaterialProperties.underClearCoat,

        MSFS2024_MaterialProperties.baseColorTexture,
        MSFS2024_MaterialProperties.omrTexture,
        MSFS2024_MaterialProperties.normalTexture,
        MSFS2024_MaterialProperties.emissiveTexture,
        MSFS2024_MaterialProperties.detailColorTexture,
        MSFS2024_MaterialProperties.detailOmrTexture,
        MSFS2024_MaterialProperties.detailNormalTexture,
        MSFS2024_MaterialProperties.blendMaskTexture,
        MSFS2024_MaterialProperties.occlusionUV2
    ]
    
    def __init__(self, material, buildTree = False):
        super().__init__(material, buildTree = buildTree)
        if buildTree:
            self.setDefaultProperties()
            self.forceUpdateNodes()

    def customShaderTree(self):
        super(MSFS2024_Geo_Decal, self).defaultShadersTree()
        self.decalTree()

    def decalTree(self):
        decalGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.decalGroup.value
        )

        if newGroup:
            #region Input/Output Nodes
            inputNode = addNode(
                nodes = decalGroup.nodes,
                name = MSFS2024_NodesSockets.groupInput.value,
                typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
                location = (65.0, -10.0),
                hidden = False
            )
            outputNode = addNode(
                nodes = decalGroup.nodes,
                name = MSFS2024_NodesSockets.groupOutput.value,
                typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
                location = (520.0, -10.0),
                hidden = False
            )
            #endregion

            #region ## Inputs
            # Alpha Base color output 
            BaseColorAInput = addGroupInput(
                group = decalGroup, 
                inputName = MSFS2024_ShaderNodes.baseColorA.value,
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            BaseColorAInput.default_value = 1.0
            #endregion 

            #region ## Outputs
            # Alpha output 
            AlphaOutput = addGroupOutput(
                group = decalGroup, 
                outputName = "Alpha",
                outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            AlphaOutput.default_value = 1.0
            AlphaOutput.min_value = 0.0
            AlphaOutput.max_value = 1.0
            #endregion 

            #region ## Nodes
            ## Vertex color
            vertexColorNode = addNode(
                nodes = decalGroup.nodes,
                name = MSFS2024_NodesSockets.vertexColor.value,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVertexColor.value,
                location = (70.0, 35.0)
            )

            ## Multiply Alpha node
            multiplyVertexColoralphaNode = addNode(
                nodes = decalGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (300.0, 40.0)
            )
            #endregion

            #region ## Links
            link(decalGroup.links, inputNode.outputs[0], multiplyVertexColoralphaNode.inputs[0])
            link(decalGroup.links, vertexColorNode.outputs[1], multiplyVertexColoralphaNode.inputs[1])
            link(decalGroup.links, multiplyVertexColoralphaNode.outputs[0], outputNode.inputs[0])
            #endregion

        decalGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.decalGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (1230.0, 300.0),
            width = 150.0,
            hidden = False
        )
        decalGroupNode.node_tree = decalGroup

        alphaGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.alphaGroup.value)
        principledBSDFNode = getNodesByClassName(self.nodes, MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value)[0]

        ## Links
        link(self.links, alphaGroupNode.outputs[0], decalGroupNode.inputs[0])
        link(self.links, decalGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.alpha.value])
    
    def setDefaultProperties(self):
        super().setDefaultProperties(self.attributes)
        setattr(self.material, MSFS2024_MaterialProperties.alphaMode.attributeName(), "BLEND")
        setattr(self.material, MSFS2024_MaterialProperties.decalMode.attributeName(), "default")

    def forceUpdateNodes(self):
        super().forceUpdateNodes()

    @staticmethod
    def drawPanel(layout, material):
        MSFS2024_Geo_Decal.drawParametersPanel(layout, material)
        MSFS2024_Geo_Decal.drawTexturesPanel(layout, material)

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

        #### Decal Blend Parameters ####
        box = layout.box()
        box.label(text="Decal Parameters")

        ## Base Color Blend Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.baseColorBlendFactor.attributeName()
        )

        ## Roughness Blend Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.roughnessBlendFactor.attributeName()
        )

        ## Metallic Blend Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.metallicBlendFactor.attributeName()
        )

        ## Occlusion Blend Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.occlusionBlendFactor.attributeName()
        )

        ## Normal Blend Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.normalBlendFactor.attributeName()
        )

        ## Emissive
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.emissiveBlendFactor.attributeName()
        )

        ## Normal Override
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.normalOverrideFactor.attributeName()
        )

        ## Render Under Clearcoat
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.underClearCoat.attributeName()
        )
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
        return
