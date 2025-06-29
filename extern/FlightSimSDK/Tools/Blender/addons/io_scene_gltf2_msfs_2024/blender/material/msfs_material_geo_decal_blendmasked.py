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


class MSFS2024_Geo_Decal_BlendMasked(MSFS2024_Material):
    
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
        MSFS2024_MaterialProperties.decalblendSharpness,
        MSFS2024_MaterialProperties.decalMode,
        MSFS2024_MaterialProperties.underClearCoat,

        MSFS2024_MaterialProperties.baseColorTexture,
        MSFS2024_MaterialProperties.omrTexture,
        MSFS2024_MaterialProperties.normalTexture,
        MSFS2024_MaterialProperties.emissiveTexture,
        MSFS2024_MaterialProperties.detailColorTexture,
        MSFS2024_MaterialProperties.detailOmrTexture,
        MSFS2024_MaterialProperties.detailNormalTexture,
        MSFS2024_MaterialProperties.decalBlendMaskTexture,
        MSFS2024_MaterialProperties.occlusionUV2,

        MSFS2024_MaterialProperties.decalblendMaskedThreshold
    ]
    
    def __init__(self, material, buildTree = False):
        super().__init__(material, buildTree = buildTree)
        if buildTree:
            self.setDefaultProperties()
            self.forceUpdateNodes()

    def customShaderTree(self):
        super(MSFS2024_Geo_Decal_BlendMasked, self).defaultShadersTree()
        self.decalBlendMaskedTree()

    def decalBlendMaskedTree(self):
        ## Decal Frame
        decalFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.decalBlendMaskedFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.5, 0.1, 0.0)
        )

        # Blend Mask
        decalBlendMaskTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_DecalNodes.decalBlendMaskTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (1133.0, 214.0),
            width = 300.0,
            frame = decalFrame
        )
        decalBlendMaskTexNode.interpolation = "Linear"

        # Blend Mask Threshold
        blendMaskThresholdNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_DecalNodes.decalBlendMaskThreshold.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (1133.0, 160.0),
            width = 300.0,
            frame = decalFrame
        )
        blendMaskThresholdNode.outputs[0].default_value = 1.0

        # Blend Mask Threshold
        blendSharpnessNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_DecalNodes.decalBlendMaskSharpness.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (1133.0, 114.0),
            width = 300.0,
            frame = decalFrame
        )
        blendSharpnessNode.outputs[0].default_value = 1.0
        
        decalBlendMaskedGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.decalBlendMaskedGroup.value
        )

        if newGroup:
            ## Group Nodes
            inputNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                name = MSFS2024_NodesSockets.groupInput.value,
                typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
                location = (-480.0, 40.0),
                hidden = False
            )
            outputNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                name = MSFS2024_NodesSockets.groupOutput.value,
                typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
                location = (1000.0, 30.0),
                hidden = False
            )

            #region ## Inputs
            BaseColorAInput = addGroupInput(
                group = decalBlendMaskedGroup, 
                inputName = MSFS2024_ShaderNodes.baseColorA.value,
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            BaseColorAInput.default_value = 1.0

            BlendMaskedInput = addGroupInput(
                group = decalBlendMaskedGroup, 
                inputName = MSFS2024_ShaderNodes.blendMaskTex.value,
                inputType = MSFS2024_GroupTypes.nodeSocketColor.value
            )
            BlendMaskedInput.default_value = (1.0, 1.0, 1.0, 1.0)

            BlendMaskThresholdInput = addGroupInput(
                group = decalBlendMaskedGroup, 
                inputName = MSFS2024_DecalNodes.decalBlendMaskThreshold.value,
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            BlendMaskThresholdInput.default_value = 1.0

            BlendMaskSharpnessInput = addGroupInput(
                group = decalBlendMaskedGroup, 
                inputName = MSFS2024_DecalNodes.decalBlendMaskSharpness.value,
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            BlendMaskSharpnessInput.default_value = 1.0
            #endregion

            #region ## Outputs
            # Alpha output 
            AlphaOutput = addGroupOutput(
                group = decalBlendMaskedGroup, 
                outputName = "Alpha",
                outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            AlphaOutput.default_value = 1.0
            AlphaOutput.min_value = 0.0
            AlphaOutput.max_value = 1.0
            #endregion 

            #region ## Nodes
            # Vertex color
            vertexColorNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                name = MSFS2024_NodesSockets.vertexColor.value,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVertexColor.value,
                location = (20.0, -7.0)
            )

            oneMinusThresholdNode = addNode(
                name = "Substract (1 - x)",
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (28.0, -40.0)
            )

            multiplyVertexColorAlphaNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (230.0, -25.0)
            )

            oneMinusSharpnessNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (24.0, -161.0)
            )
            oneMinusSharpnessNode.inputs[0].default_value = 1.0

            separateBlendMaskTexNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
                location = (20.0, -120.0)
            )

            blendMaskMinusSharpnessNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (340.0, -100.0)
            )
            blendMaskMinusSharpnessNode.use_clamp = True

            blendMaskPlusSharpnessNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.add.value,
                location = (340.0, -163.0)
            )
            blendMaskPlusSharpnessNode.use_clamp = True

            linearStepMapRangeNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMapRange.value,
                operation = MSFS2024_MapRangeType.linear.value,
                location = (560.0, -80.0)
            )

            multiplyAlphaLinearStepNode = addNode(
                nodes = decalBlendMaskedGroup.nodes,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (782.0, 5.0)
            )
            #endregion

            #region ## Links
            link(decalBlendMaskedGroup.links, inputNode.outputs[0], multiplyAlphaLinearStepNode.inputs[0])

            link(decalBlendMaskedGroup.links, inputNode.outputs[1], separateBlendMaskTexNode.inputs[0])
            link(decalBlendMaskedGroup.links, separateBlendMaskTexNode.outputs[0], blendMaskMinusSharpnessNode.inputs[0])
            link(decalBlendMaskedGroup.links, separateBlendMaskTexNode.outputs[0], blendMaskPlusSharpnessNode.inputs[0])

            link(decalBlendMaskedGroup.links, vertexColorNode.outputs[1], multiplyVertexColorAlphaNode.inputs[0])
            link(decalBlendMaskedGroup.links, inputNode.outputs[2], oneMinusThresholdNode.inputs[1])
            link(decalBlendMaskedGroup.links, oneMinusThresholdNode.outputs[0], multiplyVertexColorAlphaNode.inputs[1])
            
            link(decalBlendMaskedGroup.links, inputNode.outputs[3], oneMinusSharpnessNode.inputs[1])

            link(decalBlendMaskedGroup.links, oneMinusSharpnessNode.outputs[0], blendMaskPlusSharpnessNode.inputs[1])
            link(decalBlendMaskedGroup.links, oneMinusSharpnessNode.outputs[0], blendMaskMinusSharpnessNode.inputs[1])

            link(decalBlendMaskedGroup.links, multiplyVertexColorAlphaNode.outputs[0], linearStepMapRangeNode.inputs[0])
            link(decalBlendMaskedGroup.links, blendMaskMinusSharpnessNode.outputs[0], linearStepMapRangeNode.inputs[1])
            link(decalBlendMaskedGroup.links, blendMaskPlusSharpnessNode.outputs[0], linearStepMapRangeNode.inputs[2])

            link(decalBlendMaskedGroup.links, linearStepMapRangeNode.outputs[0], multiplyAlphaLinearStepNode.inputs[1])
            link(decalBlendMaskedGroup.links, multiplyAlphaLinearStepNode.outputs[0], outputNode.inputs[0])
            #endregion

        decalBlendMaskedGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.decalBlendMaskedGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (1513.0, 329.0),
            width = 150.0,
            hidden = False,
            frame = decalFrame
        )
        decalBlendMaskedGroupNode.node_tree = decalBlendMaskedGroup

        alphaGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.alphaGroup.value)
        principledBSDFNode = getNodesByClassName(self.nodes, MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value)[0]

        ## Links
        link(self.links, alphaGroupNode.outputs[0], decalBlendMaskedGroupNode.inputs[0])
        link(self.links, decalBlendMaskTexNode.outputs[0], decalBlendMaskedGroupNode.inputs[1])
        link(self.links, blendMaskThresholdNode.outputs[0], decalBlendMaskedGroupNode.inputs[2])
        link(self.links, blendSharpnessNode.outputs[0], decalBlendMaskedGroupNode.inputs[3])
        link(self.links, decalBlendMaskedGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.alpha.value])

    def setDefaultProperties(self):
        super().setDefaultProperties(self.attributes)
        setattr(self.material, MSFS2024_MaterialProperties.alphaMode.attributeName(), "BLEND")
        setattr(self.material, MSFS2024_MaterialProperties.decalMode.attributeName(), "blendMasked")

    def setDecalBlendMaskTex(self, texture):
        decalBlendMaskTex = getNodeByName(self.nodes, MSFS2024_DecalNodes.decalBlendMaskTex.value)
        
        if not decalBlendMaskTex:
            return
            
        decalBlendMaskTex.image = texture
        # Update shader tree
        if texture is None:
            unLinkNodeOutput(self.links, decalBlendMaskTex, 0)
            return

        decalBlendMaskGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.decalBlendMaskedGroup.value)
        if decalBlendMaskGroupNode:
            link(self.links, decalBlendMaskTex.outputs[0], decalBlendMaskGroupNode.inputs[0])

        uvGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.uvGroup.value)
        if uvGroupNode:
            link(self.links, uvGroupNode.outputs[0], decalBlendMaskTex.inputs[0])

    def setBlendMaskThreshold(self, value):
        blendThresholdValueNode = getNodeByName(self.nodes, MSFS2024_DecalNodes.decalBlendMaskThreshold.value)
        if blendThresholdValueNode:
            blendThresholdValueNode.outputs[0].default_value = value

    def setBlendMaskSharpness(self, value):
        blendMaskSharpnessValueNode = getNodeByName(self.nodes, MSFS2024_DecalNodes.decalBlendMaskSharpness.value)
        if blendMaskSharpnessValueNode:
            blendMaskSharpnessValueNode.outputs[0].default_value = value + 0.000001 # We need to add a small value to avoid division by zero

    def forceUpdateNodes(self):
        super().forceUpdateNodes()
        self.setDecalBlendMaskTex(getattr(self.material, MSFS2024_MaterialProperties.decalBlendMaskTexture.attributeName()))
        self.setBlendMaskThreshold(getattr(self.material, MSFS2024_MaterialProperties.decalblendMaskedThreshold.attributeName()))
        self.setBlendMaskSharpness(getattr(self.material, MSFS2024_MaterialProperties.decalblendSharpness.attributeName()))

    @staticmethod
    def drawPanel(layout, material):
        MSFS2024_Geo_Decal_BlendMasked.drawParametersPanel(layout, material)
        MSFS2024_Geo_Decal_BlendMasked.drawTexturesPanel(layout, material)

    @staticmethod
    def drawParametersPanel(layout, material):
        #region Colors
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
        #endregion

        ## Alpha mode
        MSFS2024_MaterialUtilsUI.drawAlphaModeProp(
            layout = layout,
            material = material,
            text = MSFS2024_MaterialProperties.alphaMode.name()
        )

        #region #### Render parameters ####
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
        #endregion

        #region #### General parameters ####
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
        #endregion

        #region #### UV options ####
        MSFS2024_MaterialUtilsUI.drawUVPanel(
            layout = layout,
            material = material
        )
        #endregion #### End UV options ####

        #region #### Gameplay Parameters ####
        MSFS2024_MaterialUtilsUI.drawGameplayPanel(
            layout = layout,
            material = material
        )
       #endregion  #### End Gameplay Parameters ####

        #region #### Decal Blend Parameters ####
        box = layout.box()
        box.label(text="Decal Blend Factors")

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

        ## Blend Sharpness
        if getattr(material, MSFS2024_MaterialProperties.decalBlendMaskTexture.attributeName()) is not None:
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.decalblendSharpness.attributeName()
            )

        ## Render Under Clearcoat
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.underClearCoat.attributeName()
        )
        #### End Decal Blend Parameters ####
        #endregion
        
        #region #### Debug Parameters ####
        if getattr(material, MSFS2024_MaterialProperties.decalBlendMaskTexture.attributeName()) is not None:
            box = layout.box()
            box.label(text="Decal Blend Mask Debug")

            ## Blend Mask Threshold
            MSFS2024_MaterialUtilsUI.draw_prop(
                layout = box,
                material = material,
                property = MSFS2024_MaterialProperties.decalblendMaskedThreshold.attributeName()
            )
        #### End Debug Parameters ####
        #endregion
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

        ## Decal Blend Mask Texture
        MSFS2024_MaterialUtilsUI.drawDecalBlendMaskTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.decalBlendMaskTexture.name()
        )

        ## Occlusion (UV2)
        MSFS2024_MaterialUtilsUI.drawOcclusionUV2TextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.occlusionUV2.name()
        )
