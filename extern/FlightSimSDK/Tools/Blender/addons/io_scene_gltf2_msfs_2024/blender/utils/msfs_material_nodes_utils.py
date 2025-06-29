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

import bpy

from enum import Enum

from ..utils.msfs_material_utils import MSFS2024_MaterialProperties

class MSFS2024_ShaderNodeTypes(Enum):
    nodeReroute = "NodeReroute"
    shaderNodeGroup = "ShaderNodeGroup"
    shaderNodeTree = "ShaderNodeTree"
    shaderNodeOutputMaterial = "ShaderNodeOutputMaterial"
    nodeFrame = "NodeFrame"
    shaderNodeMix = "ShaderNodeMix" #be carefull this one is not compatible in 3.3
    shaderNodeMixRGB = "ShaderNodeMixRGB" 
    nodeGroupOutput = "NodeGroupOutput"
    nodeGroupInput = "NodeGroupInput"
    shadeNodeBsdfPrincipled = "ShaderNodeBsdfPrincipled"
    shaderNodeTexImage = "ShaderNodeTexImage"
    shaderNodeVertexColor = "ShaderNodeVertexColor"
    shaderNodeMath = "ShaderNodeMath"
    shaderNodeUVMap = "ShaderNodeUVMap"
    shaderNodeCombineXYZ = "ShaderNodeCombineXYZ"
    shaderNodeCombineColor = "ShaderNodeCombineColor"
    shaderNodeVectorMath = "ShaderNodeVectorMath"
    shaderNodeSeparateRGB = "ShaderNodeSeparateRGB"
    shaderNodeSeparateColor = "ShaderNodeSeparateColor"
    shaderNodeSeparateXYZ = "ShaderNodeSeparateXYZ"
    shaderNodeNormalMap = "ShaderNodeNormalMap"
    shaderNodeRGB = "ShaderNodeRGB"
    shaderNodeValue = "ShaderNodeValue"
    shaderNodeRGBCurve = "ShaderNodeRGBCurve"
    shaderNodeMapRange = "ShaderNodeMapRange"
    shaderNodeVectorRotate = "ShaderNodeVectorRotate"
    shaderNodeClamp = "ShaderNodeClamp"
    shaderNodeBsdfDiffuse = "ShaderNodeBsdfDiffuse"
    shaderNodeShaderToRGB = "ShaderNodeShaderToRGB"
    shaderNodeValToRGB = "ShaderNodeValToRGB" #colorRamp

class MSFS2024_NodeDataTypes(Enum):
    float = "FLOAT"
    vector = "VECTOR"
    float_vector = "FLOAT_VECTOR"
    color = "COLOR"
    rgba = "RGBA"

class MSFS2024_NodeBlendTypes(Enum):
    mix = "MIX"
    darken = "DARKEN"
    multiply = "MULTIPLY"
    burn = "BURN"
    lighten = "LIGHTEN"
    screen = "SCREEN"
    dodge = "DODGE"
    add = "ADD"
    overlay = "OVERLAY"
    soft_light = "SOFT_LIGHT"
    linear_light = "LINEAR_LIGHT"
    difference = "DIFFERENCE"
    exclusion = "EXCLUSION"
    subtract = "SUBTRACT"
    divide = "DIVIDE"
    hue = "HUE"
    saturation = "SATURATION"
    color = "COLOR"
    value = "VALUE"

class MSFS2024_NodeMathOpe(Enum):
    # Arithmetic
    add = "ADD"
    subtract = "SUBTRACT"
    multiply = "MULTIPLY"
    divide = "DIVIDE"
    multiply_add = "MULTIPLY_ADD"
    power = "POWER"
    logarithm = "LOGARITHM"
    sqrt = "SQRT"
    inverse_sqrt = "INVERSE_SQRT"
    absolute = "ABSOLUTE"
    exponent = "EXPONENT"
    
    # Comparison
    minimum = "MINIMUM"
    maximum = "MAXIMUM"
    less_than = "LESS_THAN"
    greater_than = "GREATER_THAN"
    sign = "SIGN"
    compare = "COMPARE"
    smooth_min = "SMOOTH_MIN"
    smooth_max = "SMOOTH_MAX"
    
    # Rounding
    round = "ROUND"
    floor = "FLOOR"
    ceil = "CEIL"
    trunc = "TRUNC"
    fract = "FRACT"
    modulo = "MODULO"
    floored_modulo = "FLOORED_MODULO"
    wrap = "WRAP"
    snap = "SNAP"
    pingpong = "PINGPONG"
    
    # Trigonometric
    sine = "SINE"
    cosine = "COSINE"
    tangent = "TANGENT"
    arcsine = "ARCSINE"
    arccosine = "ARCCOSINE"
    arctangent = "ARCTANGENT"
    arctan2 = "ARCTAN2"
    sinh = "SINH"
    cosh = "COSH"
    tanh = "TANH"
    
    # Conversion
    radians = "RADIANS"
    degrees = "DEGREES"

class MSFS2024_MapRangeType(Enum):
    linear = "LINEAR"
    stepped = "STEPPED"
    smoothstep = "SMOOTHSTEP"
    smootherstep = "SMOOTHERSTEP"

class MSFS2024_FrameNodes(Enum):
    maskFrame = "Mask Frame", (0.5, 0.5, 0.5)
    detailMaskFrame = "Detail", (0.2, 0.35, 0.2)
    blendMaskFrame = "Blend", (0.35, 0.2, 0.2)
    uvFrame = "UVs Frame", (0.3, 0.3, 0.5)
    omrFrame = "Occlusion Metallic Roughness Frame", (0.1, 0.4, 0.6)
    emissiveFrame = "Emissive Frame", (0.1, 0.5, 0.3)
    normalFrame = "Normal Frame", (0.5, 0.25, 0.25)
    anisotropicFrame = "Anisotropic Frame", (0.35, 0.6, 0.1)
    parallaxFrame = "Parallax Frame", (0.5, 0.1, 0.3)
    clearcoatFrame = "Clearcoat Frame", (0.6, 0.2, 0.1)
    baseColorInputsFrame = "Base Color Inputs Frame", (0.5, 0.1, 0.0)
    alphaInputsFrame = "Alpha Inputs Frame", (0.6, 0.6, 0.0)
    decalFrame = "Decal Frame", (0.3, 0.6, 0.0)
    decalBlendMaskedFrame = "Decal BlendMasked Frame", (0.45, 0.6, 0.1)
    decalFrostedFrame = "Decal Frosted Frame", (0.1, 0.3, 0.6)
    frostFrame = "Frost", (0.4, 0.3, 0.6)
    frostTintFrame = "Frost Tint", (0.4, 0.5, 0.6)

    def name(self):
        return self.value[0]

    def color(self):
        return self.value[1]
    
class MSFS2024_NodesSockets(Enum):
    """
    Miscellaneous nodes, Inputs/Outputs names.
    """

    vertexColor = "Vertex Color"

    switchToBlendMode = "Switch To Blend Mode"

    groupInput = "Group Input"
    groupOutput = "Group Output"

class MSFS2024_ShaderNodes(Enum):
    """
    Main Graph Nodes Names.
    """
    glTFSettings = "glTF Settings"

    #region common
    baseColorTex = MSFS2024_MaterialProperties.baseColorTexture.name()
    baseColorRGB = MSFS2024_MaterialProperties.baseColor.name()

    baseColorA = "Base Color (A)"
    alphaCutoff = MSFS2024_MaterialProperties.alphaCutoff.name()

    compTex = MSFS2024_MaterialProperties.omrTexture.name()
    roughnessScale = MSFS2024_MaterialProperties.roughnessScale.name()
    metallicScale = MSFS2024_MaterialProperties.metallicScale.name()

    emissiveTex = MSFS2024_MaterialProperties.emissiveTexture.name()
    emissiveColor = MSFS2024_MaterialProperties.emissiveColor.name()
    emissiveScale = MSFS2024_MaterialProperties.emissiveScale.name()

    normalTex = MSFS2024_MaterialProperties.normalTexture.name()
    normalScale = MSFS2024_MaterialProperties.normalScale.name()

    detailColorTex = MSFS2024_MaterialProperties.detailColorTexture.name()
    detailCompTex = MSFS2024_MaterialProperties.detailOmrTexture.name()
    detailNormalTex = MSFS2024_MaterialProperties.detailNormalTexture.name()
    detailNormalScale = MSFS2024_MaterialProperties.detailNormalScale.name()

    occlusionUV2Tex = MSFS2024_MaterialProperties.occlusionUV2.name()

    blendMaskTex = MSFS2024_MaterialProperties.blendMaskTexture.name()
    detailblendMaskThreshold = MSFS2024_MaterialProperties.detailBlendThreshold.name()
    #endregion

    #region Decal 
    decalBlendMaskTex = MSFS2024_MaterialProperties.decalBlendMaskTexture.name()
    decalBlendMaskThreshold = MSFS2024_MaterialProperties.decalblendMaskedThreshold.name()
    decalBlendMaskSharpness = MSFS2024_MaterialProperties.decalblendSharpness.name()
    decalFreezeFactor = MSFS2024_MaterialProperties.decalFreezeFactor.name()
    #endregion

    #region UV
    uvOffsetU = MSFS2024_MaterialProperties.uvOffsetU.name()
    uvOffsetV = MSFS2024_MaterialProperties.uvOffsetV.name()
    uvTilingU = MSFS2024_MaterialProperties.uvTilingU.name()
    uvTilingV = MSFS2024_MaterialProperties.uvTilingV.name()
    uvRotation = MSFS2024_MaterialProperties.uvRotation.name()
    detailUVScale = MSFS2024_MaterialProperties.detailUVScale.name()
    #endregion
    behindGlassTex = MSFS2024_MaterialProperties.behindGlassColorTexture.name()

    #region clearcoat
    clearcoatTex = "Clearcoat" #TODO replace by material properties
    clearcoatNormalTex = MSFS2024_MaterialProperties.clearcoatNormalTexture.name()
    clearcoatSeparate = "Clearcoat Separate" #TODO replace by material properties
    #endregion

    principledBSDF = "Principled BSDF Shader"

class MSFS2024_GroupNodes(Enum):
    blendMaskGroup = "Blend Mask Group"
    baseColorGroup = "Base Color Group"
    alphaGroup = "Alpha Group"
    uvGroup = "UV Group"
    omrGroup = "Occlusion Metallic Roughness Group"
    emissiveGroup = "Emissive Group"
    normalGroup = "Normal Group"
    applyAOGroup = "Apply AO Group"
    decalGroup = "Decal Group"
    decalBlendMaskedGroup = "Decal BlendMasked Group"
    decalFrostedGroup = "Decal Frosted Group"
    #library group:
    linearStepGroup = "LinearStep"
    switchGroup = "Switch"
    squareRootColorGroup = "Square Root Color"
    unpackDetailORMGroup = "Unpack Detail ORM"

class MSFS2024_AnisotropicNodes(Enum):
    anisotropicTex = "Anisotropic Tex" #TODO material properties equivalent?
    separateAnisotropic = "Separate Anisotropic" #TODO material properties equivalent?

class MSFS2024_DecalNodes(Enum):  
    decalBlendMaskTex = MSFS2024_MaterialProperties.decalBlendMaskTexture.name()
    decalBlendMaskThreshold = MSFS2024_MaterialProperties.decalblendMaskedThreshold.name()
    decalBlendMaskSharpness = MSFS2024_MaterialProperties.decalblendSharpness.name()
    decalFreezeFactor = MSFS2024_MaterialProperties.decalFreezeFactor.name()

class MSFS2024_PrincipledBSDFInputs(Enum):
    baseColor = "Base Color"
    subsurfaceColor = "Subsurface Color"
    metallic = "Metallic"
    roughness = "Roughness"
    anisotropic = "Anisotropic"
    anisotropicRotation = "Anisotropic Rotation"
    clearcoat = "Clearcoat"
    clearcoatRoughness = "Clearcoat Roughness"
    clearcoatNormal = "Clearcoat Normal"
    emission = "Emission"
    emissionStrength = "Emission Strength"
    alpha = "Alpha"
    normal = "Normal"

class MSFS2024_GroupTypes(Enum):
    nodeSocketFloat = "NodeSocketFloat"
    nodeSocketInt = "NodeSocketInt"
    nodeSocketColor = "NodeSocketColor"
    nodeSocketVector = "NodeSocketVector"
    nodeGroupInput = "NodeGroupInput"
    nodeGroupOutput = "NodeGroupOutput"

####################################################################
@staticmethod
def addNode(nodes, name = "", typeNode = "", location = (0.0, 0.0), hidden = True, width = 150.0, frame = None, color = (1.0, 1.0, 1.0), blend_type = "MIX", operation =  "ADD"):
    """ This method creates a new node in the shader node tree

    Args:
        nodes (list) : List of nodes of the shader node tree
        name (str) : Name of the node. Defaults to "".
        typeNode (str) : Type of the node we want to create, see : MSFS2024_ShaderNodeTypes. Defaults to "".
        location (tuple) : Position in (x, y) of the node in the shader tree. Defaults to (0.0, 0.0).
        hidden (bool) : Close the node or not in the shader node tree. Defaults to True.
        width (float) : Width of the node in the shader node tree. Defaults to 150.0.
        frame (node) : The frame Node of the new node. Defaults to None.
        color (tuple) : Color of the node in the shader node tree used only for frame nodes. Defaults to (1.0, 1.0, 1.0).
        blend_type (str) : Blend type of shader node Mix RGB node type, see : MSFS2024_ShaderNodeTypes.shaderNodeMixRGB. Defaults to "MIX".
        operation (str) : Operation of shader node math type or shader node vector math type, see : MSFS2024_ShaderNodeTypes.shaderNodeMath / MSFS2024_ShaderNodeTypes.shaderNodeVectorMath. Defaults to "ADD", Operation items can be found in enum MSFS2024_NodeMathOpe.

    Returns:
        bpy.types.Node : A new node in the shader node tree, returns 'None' if the creation fails
    """
    if nodes is not None:
        try:
            node = nodes.new(typeNode)
            if name != "":
                node.name = name
                node.label = name
            node.location = location
            node.hide = hidden
            node.width = width
            node.parent = frame
            if(typeNode == MSFS2024_ShaderNodeTypes.nodeFrame.value):
                node.use_custom_color = True
                node.color = color
            elif(typeNode == MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value or typeNode ==MSFS2024_ShaderNodeTypes.shaderNodeMix.value):
                node.blend_type = blend_type
            elif(typeNode == MSFS2024_ShaderNodeTypes.shaderNodeMath.value or typeNode == MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value):
                node.operation = operation
            return node
        except ValueError:
            print (f"[ValueError] Type : {typeNode} mismatch affectation.")
    return None

@staticmethod
def getNodeByName(nodes, nodeName):
    """ Return a node with a given name

    Args:
        nodes (list): List of nodes of the shader node tree
        nodeName (str): Name of the node

    Returns:
        bpy.types.Node : The node if exists, 'None' if not.
    """

    if nodes.find(nodeName) > -1:
        return nodes[nodeName]
    return None

@staticmethod
def getNodesByClassName(nodes, className):
    """ Return a node with a given className

    Args:
        nodes (list): List of nodes of the shader node tree
        className (str): Name of the class of the node

    Returns:
        bpy.types.Node : The node if exists, 'None' if not.
    """

    res = []
    for n in nodes:
        if n.__class__.__name__ == className:
            res.append(n)
    return res

@staticmethod
def getOrCreateGroupbyName(groupName):
    """
    This method create and return a new group if this one is not already created
    Args:
        groups (list(NodeTree)): List of existing Groups
        groupName (str): Name of the groupe

    Returns:
        tuple(bpy.types.NodeTree, Bool): The shader node group that has the given name and if it has been created or not 
    """
    groups = bpy.data.node_groups
    if groupName in groups:
        return (groups[groupName], False)
    else:
        groups.new(groupName, MSFS2024_ShaderNodeTypes.shaderNodeTree.value)
        return (groups[groupName], True)

@staticmethod  
def link(links, out_node, in_node):
    """ Links an output/input to an input/output

    Args:
        links (bpy.types.NodeLinks): List of the links of the shader node tree or the shader node group tree
        out_node (NodeSocket): Output/Input of a node
        in_node (NodeSocket): Input/Output of a node

    Returns:
        bpy.types.NodeLink : The new link created (could be helpful)
    """
    return links.new(out_node, in_node)

@staticmethod
def unLinkNodeInput(links, node, inputIndex):
    """ Unlink a node input with a given index

    Args:
        links (bpy.types.NodeLinks): List of the links of the shader node tree or the shader node group tree
        node (bpy.types.Node): A shader node
        inputIndex (int): Index of the input to unlink
    """
    for link in node.inputs[inputIndex].links:
        links.remove(link)

@staticmethod
def unLinkNodeOutput(links, node, outputIndex):
    """ Unlink a node output with a given index

    Args:
        links (bpy.types.NodeLinks): List of the links of the shader node tree or the shader node group tree
        node (bpy.types.Node): A shader node
        outputIndex (int): Index of the output to unlink
    """
    for link in node.outputs[outputIndex].links:
        links.remove(link)

@staticmethod
def setInputValue(input, value):
    input.default_value = value 

@staticmethod
def addGroupInput(group, inputName, inputType):
    """ Add an Input to a given group

    Args:
        group (bpy.types.NodeTree): The group
        inputName (str): The name of th input
        inputType (str): The type of the input socket see MSFS2024_GroupTypes

    Returns:
        bpy.types.NodeInputs: The Socket containing the input
    """
    return group.inputs.new(inputType, inputName)

@staticmethod
def addGroupOutput(group, outputName, outputType):
    """ Add an Output to a given group

    Args:
        group (bpy.types.NodeTree): The group
        outputName (str): The name of th output
        outputType (str): The type of the output socket see MSFS2024_GroupTypes

    Returns:
        bpy.types.NodeOutputs: The Socket containing the Output
    """
    return group.outputs.new(outputType, outputName)

