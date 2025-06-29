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
from ..utils.msfs_material_nodes_library import *
from ..utils.msfs_material_utils import MSFS2024_MaterialProperties


class MSFS2024_Material:
    bl_idname = "MSFS2024_ShaderNodeTree"
    bl_label = "MSFS2024 Shader Node Tree"

    def __init__(self, material, buildTree = False, revertToPBR = False):
        self.material = material
        self.node_tree = self.material.node_tree
        if self.node_tree is not None:
            self.nodes = self.node_tree.nodes
            self.links = self.node_tree.links

            if buildTree:
                self._buildTree()

            if revertToPBR:
                self.setDefaultProperties()
                self.revertToPBRShaderTree()

    def _buildTree(self):
        self._cleanNodeTree()
        self._createTree()

    def _cleanNodeTree(self):
        nodes = self.node_tree.nodes
        for idx, node in enumerate(nodes):
            # print("Deleting: %s | %s" % (node.name, node.type))
            nodes.remove(node)

    def _createTree(self):
        nodeOutputMaterial = addNode(
            nodes = self.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeOutputMaterial.value,
            location = (2000.0, 640.0),
            hidden = False
        )

        principledBSDF = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.principledBSDF.value,
            typeNode = MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value,
            location = (1800.0, 610.0),
            hidden = False
        )

        gltfSettingsGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_ShaderNodes.glTFSettings.value
        )
        if newGroup:
            gltfSettingsInput = addGroupInput(
                group = gltfSettingsGroup, 
                inputName = "Occlusion",
                inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
            )
            gltfSettingsInput.default_value = 1.000

        nodeglTFSettings = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.glTFSettings.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (1800.0, -90.0),
            hidden = False
        )
        nodeglTFSettings.node_tree = gltfSettingsGroup

        link(self.links, principledBSDF.outputs[0], nodeOutputMaterial.inputs[0])

        self.customShaderTree()

    def _createPBRTree(self):
        nodeOutputMaterial = addNode(
            nodes = self.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeOutputMaterial.value,
            location = (1200.0, 50.0),
            hidden = False
        )
        principledBSDF = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.principledBSDF.value,
            typeNode = MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value,
            location = (1000.0, 25.0),
            hidden = False
        )
        link(self.links, principledBSDF.outputs[0], nodeOutputMaterial.inputs[0])
    
    ####################################################
    def _updateBlendMaskLinks(self):
        blendMaskTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.blendMaskTex.value)
        blendMaskGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.blendMaskGroup.value)
        ## Set Group Inputs/Outputs Links to default
        unLinkNodeInput(self.links, blendMaskGroupNode, 0)
        unLinkNodeInput(self.links, blendMaskGroupNode, 1)
        setInputValue(blendMaskGroupNode.inputs[2], 0)#disable blend mask input
        
        if blendMaskTexNode.image:
            
            link(self.links, blendMaskTexNode.outputs[0], blendMaskGroupNode.inputs[1])
            link(self.links, blendMaskTexNode.outputs[1], blendMaskGroupNode.inputs[0])
            setInputValue(blendMaskGroupNode.inputs[2], 1)#enable blend mask input

    def _updateBlendMaskMode(self):
        detailColorTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailColorTex.value)
        detailOmrTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailCompTex.value)
        detailNormalTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailNormalTex.value)

        blendMaskGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.blendMaskGroup.value)
        baseColorGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.baseColorGroup.value)
        omrGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.omrGroup.value)
        normalGroup = getNodeByName(self.nodes, MSFS2024_GroupNodes.normalGroup.value)

        if detailColorTexNode.image and detailOmrTexNode.image and detailNormalTexNode.image:# blend mode 
            setInputValue(blendMaskGroupNode.inputs[4], 1)
            setInputValue(baseColorGroupNode.inputs[6], 1)
            setInputValue(omrGroupNode.inputs[6], 1)
            setInputValue(normalGroup.inputs[6], 1)
        else:# detail mode
            setInputValue(blendMaskGroupNode.inputs[4], 0)
            setInputValue(baseColorGroupNode.inputs[6], 0)
            setInputValue(omrGroupNode.inputs[6], 0)
            setInputValue(normalGroup.inputs[6], 0)

    def _updateColorLinks(self):
        baseColorTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.baseColorTex.value)
        detailColorTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailColorTex.value)
        baseColorGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.baseColorGroup.value)
        alphaGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.alphaGroup.value)

        ## TODO - Maybe get the BlendColorMapNode From the group and change the blend_type
        
        ## Set Group Inputs/Outputs Links to default
        # Unlink Base Color Group textures and alpha detail by default 
        unLinkNodeInput(self.links, baseColorGroupNode, 1)
        unLinkNodeInput(self.links, baseColorGroupNode, 2)
        unLinkNodeInput(self.links, baseColorGroupNode, 3)
        setInputValue(baseColorGroupNode.inputs[4], 0)
        # Unlink Alpha Group textures and alpha detail by default 
        unLinkNodeInput(self.links, alphaGroupNode, 1)
        unLinkNodeInput(self.links, alphaGroupNode, 2)

        if baseColorTexNode.image :
            link(self.links, baseColorTexNode.outputs[0], baseColorGroupNode.inputs[1])
            link(self.links, baseColorTexNode.outputs[1], alphaGroupNode.inputs[1])

        if detailColorTexNode.image :
            link(self.links, detailColorTexNode.outputs[0], baseColorGroupNode.inputs[2])
            link(self.links, detailColorTexNode.outputs[1], baseColorGroupNode.inputs[3])
            link(self.links, detailColorTexNode.outputs[1], alphaGroupNode.inputs[2])
            setInputValue(baseColorGroupNode.inputs[4], 1)

    def _updateCompLinks(self):
        omrTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.compTex.value)
        detailOmrTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailCompTex.value)
        omrGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.omrGroup.value)

        ## Set Group Inputs/Outputs Links to default
        unLinkNodeInput(self.links, omrGroupNode, 2)
        unLinkNodeInput(self.links, omrGroupNode, 3)
        setInputValue(omrGroupNode.inputs[4], 0) #disable detail

        if omrTexNode.image :
            link(self.links, omrTexNode.outputs[0], omrGroupNode.inputs[2])
        if detailOmrTexNode.image:
            link(self.links, detailOmrTexNode.outputs[0], omrGroupNode.inputs[3])
            setInputValue(omrGroupNode.inputs[4], 0) #enable detail

    def _updateAOLinks(self):
        applyAOGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.applyAOGroup.value)
        occlusionUV2TexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.occlusionUV2Tex.value)
        
        unLinkNodeInput(self.links, applyAOGroupNode, 2)
      
        if occlusionUV2TexNode.image :
            link(self.links, occlusionUV2TexNode.outputs[0], applyAOGroupNode.inputs[2])

    def _updateEmissiveLinks(self):
        emissiveTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.emissiveTex.value)
        emissiveGroupNode = getNodeByName(self.nodes, MSFS2024_GroupNodes.emissiveGroup.value)
        
        ## Set Group Inputs/Outputs Links to default
        unLinkNodeInput(self.links, emissiveGroupNode, 2)

        if emissiveTexNode.image:
            link(self.links, emissiveTexNode.outputs[0], emissiveGroupNode.inputs[2])

    def _updateNormalLinks(self):
        normalScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.normalScale.value)
        normalTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.normalTex.value)
        detailNormalScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailNormalScale.value)
        detailNormalTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailNormalTex.value)
        normalGroup = getNodeByName(self.nodes, MSFS2024_GroupNodes.normalGroup.value)
        principledBSDFNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.principledBSDF.value)

        ## Set Group Inputs/Outputs Links to default
        unLinkNodeInput(self.links, normalGroup, 0)
        unLinkNodeInput(self.links, normalGroup, 1)
        unLinkNodeInput(self.links, normalGroup, 2)
        unLinkNodeInput(self.links, normalGroup, 3)

        unLinkNodeOutput(self.links, normalGroup, 0)
        setInputValue(normalGroup.inputs[4], 0)#disable detail normal
        

        if normalTexNode.image:
            link(self.links, normalScaleNode.outputs[0], normalGroup.inputs[0])
            link(self.links, normalTexNode.outputs[0], normalGroup.inputs[1])
            link(self.links, normalGroup.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.normal.value])

        if detailNormalTexNode.image:
            link(self.links, detailNormalScaleNode.outputs[0], normalGroup.inputs[2])
            link(self.links, detailNormalTexNode.outputs[0], normalGroup.inputs[3])
            setInputValue(normalGroup.inputs[4], 1)#enable detail normal
            
    ####################################################
    def _makeOpaque(self):
        self.material.blend_method = "OPAQUE"

    def _makeMasked(self):
        self.material.blend_method = "CLIP"

    def _makeAlphaBlend(self):
        self.material.blend_method = "BLEND"

    def _makeDither(self):
        # Since Eevee doesn't provide a dither mode, we'll just use alpha-blend instead.
        self.material.blend_method = "BLEND"

    ####################################################
    def revertToPBRShaderTree(self):
        self._cleanNodeTree()
        self._createPBRTree()

    def customShaderTree(self):
        raise NotImplementedError()

    def defaultShadersTree(self):
        principledBSDFNode = getNodesByClassName(self.nodes, MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value)[0]
        glTFSettingsNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.glTFSettings.value)

        #region ## Inputs ##

        ## Mask Inputs frame
        maskInputsFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.maskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.maskFrame.color()
        )
        blendMaskTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.blendMaskTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, 1050),
            width = 300.0,
            frame = maskInputsFrame
        )

        blendMaskThresholdNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.detailblendMaskThreshold.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, 1000), 
            frame = maskInputsFrame
        )

        ## Base Color Inputs frame
        baseColorInputsFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.baseColorInputsFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.5, 0.1, 0.0)
        )

        ## Base Color RGB
        baseColorRGBNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.baseColorRGB.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeRGB.value,
            location = (-200.0, 800.0),
            width = 300.0,
            frame = baseColorInputsFrame
        )

        ## Base Color Texture
        baseColorTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.baseColorTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, 750),
            width = 300.0,
            frame = baseColorInputsFrame
        )
    
        ## Detail Color Texture
        detailColorTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.detailColorTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, 700),
            width = 300.0,
            frame = baseColorInputsFrame
        )

        ## Alpha Inputs Frame
        alphaInputsFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.alphaInputsFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.6, 0.6, 0.0)
        )

        ## Base color A
        baseColorANode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.baseColorA.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, 500.0),
            width = 300.0,
            frame = alphaInputsFrame
        )
        baseColorANode.outputs[0].default_value = 1.0
        
        ## UV Inputs Frame ##
        uvFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.uvFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.3, 0.3, 0.5)
        )

        ## UV Offset U
        uvOffsetUNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.uvOffsetU.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-1200.0, 500.0),
            frame = uvFrame
        )

        ## UV Offset V
        uvOffsetVNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.uvOffsetV.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-1200.0, 450.0),
            frame = uvFrame
        )

        ## UV Tiling U
        uvTilingUNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.uvTilingU.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-1200.0, 400.0),
            frame = uvFrame
        )

        ## UV Tiling V
        uvTilingVNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.uvTilingV.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-1200.0, 350.0),
            frame = uvFrame
        )

        ## UV Rotation
        uvRotationNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.uvRotation.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-1200.0, 300.0),
            frame = uvFrame
        )

        ## Detail UV scale
        detailUVScaleNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.detailUVScale.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-1200.0, 250.0),
            frame = uvFrame
        )

        ## OMR Inputs Frame ##
        omrFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.omrFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.1, 0.4, 0.6)
        )

        ## Metallic scale
        metallicScaleNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.metallicScale.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, 350.0), 
            frame = omrFrame
        )

        ## Roughness scale
        roughnessScaleNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.roughnessScale.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, 300.0),
            frame = omrFrame
        )

        ## Comp Texture
        omrTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.compTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, 250),
            width = 300.0,
            frame = omrFrame
        )
        
        ## Detail Comp Texture
        detailOmrTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.detailCompTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, 200),
            width = 300.0,
            frame = omrFrame
        )
        
        ## Ambient Occlusion UV2
        aoUV2TexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.occlusionUV2Tex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, 150),
            width = 300.0,
            frame = omrFrame
        )

        ## Emissive Inputs Frame ##
        emissiveFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.emissiveFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.1, 0.5, 0.3)
        )

        ## Emissive Scale
        emissiveScaleNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.emissiveScale.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, 0.0),
            width = 300.0,
            frame = emissiveFrame
        )

        ## Emissive Color
        emissiveColorNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.emissiveColor.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeRGB.value,
            location = (-200.0, -50),
            width = 300.0,
            frame = emissiveFrame
        )

        ## Emissive Texture
        emissiveTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.emissiveTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, -100.0),
            width = 300.0,
            frame = emissiveFrame
        )
        
        ## Normal Inputs Frame
        normalFrame = addNode(
            nodes = self.nodes,
            name = MSFS2024_FrameNodes.normalFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.5, 0.25, 0.25)
        )

        ## Normal scale
        normalScaleNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.normalScale.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, -350.0),
            width = 300.0,
            frame = normalFrame
        )
        normalScaleNode.outputs[0].default_value = 1.0

        ## Normal Texture
        normalTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.normalTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, -400),
            width = 300.0,
            frame = normalFrame
        )

        ## Detail Normal Scale
        detailNormalScaleNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.detailNormalScale.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValue.value,
            location = (-200.0, -450.0),
            width = 300.0,
            frame = normalFrame
        )
        
        ## Detail Normal Texture
        detailNormalTexNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_ShaderNodes.detailNormalTex.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value,
            location = (-200, -500),
            width = 300.0,
            frame = normalFrame
        )

        #endregion

        #region ## Blend Mask Node Group ##
        blendMaskGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.blendMaskGroup.value
        )
        
        if newGroup:
            self.drawblendMaskShaderNodeGroup(group = blendMaskGroup)
        
        blendMaskGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.blendMaskGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (200.0, 1080.0),
            width = 250.0,
            hidden = False
        )

        blendMaskGroupNode.node_tree = blendMaskGroup
        ## Links
        link(self.links, blendMaskThresholdNode.outputs[0], blendMaskGroupNode.inputs[3])
        
        
        #endregion

        #region ## Base Color Node Group ##
        baseColorGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.baseColorGroup.value
        )
        
        if newGroup:
            self.drawBaseColorShaderNodeGroup(group = baseColorGroup)
        
        baseColorGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.baseColorGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (500.0, 900.0),
            width = 400.0,
            hidden = False
        )
        baseColorGroupNode.node_tree = baseColorGroup
        ## Links
        link(self.links, baseColorRGBNode.outputs[0], baseColorGroupNode.inputs[0])
        link(self.links, blendMaskGroupNode.outputs[0], baseColorGroupNode.inputs[5])
  
        #endregion

        #region ## Alpha Node Group ##
        alphaGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.alphaGroup.value
        )

        if newGroup:
            self.drawAlphaShaderNodeGroup(group = alphaGroup)

        alphaGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.alphaGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (500.0, 600.0),
            width = 400.0,
            hidden = False
        )
        alphaGroupNode.node_tree = alphaGroup

        ## Links
        link(self.links, alphaGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.alpha.value])
        link(self.links, baseColorANode.outputs[0], alphaGroupNode.inputs[0])
        #endregion
        
        #region ## UV Node Group ##
        uvGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.uvGroup.value
        )

        if newGroup:
            self.drawUVShaderNodeGroup(group = uvGroup)

        uvGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.uvGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (-1000.0, 500.0),
            width = 300.0,
            hidden = False
        )
        uvGroupNode.node_tree = uvGroup

        ## Links
        link(self.links, uvOffsetUNode.outputs[0], uvGroupNode.inputs[0])
        link(self.links, uvOffsetVNode.outputs[0], uvGroupNode.inputs[1])
        link(self.links, uvTilingUNode.outputs[0], uvGroupNode.inputs[2])
        link(self.links, uvTilingVNode.outputs[0], uvGroupNode.inputs[3])
        link(self.links, uvRotationNode.outputs[0], uvGroupNode.inputs[4])
        link(self.links, detailUVScaleNode.outputs[0], uvGroupNode.inputs[5])

        link(self.links, uvGroupNode.outputs[0], blendMaskTexNode.inputs[0])
        link(self.links, uvGroupNode.outputs[0], baseColorTexNode.inputs[0])
        link(self.links, uvGroupNode.outputs[0], omrTexNode.inputs[0])
        link(self.links, uvGroupNode.outputs[0], emissiveTexNode.inputs[0])
        link(self.links, uvGroupNode.outputs[0], normalTexNode.inputs[0])

        link(self.links, uvGroupNode.outputs[1], detailColorTexNode.inputs[0])
        link(self.links, uvGroupNode.outputs[1], detailOmrTexNode.inputs[0])
        link(self.links, uvGroupNode.outputs[1], detailNormalTexNode.inputs[0])

        link(self.links, uvGroupNode.outputs[2], aoUV2TexNode.inputs[0])
        #endregion

        #region ## OMR Group ##
        omrGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.omrGroup.value
        )

        if newGroup:
            self.drawOMRShaderNodeGroup(group = omrGroup)

        omrGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.omrGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (500.0, 400.0),
            width = 400.0,
            hidden = False
        )
        omrGroupNode.node_tree = omrGroup

        ## Links
        link(self.links, metallicScaleNode.outputs[0], omrGroupNode.inputs[0])
        link(self.links, roughnessScaleNode.outputs[0], omrGroupNode.inputs[1])

        link(self.links, omrGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.metallic.value])
        link(self.links, omrGroupNode.outputs[1], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.roughness.value])
        link(self.links, blendMaskGroupNode.outputs[0], omrGroupNode.inputs[5])
        
        if glTFSettingsNode:
            link(self.links, omrGroupNode.outputs[2], glTFSettingsNode.inputs[0])
        #endregion

        #region ## Emissive Group ##
        emissiveGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.emissiveGroup.value
        )

        if newGroup:
            self.drawEmissiveShaderNodeGroup(group = emissiveGroup) 

        emissiveGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.emissiveGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (500.0, 0.0),
            width = 400.0,
            hidden = False
        )
        emissiveGroupNode.node_tree = emissiveGroup

        ## Links
        link(self.links, emissiveScaleNode.outputs[0], emissiveGroupNode.inputs[0])
        link(self.links, emissiveColorNode.outputs[0], emissiveGroupNode.inputs[1])

        link(self.links, emissiveGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.emission.value])
        link(self.links, emissiveScaleNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.emissionStrength.value])
        #endregion

        #region ## Normal Group ##
        normalGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.normalGroup.value
        )

        if newGroup:
            self.drawNormalShaderNodeGroup(group = normalGroup)

        normalGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.normalGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (500.0, -250.0),
            width = 400.0,
            hidden = False
        )
        normalGroupNode.node_tree = normalGroup
        #endregion
        #region Links
        link(self.links, blendMaskGroupNode.outputs[0], normalGroupNode.inputs[5])
        
        #endregion

        #region ## Apply AO group ##
        applyAOGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.applyAOGroup.value
        )

        if newGroup:
            self.drawApplyAOGroup(group = applyAOGroup)

        applyAOGroupNode = addNode(
            nodes = self.nodes,
            name = MSFS2024_GroupNodes.applyAOGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = (1200.0, 630.0),
            width = 400.0,
            hidden = False
        )
        applyAOGroupNode.node_tree = applyAOGroup
        #endregion
        #region Links
        link(self.links, baseColorGroupNode.outputs[0], applyAOGroupNode.inputs[0])
        link(self.links, omrGroupNode.outputs[2], applyAOGroupNode.inputs[1])
        link(self.links, applyAOGroupNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.baseColor.value])
        #endregion
        return

    def setDefaultProperties(self, attributes = []):
        attributeNames = [x.attributeName() for x in attributes]
        materialProperties = list(MSFS2024_MaterialProperties)
        for i in range(1, len(materialProperties)): ## we start at 1 to avoid changing the material type
            materialProperty = materialProperties[i]
            if materialProperty.attributeName() not in attributeNames:
                if hasattr(self.material, materialProperty.attributeName()):
                    setattr(self.material, materialProperty.attributeName(), materialProperty.defaultValue())

    def forceUpdateNodes(self):
        self.setBlendMode(getattr(self.material, MSFS2024_MaterialProperties.alphaMode.attributeName()))

        self.setBaseColor(getattr(self.material, MSFS2024_MaterialProperties.baseColor.attributeName()))
        self.setBaseColorTex(getattr(self.material, MSFS2024_MaterialProperties.baseColorTexture.attributeName()))
        self.setCompTex(getattr(self.material, MSFS2024_MaterialProperties.omrTexture.attributeName()))
        self.setNormalTex(getattr(self.material, MSFS2024_MaterialProperties.normalTexture.attributeName()))

        self.setBlendMaskTex(getattr(self.material, MSFS2024_MaterialProperties.blendMaskTexture.attributeName()))
        self.setDetailColorTex(getattr(self.material, MSFS2024_MaterialProperties.detailColorTexture.attributeName()))
        self.setDetailCompTex(getattr(self.material, MSFS2024_MaterialProperties.detailOmrTexture.attributeName()))
        self.setDetailNormalTex(getattr(self.material, MSFS2024_MaterialProperties.detailNormalTexture.attributeName()))
        self.setOcclusionUV2Tex(getattr(self.material, MSFS2024_MaterialProperties.occlusionUV2.attributeName()))

        self.setEmissiveTexture(getattr(self.material, MSFS2024_MaterialProperties.emissiveTexture.attributeName()))
        self.setEmissiveColor(getattr(self.material, MSFS2024_MaterialProperties.emissiveColor.attributeName()))
        self.setEmissiveScale(getattr(self.material, MSFS2024_MaterialProperties.emissiveScale.attributeName()))
        self.setNormalScale(getattr(self.material, MSFS2024_MaterialProperties.normalScale.attributeName()))
        self.setMetallicScale(getattr(self.material, MSFS2024_MaterialProperties.metallicScale.attributeName()))
        self.setRoughnessScale(getattr(self.material, MSFS2024_MaterialProperties.roughnessScale.attributeName()))

        self.updateDoubleSided()
        self.updateAlphaCutoff()

        self.setUVOffsetU(getattr(self.material, MSFS2024_MaterialProperties.uvOffsetU.attributeName()))
        self.setUVOffsetV(getattr(self.material, MSFS2024_MaterialProperties.uvOffsetV.attributeName()))
        self.setUVTilingU(getattr(self.material, MSFS2024_MaterialProperties.uvTilingU.attributeName()))
        self.setUVTilingV(getattr(self.material, MSFS2024_MaterialProperties.uvTilingV.attributeName()))
        self.setUVRotation(getattr(self.material, MSFS2024_MaterialProperties.uvRotation.attributeName()))
        
        self.setDetailUVScale(getattr(self.material, MSFS2024_MaterialProperties.detailUVScale.attributeName()))
        self.setDetailNormalScale(getattr(self.material, MSFS2024_MaterialProperties.detailNormalScale.attributeName()))


    def updateMaterial(self):
        self._buildTree()

    #region ###Setter###
    def setBaseColor(self, color):
        baseColorNodeRGBNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.baseColorRGB.value)
        baseColorANode = getNodeByName(self.nodes,MSFS2024_ShaderNodes.baseColorA.value)

        if baseColorNodeRGBNode and baseColorANode:
            baseColorNodeRGBNode.outputs[0].default_value[0] = color[0]
            baseColorNodeRGBNode.outputs[0].default_value[1] = color[1]
            baseColorNodeRGBNode.outputs[0].default_value[2] = color[2]
            baseColorANode.outputs[0].default_value = color[3]

            self._updateColorLinks()
    
    def setBaseColorTex(self, texture):
        baseColorRGBTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.baseColorTex.value)
        if baseColorRGBTexNode:
            baseColorRGBTexNode.image = texture
            self._updateColorLinks()

    def setDetailColorTex(self, texture):
        detailColorTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailColorTex.value)
        if detailColorTexNode:
            detailColorTexNode.image = texture
            self._updateColorLinks()
            self._updateBlendMaskMode()

    def setCompTex(self, texture):
        compTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.compTex.value)
        if compTexNode:
            compTexNode.image = texture
            if texture is not None:
                compTexNode.image.colorspace_settings.name = "Non-Color"
            self._updateCompLinks()

    def setDetailCompTex(self, texture):
        detailCompTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailCompTex.value)
        if detailCompTexNode:
            detailCompTexNode.image = texture
            if texture is not None:
                detailCompTexNode.image.colorspace_settings.name = "Non-Color"
            self._updateCompLinks()
            self._updateBlendMaskMode()

    def setOcclusionUV2Tex(self, texture):
        oclusionUV2TexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.occlusionUV2Tex.value)
        if oclusionUV2TexNode:
            oclusionUV2TexNode.image = texture
            if texture is not None:
                oclusionUV2TexNode.image.colorspace_settings.name = "Non-Color"
            self._updateAOLinks()

    def setRoughnessScale(self, scale):
        roughnessScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.roughnessScale.value)
        if roughnessScaleNode:
            roughnessScaleNode.outputs[0].default_value = scale
            self._updateCompLinks()

    def setMetallicScale(self, scale):
        metallicScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.metallicScale.value)
        if metallicScaleNode:
            metallicScaleNode.outputs[0].default_value = scale
            self._updateCompLinks()

    def setEmissiveTexture(self, texture):
        emissiveTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.emissiveTex.value)
        if emissiveTexNode:
            emissiveTexNode.image = texture
            if texture is not None:
                emissiveTexNode.image.colorspace_settings.name = "Non-Color"
            self._updateEmissiveLinks()

    def setEmissiveScale(self, scale):
        emissiveScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.emissiveScale.value)
        if emissiveScaleNode:
            emissiveScaleNode.outputs[0].default_value = scale
            self._updateEmissiveLinks()

    def setEmissiveColor(self, color):
        emissiveColorNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.emissiveColor.value)
        if emissiveColorNode:
            emissiveValue = emissiveColorNode.outputs[0].default_value
            emissiveValue[0] = color[0]
            emissiveValue[1] = color[1]
            emissiveValue[2] = color[2]
            emissiveColorNode.outputs[0].default_value = emissiveValue
            self._updateEmissiveLinks()

    def setNormalScale(self, scale):
        normalScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.normalScale.value)
        if normalScaleNode:
            normalScaleNode.outputs[0].default_value = scale
            self._updateNormalLinks()

    def setNormalTex(self, texture):
        normalTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.normalTex.value)
        if normalTexNode:
            normalTexNode.image = texture
            if texture is not None:
                normalTexNode.image.colorspace_settings.name = "Non-Color"
            self._updateNormalLinks()

    def setDetailNormalScale(self, scale):
        detailNormalScaleNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailNormalScale.value)
        if detailNormalScaleNode:
            detailNormalScaleNode.outputs[0].default_value = scale
            self._updateNormalLinks()

    def setDetailNormalTex(self, texture):
        detailNormalTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailNormalTex.value)
        if detailNormalTexNode:
            detailNormalTexNode.image = texture
            if texture is not None:
                detailNormalTexNode.image.colorspace_settings.name = "Non-Color"
            self._updateNormalLinks()
            self._updateBlendMaskMode()

    def setBlendMaskThreshold(self,value):
        blendMaskThresholdNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailblendMaskThreshold.value)
        if blendMaskThresholdNode:
            blendMaskThresholdNode.outputs[0].default_value = value

    def setBlendMaskTex(self, texture):
        detailBlendTexNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.blendMaskTex.value)
        if detailBlendTexNode:
            detailBlendTexNode.image = texture
            if texture is not None:
                detailBlendTexNode.image.colorspace_settings.name = "Non-Color"
            self._updateBlendMaskLinks()

    def setDetailUVScale(self, uvScale):
        nodeDetailUvScale = getNodeByName(self.nodes, MSFS2024_ShaderNodes.detailUVScale.value)

        if (nodeDetailUvScale):
            nodeDetailUvScale.outputs[0].default_value = uvScale

    def setUVOffsetU(self, offsetU):
        uvOffsetUNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.uvOffsetU.value)

        if (uvOffsetUNode):
            uvOffsetUNode.outputs[0].default_value = offsetU
    
    def setUVOffsetV(self, offsetV):
        uvOffsetVNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.uvOffsetV.value)

        if (uvOffsetVNode):
            uvOffsetVNode.outputs[0].default_value = offsetV

    def setUVTilingU(self, tilingU):
        uvTilingUNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.uvTilingU.value)

        if (uvTilingUNode):
            uvTilingUNode.outputs[0].default_value = tilingU

    def setUVTilingV(self, tilingV):
        uvTilingVNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.uvTilingV.value)

        if (uvTilingVNode):
            uvTilingVNode.outputs[0].default_value = tilingV

    def setUVRotation(self, rotation):
        uvRotationNode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.uvRotation.value)

        if (uvRotationNode):
            uvRotationNode.outputs[0].default_value = rotation

    def setBlendMode(self, blendMode):
        if blendMode == "BLEND":
            self._makeAlphaBlend()
        elif blendMode == "MASK":
            self._makeMasked()
        elif blendMode == "DITHER":
            self._makeDither()
        else:
            self._makeOpaque()
 
    def updateDoubleSided(self):
        self.material.use_backface_culling = not getattr(self.material, MSFS2024_MaterialProperties.doubleSided.attributeName())

    def updateAlphaCutoff(self):
        self.material.alpha_threshold = getattr(self.material, MSFS2024_MaterialProperties.alphaCutoff.attributeName())
    #endregion

    #region ###Shader Graph Nodes###
    def drawblendMaskShaderNodeGroup(self, group):
        
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            hidden = False
        )

        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (1625.0, 30.0),
            hidden = False
        )
        #region Inputs
        # Base Color A
        baseColorAlphaInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.detailColorTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        baseColorAlphaInput.default_value = 1.0
        
        # Blend Mask Texture
        blendMaskTexInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.blendMaskTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        blendMaskTexInput.default_value = (1.0, 1.0, 1.0, 1.0)

        # Enable Blend Mask Bool
        enableBlendMaskInput = addGroupInput(
            group = group, 
            inputName = "Enable Blend Mask",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        enableBlendMaskInput.default_value = 0.0

        # Detail Color Texture
        blendMaskThresholdInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.detailblendMaskThreshold.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        blendMaskThresholdInput.default_value = 0

        # Switch blend mode
        switchToBlendModeInput = addGroupInput(
            group = group, 
            inputName = "Switch To Blend Mode",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        switchToBlendModeInput.default_value = 0
        #endregion

        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "Mask",
            outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        #endregion

        #region #Common Nodes#
        
        vertexColorMapNode = addNode(
        nodes = group.nodes,
        name = MSFS2024_NodesSockets.vertexColor.value,
        typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVertexColor.value,
        location = (0.0, 174),
        hidden = False
        )   
        #endregion

        #region #Detail Mode#

        detailMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.detailMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.detailMaskFrame.color()
        )

        detailMultiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (230, 30),
            frame = detailMaskFrame
        )

        rerouteDetailNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.nodeReroute.value,
            location = (1114, 20),
            frame = detailMaskFrame
        )

        #region Links
        link(group.links, vertexColorMapNode.outputs[1], detailMultiplyNode.inputs[0])
        link(group.links, inputNode.outputs[0], detailMultiplyNode.inputs[1])
        link(group.links, detailMultiplyNode.outputs[0], rerouteDetailNode.inputs[0])
        #endregion
        #endregion #Detail Mode#

        #region #Blend Mode#
        blendMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.blendMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.blendMaskFrame.color()
        )

        blendSeparateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (220, -250),
            frame=blendMaskFrame
        )
        blendSubstractNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (450, -330),
            frame=blendMaskFrame
        )
        blendAddNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (450, -225),
            frame=blendMaskFrame
        )

  
        blendLinearStepNode=MSFS2024_NodesLibrary.addLinearStepNode(
                                        node_tree = group,
                                        location = (700,-200),
                                        frame=blendMaskFrame)
        
        

        blendSwitchNode = MSFS2024_NodesLibrary.addSwitchNode(
                                    node_tree = group,
                                   location = (975, -90),
                                   frame=blendMaskFrame)


        #region Links
        link(group.links, inputNode.outputs[1], blendSeparateColorNode.inputs[0])

        link(group.links, inputNode.outputs[3], blendAddNode.inputs[0])
        link(group.links, inputNode.outputs[3], blendSubstractNode.inputs[1])
        

        link(group.links, blendSeparateColorNode.outputs[0], blendAddNode.inputs[1])
        link(group.links, blendSeparateColorNode.outputs[0], blendSubstractNode.inputs[0])

        link(group.links, blendSubstractNode.outputs[0], blendLinearStepNode.inputs[0])
        link(group.links, blendAddNode.outputs[0], blendLinearStepNode.inputs[1])
        link(group.links, vertexColorMapNode.outputs[1], blendLinearStepNode.inputs[2])

        link(group.links, inputNode.outputs[2], blendSwitchNode.inputs[0])
        link(group.links, vertexColorMapNode.outputs[1], blendSwitchNode.inputs[1])
        link(group.links, blendLinearStepNode.outputs[0], blendSwitchNode.inputs[2])
         
        #endregion

        #endregion #Blend Mode#

        modeSwitchNode=MSFS2024_NodesLibrary.addSwitchNode(
            group,
            location=(1325,30)
            )
        
        link(group.links, inputNode.outputs[4], modeSwitchNode.inputs[0])
        link(group.links, rerouteDetailNode.outputs[0], modeSwitchNode.inputs[1])
        link(group.links, blendSwitchNode.outputs[0], modeSwitchNode.inputs[2])
        link(group.links, modeSwitchNode.outputs[0], outputNode.inputs[0])

    def drawBaseColorShaderNodeGroup(self, group):
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            hidden = False
        )

        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (2600.0, -350.0),
            hidden = False
        )

        #region Inputs
        # Base Color RGB
        baseColorRGBInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.baseColorRGB.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        baseColorRGBInput.default_value = (1.0, 1.0, 1.0, 1.0)
        
        # Base Color Texture
        baseColorTexInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.baseColorTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        baseColorTexInput.default_value = (1.0, 1.0, 1.0, 1.0)

        # Detail Color Texture
        detailColorTexInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.detailColorTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        detailColorTexInput.default_value = (1.0, 1.0, 1.0, 1.0)

        # Detail Color Texture Alpha
        detailColorTexAlphaInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.detailColorTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        detailColorTexAlphaInput.default_value = 1.0
        
        enableDetailColorInput = addGroupInput(
            group = group,
            inputName = "Enable Detail Color",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        enableDetailColorInput.default_value = 0

        maskInput = addGroupInput(
            group = group,
            inputName = "Mask",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        maskInput.default_value = 0

        switchToBlendModeInput = addGroupInput(
            group = group,
            inputName = MSFS2024_NodesSockets.switchToBlendMode.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        switchToBlendModeInput.default_value = 0
        #endregion

        #region Outputs
        # Base Color RGB
        addGroupOutput(
            group = group,
            outputName = MSFS2024_ShaderNodes.baseColorRGB.value,
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion

        #region #Common Nodes#
        mulBaseColorRGBNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            blend_type = MSFS2024_NodeBlendTypes.multiply.value,
            location = (270.0, -25.0),
        )
        mulBaseColorRGBNode.inputs[0].default_value = 1.0
 
        vertexColorMapNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.vertexColor.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVertexColor.value,
            location = (1500, -435),
            hidden = False
        )  
        #region Links
        link(group.links, inputNode.outputs[0], mulBaseColorRGBNode.inputs[1])
        link(group.links, inputNode.outputs[1], mulBaseColorRGBNode.inputs[2])
        #endregion
        #endregion #Common Nodes#

        #region #Detail Mode#
        detailMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.detailMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.detailMaskFrame.color()
        )

        detailMutiplyRGBNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            blend_type = MSFS2024_NodeBlendTypes.multiply.value,
            location = (585.0, -190.0),
            frame=detailMaskFrame
        )
        detailMutiplyRGBNode.inputs[0].default_value = 1.0

        squareRootColorNode = MSFS2024_NodesLibrary.addSquareRootColorNode(
            group,
            frame = detailMaskFrame,
            location = (800,-240)
        )

        smoothStepNode = addNode(
            nodes = group.nodes,
            name = "Smoothstep",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMapRange.value,
            location = (1075.0, -275.0),
            frame = detailMaskFrame
        )
        smoothStepNode.data_type = MSFS2024_NodeDataTypes.float_vector.value
        smoothStepNode.interpolation_type = MSFS2024_MapRangeType.smoothstep.value

        detailMutiplyAlphaNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation =MSFS2024_NodeMathOpe.multiply.value,
            location = (1200.0, -120.0),
            frame=detailMaskFrame
        )
        detailMutiplyAlphaNode.inputs[0].default_value = 1.0

        detailMixNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (1425.0, -165.0),
            frame=detailMaskFrame
        )
   
        detailSwitchNode = MSFS2024_NodesLibrary.addSwitchNode(
            group,
            frame = detailMaskFrame,
            location = (1600,0)
        )

        detailMutiplyVCNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            blend_type = MSFS2024_NodeBlendTypes.multiply.value,
            location = (1900.0, -25.0),
            frame=detailMaskFrame
        )
        
        detailMutiplyVCNode.inputs[0].default_value = 1.0
        

        #region Links
        link(group.links, mulBaseColorRGBNode.outputs[0], detailMutiplyRGBNode.inputs[1])
        link(group.links, inputNode.outputs[2], detailMutiplyRGBNode.inputs[2])

        link(group.links, detailMutiplyRGBNode.outputs[0], squareRootColorNode.inputs[0])
        link(group.links, squareRootColorNode.outputs[0], smoothStepNode.inputs[6])## input[6] == "Vector"

        link(group.links, inputNode.outputs[3], detailMutiplyAlphaNode.inputs[0])
        link(group.links, inputNode.outputs[5], detailMutiplyAlphaNode.inputs[1])

        link(group.links, detailMutiplyAlphaNode.outputs[0], detailMixNode.inputs[0])
        
        link(group.links, mulBaseColorRGBNode.outputs[0], detailMixNode.inputs[1])
        link(group.links, smoothStepNode.outputs[1], detailMixNode.inputs[2])

        link(group.links, inputNode.outputs[4], detailSwitchNode.inputs[0])
        link(group.links, mulBaseColorRGBNode.outputs[0], detailSwitchNode.inputs[1])
        link(group.links, detailMixNode.outputs[0], detailSwitchNode.inputs[2])

        link(group.links, detailSwitchNode.outputs[0], detailMutiplyVCNode.inputs[1])
        link(group.links, vertexColorMapNode.outputs[0], detailMutiplyVCNode.inputs[2])
        #endregion 
        #endregion #Detail Mode#

        #region #Blend Mode#
        blendMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.blendMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.blendMaskFrame.color()
        )

        blendMixNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (585.0, -600.0),
            frame=blendMaskFrame
        )

        blendMultiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            blend_type = MSFS2024_NodeBlendTypes.multiply.value,
            location = (1900.0, -600.0),
            frame=blendMaskFrame
        )
        blendMultiplyNode.inputs[0].default_value = 1.0
        #region Links
        link(group.links, inputNode.outputs[5], blendMixNode.inputs[0])
        link(group.links, inputNode.outputs[2], blendMixNode.inputs[1])
        link(group.links, mulBaseColorRGBNode.outputs[0], blendMixNode.inputs[2])

        link(group.links, blendMixNode.outputs[0], blendMultiplyNode.inputs[1])
        link(group.links, vertexColorMapNode.outputs[0], blendMultiplyNode.inputs[2])

        #endregion 
        #endregion #Blend Mode#
        modeSwitchNode = MSFS2024_NodesLibrary.addSwitchNode(
            group,
            location = (2250,-330)
        ) #Switch between detail and blend mode
        link(group.links, inputNode.outputs[6], modeSwitchNode.inputs[0])
        link(group.links, detailMutiplyVCNode.outputs[0], modeSwitchNode.inputs[1])
        link(group.links, blendMultiplyNode.outputs[0], modeSwitchNode.inputs[2])
        link(group.links, modeSwitchNode.outputs[0], outputNode.inputs[0])

    def drawAlphaShaderNodeGroup(self, group):
        ## Group Nodes
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            hidden = False
        )
        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (1000.0, 0.0),
            hidden = False
        )

        # Blend Alpha Map (Detail alpha operator)
        blendAlphaMapNode = addNode(
            nodes = group.nodes,
            name = "Blend Alpha Map",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (300.0, -100.0),
            width = 200.0
        )

        ## Base Color Multiplier
        mulBaseColorANode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (600.0, -50.0),
            width = 200.0
        )

        ## Inputs
        # Alpha Scalar
        alphaScalarInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.baseColorA.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        alphaScalarInput.default_value = 1.0

        # Base Color Texture Alpha
        baseColorTextAlphaInput = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.baseColorTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        baseColorTextAlphaInput.default_value = 1.0

        # Detail Color Texture Alpha
        detailColorTexalpha = addGroupInput(
            group = group, 
            inputName = MSFS2024_ShaderNodes.detailColorTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        detailColorTexalpha.default_value = 1.0

        ## Outputs
        # Alpha
        addGroupOutput(
            group = group,
            outputName = MSFS2024_ShaderNodes.baseColorA.value,
            outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        ## Links
        link(group.links, inputNode.outputs[1], blendAlphaMapNode.inputs[0])
        link(group.links, inputNode.outputs[2], blendAlphaMapNode.inputs[1])
        link(group.links, inputNode.outputs[0], mulBaseColorANode.inputs[0])
        link(group.links, blendAlphaMapNode.outputs[0], mulBaseColorANode.inputs[1])
        link(group.links, mulBaseColorANode.outputs[0], outputNode.inputs[0])

    def drawUVShaderNodeGroup(self, group):
        ## Group Nodes
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            location = (-450.0, 10.0),
            hidden = False
        )
        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (1235.0, 10.0),
            hidden = False
        )

        #region ## Inputs
        # UV Offset U
        uvOffsetUInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.uvOffsetU.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # UV Offset V
        uvOffsetVInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.uvOffsetV.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # UV Tiling U
        uvTilingUInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.uvTilingU.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # UV Tiling V
        uvTilingVInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.uvTilingV.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # UV Rotation
        uvRotationInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.uvRotation.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # Detail UV Scale
        detailUVScaleInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.detailUVScale.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        #endregion

        #region ## Outputs
        # UV Coordinates
        addGroupOutput(
            group = group,
            outputName = "UV Coordinate",
            outputType = MSFS2024_GroupTypes.nodeSocketVector.value
        )

        # Detail UV Coordinates
        addGroupOutput(
            group = group,
            outputName = "Detail UV Coordinate",
            outputType = MSFS2024_GroupTypes.nodeSocketVector.value
        )
        addGroupOutput(
            group = group,
            outputName = "UV2",
            outputType = MSFS2024_GroupTypes.nodeSocketVector.value
        )
        #endregion

        #region ## Nodes
        # UV Map
        uvMapNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeUVMap.value,
            location = (-606.0, 115.0)
        )

        subHalfNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (-355.0, 90.0)
        )
        subHalfNode.inputs[1].default_value=(0.5,0.5,0.0)

        toRadNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.radians.value,
            location = (-245.0, 36.0)
        )
        
        # Rotate UV
        uvRotateNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorRotate.value,
            location = (-175.0, 85.0)
        )

        # Separate UV
        separateUVNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateXYZ.value,
            location = (5.0, 86.0)
        )

        # Multiply Tiling U
        multiplyTilingUNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (200.0, 92.0)
        )

        # Multiply Tiling V
        multiplyTilingVNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (200.0, 44.0)
        )

        # Add Offset U
        subOffsetUNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (450.0, -10.0)
        )

        # Add Offset V
        addOffsetVNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (450.0, -50.0)
        )

        # Combine UV
        combineUVNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeCombineXYZ.value,
            location = (710.0, -10.0)
        )

        addHalfNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (885.0, -10.0)
        )

        addHalfNode.inputs[1].default_value=(0.5,0.5,0.0)

        # Multiply Detail UV Scale
        multiplyDetailUVScaleNode = addNode(
            nodes = group.nodes,
            name = "Multiply (UV * Detail Scale)",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (1060.0, -35.0)
        )
        uv2Node = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeUVMap.value,
            location = (885.0, -100.0)
        )
        uv2Node.uv_map ="UV Map.001"

        #endregion

        #region ## Links
        link(group.links, uvMapNode.outputs[0], subHalfNode.inputs[0])
        link(group.links, subHalfNode.outputs[0], uvRotateNode.inputs[0])
        link(group.links, inputNode.outputs[4], toRadNode.inputs[0])
        link(group.links, toRadNode.outputs[0], uvRotateNode.inputs[3])

        link(group.links, uvRotateNode.outputs[0], separateUVNode.inputs[0])

        link(group.links, separateUVNode.outputs[0], multiplyTilingUNode.inputs[0])
        link(group.links, separateUVNode.outputs[1], multiplyTilingVNode.inputs[0])

        link(group.links, multiplyTilingUNode.outputs[0], subOffsetUNode.inputs[0])
        link(group.links, multiplyTilingVNode.outputs[0], addOffsetVNode.inputs[0])

        link(group.links, subOffsetUNode.outputs[0], combineUVNode.inputs[0])
        link(group.links, addOffsetVNode.outputs[0], combineUVNode.inputs[1])

        link(group.links, inputNode.outputs[0], subOffsetUNode.inputs[1])
        link(group.links, inputNode.outputs[1], addOffsetVNode.inputs[1])
        link(group.links, inputNode.outputs[2], multiplyTilingUNode.inputs[1])
        link(group.links, inputNode.outputs[3], multiplyTilingVNode.inputs[1])
        
        link(group.links, inputNode.outputs[5], multiplyDetailUVScaleNode.inputs[1])

        link(group.links, combineUVNode.outputs[0], addHalfNode.inputs[0])
        link(group.links, addHalfNode.outputs[0], outputNode.inputs[0])

        link(group.links, addHalfNode.outputs[0], multiplyDetailUVScaleNode.inputs[0])
        link(group.links, multiplyDetailUVScaleNode.outputs[0], outputNode.inputs[1])
        link(group.links, uv2Node.outputs[0], outputNode.inputs[2])
        #endregion
        return

    def drawOMRShaderNodeGroup(self, group):
        ## Group Nodes
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            location = (-220.0, 0.0),
            width = 300.0,
            hidden = False
        )
        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (2725.0, 0.0),
            width = 200.0,
            hidden = False
        )
        #region Inputs
        # Metallic Scale
        metallicScaleInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.metallicScale.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # Rougness Scale
        roughnessScaleInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.roughnessScale.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )

        # Comp (OMR) Texture
        omrTexInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.compTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        omrTexInput.default_value = (1.0, 1.0, 1.0, 1.0)

        # Detail Comp (OMR) Texture
        omrDetailTexInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.detailCompTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        omrDetailTexInput.default_value = (0.0, 0.0, 0.0, 1.0)

        enableDetailInput = addGroupInput(
            group = group,
            inputName = "Enable Detail",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        enableDetailInput.default_value = 0

        maskInput = addGroupInput(
            group = group,
            inputName = "Mask",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        maskInput.default_value = 0

        switchToBlendModeInput = addGroupInput(
            group = group,
            inputName = MSFS2024_NodesSockets.switchToBlendMode.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        switchToBlendModeInput.default_value = 0
        #endregion

        #region Outputs
        # Metallic Scale
        addGroupOutput(
            group = group,
            outputName = MSFS2024_ShaderNodes.metallicScale.value,
            outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        
        # Roughness Scale
        addGroupOutput(
            group = group,
            outputName = MSFS2024_ShaderNodes.roughnessScale.value,
            outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        
        # Occlusion Scale
        addGroupOutput(
            group = group,
            outputName = "Occlusion Scale",
            outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        #endregion
       
        #region #Detail Mode#
        detailMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.detailMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.detailMaskFrame.color()
        )

        unpackDetailORMNode = MSFS2024_NodesLibrary.addUnpackDetailORMNode(
            node_tree=group,
            location = (195, 195.0),
            frame=detailMaskFrame
        )

        detailMixNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (575.0, 90.0),
            frame=detailMaskFrame
        )
        detailMixNode.inputs[1].default_value = (0.0,0.0,0.0,1.0)

        detailBaseSeparateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (830, 175),
            width=300,
            frame=detailMaskFrame
        )

        detailSeparateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (830, 86),
            width=300,
            frame=detailMaskFrame
        )

        detailRoughnessMultiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (1245, 175),
            frame=detailMaskFrame
        )
        detailMetallicMultiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (1245, 85),
            frame=detailMaskFrame
        )
        detailAOAddNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (1525, 271),
            frame=detailMaskFrame
        )
        detailAOAddNode.use_clamp=True

        detailRoughnessAddNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (1525, 175),
            frame=detailMaskFrame
        )
        detailRoughnessAddNode.use_clamp=True

        detailMetallicAddNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (1525, 85),
            frame=detailMaskFrame
        )
        detailMetallicAddNode.use_clamp=True

        detailAddCombineColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeCombineColor.value,
            location = (1755, 175),
            frame=detailMaskFrame
        )

        detailCombineColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeCombineColor.value,
            location = (1675, 425),
            frame=detailMaskFrame
        )
        detailCombineColorNode.inputs[0].default_value = 1

        detailSwitchNode = MSFS2024_NodesLibrary.addSwitchNode (
            node_tree = group,
            frame = detailMaskFrame,
            location = (2020,175)
        )
        
        #region Links
        link(group.links, inputNode.outputs[2], detailBaseSeparateColorNode.inputs[0])
        link(group.links, inputNode.outputs[3], unpackDetailORMNode.inputs[0])
        link(group.links, inputNode.outputs[5], detailMixNode.inputs[0])
        link(group.links, unpackDetailORMNode.outputs[0], detailMixNode.inputs[2])
        link(group.links, detailMixNode.outputs[0], detailSeparateColorNode.inputs[0])

        link(group.links, detailBaseSeparateColorNode.outputs[0], detailAOAddNode.inputs[0])
        link(group.links, detailBaseSeparateColorNode.outputs[1], detailRoughnessMultiplyNode.inputs[0])
        link(group.links, detailBaseSeparateColorNode.outputs[2], detailMetallicMultiplyNode.inputs[0])

        link(group.links, inputNode.outputs[1], detailRoughnessMultiplyNode.inputs[1])
        link(group.links, inputNode.outputs[0], detailMetallicMultiplyNode.inputs[1])
        
        link(group.links, detailRoughnessMultiplyNode.outputs[0], detailRoughnessAddNode.inputs[0])
        link(group.links, detailMetallicMultiplyNode.outputs[0], detailMetallicAddNode.inputs[0])

        link(group.links, detailSeparateColorNode.outputs[0], detailAOAddNode.inputs[1])
        link(group.links, detailSeparateColorNode.outputs[1], detailRoughnessAddNode.inputs[1])
        link(group.links, detailSeparateColorNode.outputs[2], detailMetallicAddNode.inputs[1])

     
        link(group.links, detailRoughnessMultiplyNode.outputs[0], detailCombineColorNode.inputs[1])
        link(group.links, detailMetallicMultiplyNode.outputs[0], detailCombineColorNode.inputs[2])

        link(group.links, detailAOAddNode.outputs[0], detailAddCombineColorNode.inputs[0])
        link(group.links, detailRoughnessAddNode.outputs[0], detailAddCombineColorNode.inputs[1])
        link(group.links, detailMetallicAddNode.outputs[0], detailAddCombineColorNode.inputs[2])

        link(group.links, inputNode.outputs[4], detailSwitchNode.inputs[0])
        link(group.links, detailCombineColorNode.outputs[0], detailSwitchNode.inputs[1])
        link(group.links, detailAddCombineColorNode.outputs[0], detailSwitchNode.inputs[2])
        
        
        #endregion
        #endregion

        #region #Blend Mode#
        blendMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.blendMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.blendMaskFrame.color()
        )
        blendMixNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (575.0, -175.0),
            frame=blendMaskFrame
        )
        blendSeparateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (830, -175),
            width=300,
            frame=blendMaskFrame
        )
        blendRoughnessMultNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (1245, -265),
            frame=blendMaskFrame
        )
        blendMetallicMultNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (1245, -335),
            frame=blendMaskFrame
        )
        blendCombineColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeCombineColor.value,
            location = (1738, -239),
            frame=blendMaskFrame
        )
        #region Links
  
        link(group.links, inputNode.outputs[2], blendMixNode.inputs[2])
        link(group.links, inputNode.outputs[3], blendMixNode.inputs[1])
        link(group.links, inputNode.outputs[5], blendMixNode.inputs[0])

        link(group.links, blendMixNode.outputs[0], blendSeparateColorNode.inputs[0])

        link(group.links, blendSeparateColorNode.outputs[1], blendRoughnessMultNode.inputs[0])
        link(group.links, blendSeparateColorNode.outputs[2], blendMetallicMultNode.inputs[0])

        link(group.links, inputNode.outputs[1], blendRoughnessMultNode.inputs[1])
        link(group.links, inputNode.outputs[0], blendMetallicMultNode.inputs[1])

        link(group.links, blendSeparateColorNode.outputs[0], blendCombineColorNode.inputs[0])
        link(group.links, blendRoughnessMultNode.outputs[0], blendCombineColorNode.inputs[1])
        link(group.links, blendMetallicMultNode.outputs[0], blendCombineColorNode.inputs[2])
        #endregion
        #endregion

        modeSwitchNode=MSFS2024_NodesLibrary.addSwitchNode(
            group,
            location = (2270,0)
            ) #Switch between detail and blend mode
        switchSeparateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (2495, -65),
        )
        link(group.links, inputNode.outputs[6], modeSwitchNode.inputs[0])
        link(group.links, detailSwitchNode.outputs[0], modeSwitchNode.inputs[1])
        link(group.links, blendCombineColorNode.outputs[0], modeSwitchNode.inputs[2])

        link(group.links, modeSwitchNode.outputs[0], switchSeparateColorNode.inputs[0])
        link(group.links, switchSeparateColorNode.outputs[0], outputNode.inputs[2])
        link(group.links, switchSeparateColorNode.outputs[1], outputNode.inputs[1])
        link(group.links, switchSeparateColorNode.outputs[2], outputNode.inputs[0])

    def drawEmissiveShaderNodeGroup(self, group):
        ## Group Nodes
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            width = 200.0,
            hidden = False
        )
        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (500.0, 0.0),
            width = 200.0,
            hidden = False
        )

        ## Emissive Multiplier
        emissiveMulNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            blend_type = MSFS2024_NodeMathOpe.multiply.value,
            location = (300.0, -50.0)
        )

        ## Inputs
        # Emissive Scale
        emissiveScaleInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.emissiveScale.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )

        # Emissive Color
        emissiveColorInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.emissiveColor.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )

        # Emissive Texture
        emissiveTexInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.emissiveTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        emissiveTexInput.default_value = (1.0, 1.0, 1.0, 1.0)

        ## Outputs
        # Emissive Color
        addGroupOutput(
            group = group,
            outputName = MSFS2024_ShaderNodes.emissiveColor.value,
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )

        ## Links
        link(group.links, inputNode.outputs[0], emissiveMulNode.inputs[0])
        link(group.links, inputNode.outputs[1], emissiveMulNode.inputs[1])
        link(group.links, inputNode.outputs[2], emissiveMulNode.inputs[2])

        link(group.links, emissiveMulNode.outputs[0], outputNode.inputs[0])

    def drawNormalShaderNodeGroup(self, group):
        ## Group Nodes
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            width = 200.0,
            hidden = False
        )
        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (2125.0, 0.0),
            width = 200.0,
            hidden = False
        )
        #region Inputs
        # Normal Scale Input
        normalScaleInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.normalScale.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        normalScaleInput.default_value = 1.0

        # Normal Texture Input
        normalTexInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.normalTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        normalTexInput.default_value = (0.5, 0.5, 1.0, 1.0)

        # Detail Normal Scale Input
        detailNormalScaleInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.detailNormalScale.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        detailNormalScaleInput.default_value = 1.0

        # Detail Normal Texture Input
        detailNormalTexInput = addGroupInput(
            group = group,
            inputName = MSFS2024_ShaderNodes.detailNormalTex.value,
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        detailNormalTexInput.default_value = (0.5, 0.5, 1.0, 1.0)

        enableDetailInput = addGroupInput(
            group = group,
            inputName = "Enable Detail",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        enableDetailInput.default_value = 0

        maskInput = addGroupInput(
            group = group,
            inputName = "Mask",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        maskInput.default_value = 0

        switchToBlendModeInput = addGroupInput(
            group = group,
            inputName = MSFS2024_NodesSockets.switchToBlendMode.value,
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        switchToBlendModeInput.default_value = 0
        #endregion
        #region Outputs
        # Normal Color
        addGroupOutput(
            group = group,
            outputName = "Normal",
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion
        #region #Common Nodes#
        # Invert Y Channel in order to obtain OpenGl normal format
        RGBCurvesNode = addNode(
            nodes = group.nodes,
            name = "Invert Y",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeRGBCurve.value,
            location = (360.0,0)
        )
        curveMapping = RGBCurvesNode.mapping.curves[1]
        curveMapping.points[0].location = (0.0, 1.0)
        curveMapping.points[1].location = (1.0, 0.0)

        ## Normal Map Sampler
        normalMapSamplerNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeNormalMap.value,
            location = (575.0, 0)
        )

        RGBCurvesDetailNode = addNode(
            nodes = group.nodes,
            name = "Invert Y",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeRGBCurve.value,
            location = (365.0, -95.0)
        )

        curveMapping = RGBCurvesDetailNode.mapping.curves[1]
        curveMapping.points[0].location = (0.0, 1.0)
        curveMapping.points[1].location = (1.0, 0.0)
        ## Detail Normal Map Sampler
        NormalMapSamplerDetailNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeNormalMap.value,
            location = (578.0, -90.0)
        )
        #region Link
        link(group.links, inputNode.outputs[0], normalMapSamplerNode.inputs[0])
        link(group.links, inputNode.outputs[1], RGBCurvesNode.inputs[1])

        link(group.links, RGBCurvesNode.outputs[0], normalMapSamplerNode.inputs[1])

        link(group.links, inputNode.outputs[2], NormalMapSamplerDetailNode.inputs[0])
        link(group.links, inputNode.outputs[3], RGBCurvesDetailNode.inputs[1])

        link(group.links, RGBCurvesDetailNode.outputs[0], NormalMapSamplerDetailNode.inputs[1])
        #endregion
        #endregion #Common Nodes#

        #region #Detail Mode#
        detailMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.detailMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.detailMaskFrame.color()
        )
        detailNeutralNormalNode = addNode(
            nodes = group.nodes,
            name = "Neutral Normal",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeNormalMap.value,
            location = (885.0, 70.0),
            frame=detailMaskFrame
        )
        detailMixNormalNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (1060.0, 115.0),
            frame=detailMaskFrame
        )
       
        detailAddNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.add.value,
            location = (1240, 110),
            frame=detailMaskFrame
        )

        detailSwitchNode = MSFS2024_NodesLibrary.addSwitchNode(
            node_tree = group,
            location = (1485,225),
            frame = detailMaskFrame
        )
        #region Links
        
        
        link(group.links, inputNode.outputs[5], detailMixNormalNode.inputs[0])
        link(group.links, detailNeutralNormalNode.outputs[0], detailMixNormalNode.inputs[1])
        link(group.links, NormalMapSamplerDetailNode.outputs[0], detailMixNormalNode.inputs[2])

        link(group.links, normalMapSamplerNode.outputs[0], detailAddNode.inputs[0])
        link(group.links, detailMixNormalNode.outputs[0], detailAddNode.inputs[1])

        link(group.links, inputNode.outputs[4], detailSwitchNode.inputs[0])
        link(group.links, normalMapSamplerNode.outputs[0], detailSwitchNode.inputs[1])
        link(group.links, detailAddNode.outputs[0], detailSwitchNode.inputs[2])
        #endregion
        #endregion #Detail Mode#

        #region #Blend Mode#
        blendMaskFrame = addNode(
            nodes = group.nodes,
            name = MSFS2024_FrameNodes.blendMaskFrame.name(),
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = MSFS2024_FrameNodes.blendMaskFrame.color()
        )
        blendMixNormalNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (1060.0, -200.0),
            frame=blendMaskFrame
        )
        
        #region Links
        link(group.links, inputNode.outputs[5], blendMixNormalNode.inputs[0])
        link(group.links, NormalMapSamplerDetailNode.outputs[0], blendMixNormalNode.inputs[1])
        link(group.links, normalMapSamplerNode.outputs[0], blendMixNormalNode.inputs[2])
        #endregion
        #endregion #Blend Mode#
        
        modeSwitchNode = MSFS2024_NodesLibrary.addSwitchNode(
            group,
            location = (1850,55)
        )#switch between detail and blend mode

        link(group.links, inputNode.outputs[6], modeSwitchNode.inputs[0])
        link(group.links, detailSwitchNode.outputs[0], modeSwitchNode.inputs[1])
        link(group.links, blendMixNormalNode.outputs[0], modeSwitchNode.inputs[2])
        link(group.links, modeSwitchNode.outputs[0], outputNode.inputs[0])
    
    def drawApplyAOGroup(self, group):
        ## Group Nodes
        inputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupInput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupInput.value,
            width = 200.0,
            hidden = False
        )
        outputNode = addNode(
            nodes = group.nodes,
            name = MSFS2024_NodesSockets.groupOutput.value,
            typeNode = MSFS2024_GroupTypes.nodeGroupOutput.value,
            location = (1776.0, 0.0),
            width = 200.0,
            hidden = False
        )
        #region Inputs
        colorInput = addGroupInput(
            group = group,
            inputName = "Color",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        colorInput.default_value = (1,1,1,1)

        aoInput = addGroupInput(
            group = group,
            inputName = "AO",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        aoInput.default_value = 1.0

        aoUV2Input = addGroupInput(
            group = group,
            inputName = "AO UV2",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        aoUV2Input.default_value = (1.0, 1.0, 1.0, 1.0)


        #endregion
        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "Color",
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion
        
        shadowMaskFrame = addNode(
            nodes = group.nodes,
            name = "Shadow Mask",
            typeNode = MSFS2024_ShaderNodeTypes.nodeFrame.value,
            color = (0.3,0.3,0.3,1)
        )

        diffuseBSDFNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeBsdfDiffuse.value,
            location = (168.0, 130.0),
            frame=shadowMaskFrame
        )

        shaderToRGBNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeShaderToRGB.value,
            location = (380.0, 130.0),
            frame=shadowMaskFrame
        )

        colorRampNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeValToRGB.value,
            location = (575.0, 124.0),
            frame=shadowMaskFrame
        )

        colorRampNode.color_ramp.elements[0].position = 0.65 
        colorRampNode.color_ramp.elements[0].color = (0,0,0,1) 
        colorRampNode.color_ramp.elements[1].position = 0.35 
        colorRampNode.color_ramp.elements[1].color = (1,1,1,1) 

        mixNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (905, 75)
        )

        separateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (220, -100)
        )

        multiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (432, -50)
        )
        multiplyColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            blend_type = MSFS2024_NodeBlendTypes.multiply.value,
            location = (658, -10)
        )
        multiplyColorNode.inputs[0].default_value = 1.0 #factor
        #region Links
        link(group.links, diffuseBSDFNode.outputs[0], shaderToRGBNode.inputs[0])
        link(group.links, shaderToRGBNode.outputs[0], colorRampNode.inputs[0])
        link(group.links, colorRampNode.outputs[0], mixNode.inputs[0])#mix node factor
        link(group.links, mixNode.outputs[0], outputNode.inputs[0])

        
        link(group.links, inputNode.outputs[2], separateColorNode.inputs[0])
        link(group.links, inputNode.outputs[1], multiplyNode.inputs[0])
        link(group.links, separateColorNode.outputs[0], multiplyNode.inputs[1])

        link(group.links, inputNode.outputs[0], multiplyColorNode.inputs[1])#mix A input
        link(group.links, multiplyNode.outputs[0], multiplyColorNode.inputs[2])#mix B input

        link(group.links, inputNode.outputs[0], mixNode.inputs[1])
        link(group.links, multiplyColorNode.outputs[0], mixNode.inputs[2])
        #endregion
        return
    #endregion