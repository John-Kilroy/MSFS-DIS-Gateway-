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


class MSFS2024_Invisible(MSFS2024_Material):

    attributes = [
        MSFS2024_MaterialProperties.baseColor,
        MSFS2024_MaterialProperties.emissiveColor,
        MSFS2024_MaterialProperties.disableMotionBlur,

        MSFS2024_MaterialProperties.uvOffsetU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvTilingU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvRotation,
        MSFS2024_MaterialProperties.clampUVX,
        MSFS2024_MaterialProperties.clampUVY,

        MSFS2024_MaterialProperties.collisionMaterial,
        MSFS2024_MaterialProperties.roadCollisionMaterial
    ]
    
    def __init__(self, material, buildTree = False):
        super().__init__(material, buildTree = buildTree)
        if buildTree:
            self.setDefaultProperties()
            self.forceUpdateNodes()

    def customShaderTree(self):
        super(MSFS2024_Invisible, self).defaultShadersTree()
        baseColorANode = getNodeByName(self.nodes, MSFS2024_ShaderNodes.baseColorA.value)
        baseColorANode.outputs[0].default_value = 0.0

    def setDefaultProperties(self):
        super().setDefaultProperties(self.attributes)
        setattr(self.material, MSFS2024_MaterialProperties.alphaMode.attributeName(), "BLEND")
        setattr(self.material, MSFS2024_MaterialProperties.noCastShadow.attributeName(), True)

    def forceUpdateNodes(self):
        super().forceUpdateNodes()

    @staticmethod
    def drawPanel(layout, material):
        MSFS2024_Invisible.drawParametersPanel(layout, material)

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

        #### Render parameters ####
        box = layout.box()
        box.label(text="Render Parameters")

        ## Motion Blur
        MSFS2024_MaterialUtilsUI.drawMotionBlurProp(
            layout = box,
            material = material,
            text = MSFS2024_MaterialProperties.disableMotionBlur.name()
        )
        #### End Render parameters ####

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
        return
