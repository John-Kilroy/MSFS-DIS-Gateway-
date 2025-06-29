
from ..utils.msfs_material_nodes_utils import *

class MSFS2024_NodesLibrary:
    """
    Common shader functions library
    """
    #region PRIVATE
    @staticmethod
    def _drawLinearStep(group):
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
        
        mathSubstractNode_1 = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (-200, 130)
        )

        mathSubstractNode_2 = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (-200, -80)
        )
        
        mathDivideNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.divide.value,
            location = (20, 60)
        )

        clampNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeClamp.value,
            location = (220, 75)
        )

        #region Inputs
        lowInput = addGroupInput(
            group = group, 
            inputName = "low",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        lowInput.default_value = 0.0
        
        highInput = addGroupInput(
            group = group, 
            inputName = "high",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        highInput.default_value = 1.0

        valueInput = addGroupInput(
            group = group, 
            inputName = "value",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        valueInput.default_value = 1.0
        #endregion

        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "Result",
            outputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        #endregion

        #region Links
        link(group.links, inputNode.outputs[0], mathSubstractNode_1.inputs[1])
        link(group.links, inputNode.outputs[2], mathSubstractNode_1.inputs[0])

        link(group.links, inputNode.outputs[0], mathSubstractNode_2.inputs[1])
        link(group.links, inputNode.outputs[1], mathSubstractNode_2.inputs[0])

        link(group.links, mathSubstractNode_1.outputs[0], mathDivideNode.inputs[0])
        link(group.links, mathSubstractNode_2.outputs[0], mathDivideNode.inputs[1])

        link(group.links, mathDivideNode.outputs[0], clampNode.inputs[0])

        link(group.links, clampNode.outputs[0], outputNode.inputs[0])
        #endregion
        return

    @staticmethod
    def _drawSwitch(group):
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
        
        compareMathNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation=MSFS2024_NodeMathOpe.compare.value,
            location = (225, 15)
        )
        compareMathNode.inputs[1].default_value = 1.0 #value
        compareMathNode.inputs[2].default_value = 0.0 #epsilon
        
        mixNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMixRGB.value,
            location = (575, -55)
        )

        #region Inputs
        switchInput = addGroupInput(
            group = group, 
            inputName = "switch",
            inputType = MSFS2024_GroupTypes.nodeSocketFloat.value
        )
        switchInput.default_value = 0.0
        
        falseInput = addGroupInput(
            group = group, 
            inputName = "false",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        falseInput.default_value = (1.0, 1.0, 1.0, 1.0)
        
        trueInput = addGroupInput(
            group = group, 
            inputName = "true",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        trueInput.default_value = (1.0, 1.0, 1.0, 1.0)
        #endregion

        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "output",
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion

        #region Links
        link(group.links, inputNode.outputs[0], compareMathNode.inputs[0])#switch
        link(group.links, inputNode.outputs[1], mixNode.inputs[1])#false
        link(group.links, inputNode.outputs[2], mixNode.inputs[2])#true
        
        link(group.links, compareMathNode.outputs[0], mixNode.inputs[0])#factor

        link(group.links, mixNode.outputs[0], outputNode.inputs[0])
        #endregion
        return

    @staticmethod
    def _drawSquareRootColor(group):
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
            location = (770.0, 0.0),
            hidden = False
        )
        
        separateColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeSeparateColor.value,
            location = (215, 66)
        )

        squareRootRedNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.sqrt.value,
            location = (410, 55)
        )
        squareRootBlueNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.sqrt.value,
            location = (410, 0)
        )
        squareRootGreenNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeMath.value,
            operation = MSFS2024_NodeMathOpe.sqrt.value,
            location = (410, -50)
        )

        combineColorNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeCombineColor.value,
            location = (585, 66)
        )

        #region Inputs
        colorInput = addGroupInput(
            group = group, 
            inputName = "color",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        colorInput.default_value = (1.0, 1.0, 1.0, 1.0)
        
        #endregion

        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "output",
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion

        #region Links
        link(group.links, inputNode.outputs[0], separateColorNode.inputs[0])
        link(group.links, separateColorNode.outputs[0], squareRootRedNode.inputs[0])
        link(group.links, separateColorNode.outputs[1], squareRootGreenNode.inputs[0])
        link(group.links, separateColorNode.outputs[2], squareRootBlueNode.inputs[0])
        
        
        link(group.links, squareRootRedNode.outputs[0], combineColorNode.inputs[0])
        link(group.links, squareRootGreenNode.outputs[0], combineColorNode.inputs[1])
        link(group.links, squareRootBlueNode.outputs[0], combineColorNode.inputs[2])

        link(group.links, combineColorNode.outputs[0], outputNode.inputs[0])
        #endregion
        return

    @staticmethod
    def _drawUnpackDetailORMNode(group):
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
            location = (770.0, 0.0),
            hidden = False
        )
        
        multiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (295, 0)
        )
        multiplyNode.inputs[1].default_value=(2,2,2)

        substractNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (505, 0)
        )
        
        substractNode.inputs[1].default_value=(1, 1, 1)

        #region Inputs
        colorInput = addGroupInput(
            group = group, 
            inputName = "detail ORM",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        colorInput.default_value = (1.0, 1.0, 1.0, 1.0)
        
        #endregion

        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "detail ORM",
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion

        #region Links
        link(group.links, inputNode.outputs[0], multiplyNode.inputs[0])
        link(group.links, multiplyNode.outputs[0], substractNode.inputs[0])
        link(group.links, substractNode.outputs[0], outputNode.inputs[0])
        #endregion
        return
    
    @staticmethod
    def _drawUnpackDetailORMNode(group):
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
            location = (770.0, 0.0),
            hidden = False
        )
        
        multiplyNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.multiply.value,
            location = (295, 0)
        )
        multiplyNode.inputs[1].default_value=(2, 2, 2)

        substractNode = addNode(
            nodes = group.nodes,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeVectorMath.value,
            operation = MSFS2024_NodeMathOpe.subtract.value,
            location = (505, 0)
        )
        
        substractNode.inputs[1].default_value=(1, 1, 1)

        #region Inputs
        colorInput = addGroupInput(
            group = group, 
            inputName = "detail ORM",
            inputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        colorInput.default_value = (1.0, 1.0, 1.0, 1.0)
        
        #endregion

        #region Outputs
        addGroupOutput(
            group = group,
            outputName = "detail ORM",
            outputType = MSFS2024_GroupTypes.nodeSocketColor.value
        )
        #endregion

        #region Links
        link(group.links, inputNode.outputs[0], multiplyNode.inputs[0])
        link(group.links, multiplyNode.outputs[0], substractNode.inputs[0])
        link(group.links, substractNode.outputs[0], outputNode.inputs[0])
        #endregion
        return
    
    #endregion

    #region PUBLIC
    @staticmethod
    def addLinearStepNode(node_tree, frame=None, location=(0, 0)):
        """ 
        LinearStep  :
            The function interpolates smoothly between two input values based on a third one.
            that should be between the first two. The returned value is clamped between 0 and 1.

        Args:
            node_tree : ShaderNodeTree or Group
            frame (node) : The frame Node of the new node. Defaults to None.
            location (tuple) : Position in (x, y) of the node in the shader tree. Defaults to (0.0, 0.0).

        Node Inputs:
            input_low 
            input_high 
            value 

        Shader Code:
            float linearstep(const float lo, const float hi, const float input)
            {
                return saturate((input - lo) / (hi - lo));
            }
        """

        linearStepGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.linearStepGroup.value
        )
        
        if newGroup:
            MSFS2024_NodesLibrary._drawLinearStep(group=linearStepGroup)
        
        linearStepGroupNode = addNode(
            nodes = node_tree.nodes,
            name = MSFS2024_GroupNodes.linearStepGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = location,
            width = 200.0,
            frame = frame,
            hidden = False
        )
        linearStepGroupNode.node_tree = linearStepGroup

        return linearStepGroupNode
    
    @staticmethod
    def addSwitchNode(node_tree, frame=None, location=(0, 0)):
        """
        Args:
            node_tree : ShaderNodeTree or Group
            frame (node) : The frame Node of the new node. Defaults to None.
            location (tuple) : Position in (x, y) of the node in the shader tree. Defaults to (0.0, 0.0).

        Node Inputs:
            switch 
            false 
            true 
        """

        switchGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.switchGroup.value
        )
        
        if newGroup:
            MSFS2024_NodesLibrary._drawSwitch(group=switchGroup)
        
        switchGroupNode = addNode(
            nodes = node_tree.nodes,
            name = MSFS2024_GroupNodes.switchGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = location,
            width = 200.0,
            frame = frame,
            hidden = False
        )
        switchGroupNode.node_tree = switchGroup

        return switchGroupNode
    
    @staticmethod
    def addSquareRootColorNode(node_tree, frame=None, location=(0, 0)):
        """
        Args:
            node_tree : ShaderNodeTree or Group
            frame (node) : The frame Node of the new node. Defaults to None.
            location (tuple) : Position in (x, y) of the node in the shader tree. Defaults to (0.0, 0.0).

        Node Inputs:
            color
        """
        squareRootColorGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.squareRootColorGroup.value
        )
        
        if newGroup:
            MSFS2024_NodesLibrary._drawSquareRootColor(group = squareRootColorGroup)
        
        squareRootColorGroupNode = addNode(
            nodes = node_tree.nodes,
            name = MSFS2024_GroupNodes.squareRootColorGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = location,
            width = 200.0,
            frame = frame,
            hidden = False
        )
        squareRootColorGroupNode.node_tree = squareRootColorGroup

        return squareRootColorGroupNode

    @staticmethod
    def addUnpackDetailORMNode(node_tree, frame=None, location=(0, 0)):
        """
        Args:
            node_tree : ShaderNodeTree or Group
            frame (node) : The frame Node of the new node. Defaults to None.
            location (tuple) : Position in (x, y) of the node in the shader tree. Defaults to (0.0, 0.0).

        Node Inputs:
            color
        """
        unpackORMGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.unpackDetailORMGroup.value
        )
        
        if newGroup:
            MSFS2024_NodesLibrary._drawUnpackDetailORMNode(group = unpackORMGroup)
        
        unpackORMGroupNode = addNode(
            nodes = node_tree.nodes,
            name = MSFS2024_GroupNodes.unpackDetailORMGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = location,
            width = 200.0,
            frame = frame,
            hidden = False
        )
        unpackORMGroupNode.node_tree = unpackORMGroup

        return unpackORMGroupNode
    
    @staticmethod
    def addUnpackDetailORMNode (node_tree, frame=None, location=(0, 0)):
        """
        Args:
            node_tree : ShaderNodeTree or Group
            frame (node) : The frame Node of the new node. Defaults to None.
            location (tuple) : Position in (x, y) of the node in the shader tree. Defaults to (0.0, 0.0).

        Node Inputs:
            color
        """
        unpackORMGroup, newGroup = getOrCreateGroupbyName(
            groupName = MSFS2024_GroupNodes.unpackDetailORMGroup.value
        )
        
        if newGroup:
            MSFS2024_NodesLibrary._drawUnpackDetailORMNode(group = unpackORMGroup)
        
        unpackORMGroupNode = addNode(
            nodes = node_tree.nodes,
            name = MSFS2024_GroupNodes.unpackDetailORMGroup.value,
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeGroup.value,
            location = location,
            width = 200.0,
            frame = frame,
            hidden = False
        )
        unpackORMGroupNode.node_tree = unpackORMGroup

        return unpackORMGroupNode

    #endregion