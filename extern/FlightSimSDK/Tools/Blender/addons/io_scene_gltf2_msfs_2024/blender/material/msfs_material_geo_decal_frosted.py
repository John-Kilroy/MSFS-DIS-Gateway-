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


class MSFS2024_Geo_Decal_Frosted(MSFS2024_Material):

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
        super(MSFS2024_Geo_Decal_Frosted, self).defaultShadersTree()
        self.decalFrostedTree()

    def decalFrostedTree(self):
        decalFrostedFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.decalFrostedFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.decalFrostedFrame.color()
        )

        freezeFactorNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_DecalNodes.decalFreezeFactor.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (1135.0, -40.0),
            hidden = True,
            frame = decalFrostedFrame
        )

        decalFrostedGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.decalFrostedGroup.value
        )

        if newGroup:
            #region Input/Output Nodes
            inputNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = MSFS2024_NodesSockets.groupInput.value,
                typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
                location = (-1080.0, -160.0),
                hidden = False
            )
            outputNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = MSFS2024_NodesSockets.groupOutput.value,
                typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
                location = (810.0, -165.0),
                hidden = False
            )
            #endregion

            #region ## Inputs
            # Base color RGB Input
            BaseColorRGBInput = addGroupInput(
                group = decalFrostedGroup, 
                inputName = MSFS2024_ShaderNodes.baseColorRGB.value,
                inputType = MSFS2024_GroupTypes.nodeSocketColor.value
            )
            BaseColorRGBInput.default_value = (1.0, 1.0, 1.0, 1.0)

            # Alpha Base color output 
            BaseColorAInput = addGroupInput(
                group = decalFrostedGroup, 
                inputName = MSFS2024_ShaderNodes.baseColorA.value,
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            BaseColorAInput.default_value = 1.0

            # Freeze factor
            FreezeFactorInput = addGroupInput(
                group = decalFrostedGroup, 
                inputName = MSFS2024_DecalNodes.decalFreezeFactor.value,
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            FreezeFactorInput.default_value = 0.0
            #endregion 

            #region ## Outputs
            # Base Color Output
            BaseColorOutput = addGroupOutput(
                group = decalFrostedGroup, 
                outputName = MSFS2024_ShaderNodes.baseColorRGB.value,
                outputType = MSFS2024_GroupTypes.nodeSocketColor.value
            )
            BaseColorOutput.default_value = (1.0, 1.0, 1.0, 1.0)

            # Alpha output 
            AlphaOutput = addGroupOutput(
                group = decalFrostedGroup, 
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
                nodes = decalFrostedGroup.nodes,
                name = MSFS2024_NodesSockets.vertexColor.value,
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVertexColor.value,
                location = (-800.0, -215.0)
            )

            # Multiply Alpha node
            multiplyVertexColoralphaNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Multiply (Alpha * Vertex Color)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (-620.0, -230.0),
                width = 200.0
            )

            # Invert Alpha
            oneMinusAlphaNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "1 - alpha",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (-370.0, -230.0)
            )
            oneMinusAlphaNode.inputs[0].default_value = 1.0

            # Classic Frost (cf)
            cfFrame = addNode(
                nodes = decalFrostedGroup.nodes,
                name = MSFS2024_FrameNodes.frostFrame.name(),
                typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
                color = MSFS2024_FrameNodes.frostFrame.color(),
                location = (2800.0, -1340.0)
            )

            # Multiply (x * 0.675)
            multiply0675Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Multiply (x * 0.675)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (-510.0, -50.0),
                frame = cfFrame
            )
            multiply0675Node.inputs[1].default_value = 0.675

            # Subtract (x - 0.02)
            subtract002Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Substract (x - 0.02)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (-310.0, -50.0),
                frame = cfFrame
            )
            subtract002Node.inputs[1].default_value = 0.02

            # Multiply (x * 0.951)
            multiply0951Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Multiply (x * 0.951)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (-510.0, -90.0),
                frame = cfFrame
            )
            multiply0951Node.inputs[1].default_value = 0.951

            # Subtract (x - 0.01)
            subtract001Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Substract (x - 0.01)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (-310.0, -90.0),
                frame = cfFrame
            )
            subtract001Node.inputs[1].default_value = 0.01

            # Linearstep(freezeFactor * 0.675 - 0.02, freezeFactor * 0.951 - 0.01, 1.0 - alpha)
            cfFirstPassNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Frost First Pass",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMapRange.value,
                location = (-100.0, -70.0),
                frame = cfFrame
            )
            cfFirstPassNode.interpolation_type = "LINEAR"

            # Subtract (1 - linearStep(freezeFactor * 0.675 - 0.02, freezeFactor * 0.951 - 0.01, 1.0 - alpha))
            invertcfFirstPassNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Substract (1 - classicFrostFirstPass)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (70.0, -72.0),
                width = 225.0,
                frame = cfFrame
            )
            invertcfFirstPassNode.inputs[0].default_value = 1.0

            # Subtract (classicFrostFirstPass - frostTint)
            cfFirstPassMinusfrostTintNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Substract (classicFrostFirstPass - frostTint)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (315.0, -72.0),
                width = 250.0,
                frame = cfFrame
            )
            cfFirstPassMinusfrostTintNode.use_clamp = True

            # Multiply saturate((classicFrostFirsPass - frostedTint) * 0.4)
            cfSecondPassNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Multiply (x * 0.4)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (590.0, -75.0),
                frame = cfFrame
            )
            cfSecondPassNode.use_clamp = True
            cfSecondPassNode.inputs[1].default_value = 0.4

            # Frost Tint
            frostTintFrame = addNode(
                nodes = decalFrostedGroup.nodes,
                name = MSFS2024_FrameNodes.frostTintFrame.name(),
                typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
                color = MSFS2024_FrameNodes.frostTintFrame.color()
            )

            # Multiply (x * 0.455)
            multiply0455Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Multiply (x * 0.455)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (-615.0, -300.0),
                frame = frostTintFrame
            )
            multiply0455Node.inputs[1].default_value = 0.455

            # Multiply (x * 0.935)
            multiply0935Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Multiply (x * 0.935)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (-615.0, -340.0),
                frame = frostTintFrame
            )
            multiply0935Node.inputs[1].default_value = 0.935

            # Subtract (x - 0.2)
            subtract02Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Subtract (x -0.2)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (-396.0, -300.0),
                frame = frostTintFrame
            )
            subtract02Node.inputs[1].default_value = 0.2

            # Subtract (x - 0.15)
            subtract015Node = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Subtract (x -0.15)",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (-396.0, -340.0),
                frame = frostTintFrame
            )
            subtract015Node.inputs[1].default_value = 0.15

            # Linearstep(freezeFactor * 0.455 - 0.2, freezeFactor * 0.935 - 0.15, 1.0 - alpha)
            frostTintFirstPassNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Frost Tint First Pass",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMapRange.value,
                location = (-165.0, -320.0),
                frame = frostTintFrame
            )
            frostTintFirstPassNode.interpolation_type = "LINEAR"

            # Frost Tint
            frostTintNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Frost Tint Result",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
                operation = MSFS2024_NodeMathOpe.subtract.value,
                location = (-4.0, -320.0),
                frame = frostTintFrame
            )
            frostTintNode.inputs[0].default_value = 1.0

            # Linearstep lerp(float3(1,1,1), float3(0.7, 0.85, 0.9), frostedTint)
            lerpFrostTintNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Lerp Frost Tint",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMapRange.value,
                location = (365.0, -140.0)
            )
            lerpFrostTintNode.interpolation_type = "LINEAR"
            lerpFrostTintNode.data_type = "FLOAT_VECTOR"
            lerpFrostTintNode.inputs[7].default_value = (1.0, 1.0, 1.0)
            lerpFrostTintNode.inputs[8].default_value = (0.7, 0.85, 0.9)

            # Base color RGB * lerpFrostTint
            multiplyRGBFrostTintNode = addNode(
                nodes = decalFrostedGroup.nodes,
                name = "Base Color RGB * Frost Tint",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
                operation = MSFS2024_NodeMathOpe.multiply.value,
                location = (540.0, -190.0),
                width = 200.0
            )
            #endregion

            #region ## Links
            # Alpha
            link(decalFrostedGroup.links, vertexColorNode.outputs[1], multiplyVertexColoralphaNode.inputs[0])
            link(decalFrostedGroup.links, inputNode.outputs[1], multiplyVertexColoralphaNode.inputs[1])
            link(decalFrostedGroup.links, multiplyVertexColoralphaNode.outputs[0], oneMinusAlphaNode.inputs[1])

            # Frost Tint
            link(decalFrostedGroup.links, inputNode.outputs[2], multiply0455Node.inputs[0])
            link(decalFrostedGroup.links, inputNode.outputs[2], multiply0935Node.inputs[0])
            
            link(decalFrostedGroup.links, multiply0455Node.outputs[0], subtract02Node.inputs[0])
            link(decalFrostedGroup.links, multiply0935Node.outputs[0], subtract015Node.inputs[0])

            link(decalFrostedGroup.links, oneMinusAlphaNode.outputs[0], frostTintFirstPassNode.inputs[0])
            link(decalFrostedGroup.links, subtract02Node.outputs[0], frostTintFirstPassNode.inputs[1])
            link(decalFrostedGroup.links, subtract015Node.outputs[0], frostTintFirstPassNode.inputs[2])
            link(decalFrostedGroup.links, frostTintFirstPassNode.outputs[0], frostTintNode.inputs[1])

            # Classic Frost
            link(decalFrostedGroup.links, inputNode.outputs[2], multiply0675Node.inputs[0])
            link(decalFrostedGroup.links, inputNode.outputs[2], multiply0951Node.inputs[0])

            link(decalFrostedGroup.links, multiply0675Node.outputs[0], subtract002Node.inputs[0])
            link(decalFrostedGroup.links, multiply0951Node.outputs[0], subtract001Node.inputs[0])

            link(decalFrostedGroup.links, oneMinusAlphaNode.outputs[0], cfFirstPassNode.inputs[0])
            link(decalFrostedGroup.links, subtract002Node.outputs[0], cfFirstPassNode.inputs[1])
            link(decalFrostedGroup.links, subtract001Node.outputs[0], cfFirstPassNode.inputs[2])

            link(decalFrostedGroup.links, cfFirstPassNode.outputs[0], invertcfFirstPassNode.inputs[1])
            
            link(decalFrostedGroup.links, invertcfFirstPassNode.outputs[0], cfFirstPassMinusfrostTintNode.inputs[0])
            link(decalFrostedGroup.links, frostTintNode.outputs[0], cfFirstPassMinusfrostTintNode.inputs[1])

            link(decalFrostedGroup.links, cfFirstPassMinusfrostTintNode.outputs[0], cfSecondPassNode.inputs[0])

            # Base Color RGB
            link(decalFrostedGroup.links, frostTintNode.outputs[0], lerpFrostTintNode.inputs[6])
            link(decalFrostedGroup.links, lerpFrostTintNode.outputs[1], multiplyRGBFrostTintNode.inputs[0])
            link(decalFrostedGroup.links, inputNode.outputs[0], multiplyRGBFrostTintNode.inputs[1])


            link(decalFrostedGroup.links, multiplyRGBFrostTintNode.outputs[0], outputNode.inputs[0])
            link(decalFrostedGroup.links, cfSecondPassNode.outputs[0], outputNode.inputs[1])
            #endregion

        decalFrostedGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.decalFrostedGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (1345.0, 120.0),
            width = 200.0,
            hidden = False,
            frame = decalFrostedFrame
        )
        decalFrostedGroupNode.node_tree = decalFrostedGroup

        alphaGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.alphaGroup.value)
        baseColorRGBGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.baseColorGroup.value)
        principledBSDFNode = getNodesByClassName(self.nodes, MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value)[0]

        ## Links
        link(self.links, baseColorRGBGroupNode.outputs[0], decalFrostedGroupNode.inputs[0])
        link(self.links, decalFrostedGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.baseColor.value])
        link(self.links, alphaGroupNode.outputs[0], decalFrostedGroupNode.inputs[1])
        link(self.links, decalFrostedGroupNode.outputs[1], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.alpha.value])
        link(self.links, freezeFactorNode.outputs[0], decalFrostedGroupNode.inputs[2])

    def setDefaultProperties(self):
        super().setDefaultProperties(self.attributes)
        setattr(self.material, MSFS2024_MaterialProperties.alphaMode.attributeName(), "BLEND")
        setattr(self.material, MSFS2024_MaterialProperties.decalMode.attributeName(), "frosted")

    def setFreezeFactor(self, value):
        freezeFactorNode = getNodeByName(self.nodes, MSFS2024_DecalNodes.decalFreezeFactor.value)
        if (freezeFactorNode):
            freezeFactorNode.outputs[0].default_value = value

    def forceUpdateNodes(self):
        super().forceUpdateNodes()
        self.setFreezeFactor(getattr(self.material, MSFS2024_MaterialProperties.decalFreezeFactor.attributeName()))

    @staticmethod
    def drawPanel(layout, material):
        MSFS2024_Geo_Decal_Frosted.drawParametersPanel(layout, material)
        MSFS2024_Geo_Decal_Frosted.drawTexturesPanel(layout, material)

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
            text = MSFS2024_MaterialProperties.occlusionStrength.name()
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

        #### Decal Blend Parameters ####
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

        ## Render Under Clearcoat
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.underClearCoat.attributeName()
        )
        #### End Decal Blend Parameters ####

        #### Decal Debug ####
        box = layout.box()
        box.label(text="Debug")

        ## Freeze Factor
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = box,
            material = material,
            property = MSFS2024_MaterialProperties.decalFreezeFactor.attributeName()
        )
        #### End Decal Debug ####
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

        ## Melt Pattern (R), Roughness (G), Metallic (B) Texture
        MSFS2024_MaterialUtilsUI.drawDetailOmrTextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.decalMeltRoughnessMetallicTexture.name()
        )
        
        ## Detail Normal Texture
        MSFS2024_MaterialUtilsUI.drawDetailNormalTexture(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.detailNormalTexture.name()
        )

        ## Occlusion (UV2)
        MSFS2024_MaterialUtilsUI.drawOcclusionUV2TextureProp(
            layout = box, 
            material = material, 
            text = MSFS2024_MaterialProperties.occlusionUV2.name()
        )
        return

