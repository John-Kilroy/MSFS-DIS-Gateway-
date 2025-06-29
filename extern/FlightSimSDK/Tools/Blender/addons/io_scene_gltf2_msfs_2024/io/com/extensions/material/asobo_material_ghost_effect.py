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
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

from .....blender.utils.msfs_material_utils import (MSFS2024_MaterialProperties,
                                                  MSFS2024_MaterialTypes)


class AsoboMaterialGhostEffectExtension:

    ExtensionName = "ASOBO_material_ghost_effect"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.ghostBias,
        MSFS2024_MaterialProperties.ghostScale,
        MSFS2024_MaterialProperties.ghostPower
    ]

    bpy.types.Material.msfs_ghost_bias = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.ghostBias.name(),
        min = 0.001,
        max = 64.0,
        default = MSFS2024_MaterialProperties.ghostBias.defaultValue(),
        options = set()
    )
    
    bpy.types.Material.msfs_ghost_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.ghostScale.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.ghostScale.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_ghost_power = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.ghostPower.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.ghostPower.defaultValue(),
        options = set()
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialGhostEffectExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.ghost.value)
        
        for extensionParameter in AsoboMaterialGhostEffectExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        if getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) != MSFS2024_MaterialTypes.ghost.value:
            return

        result = {}

        for extensionParameter in AsoboMaterialGhostEffectExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter,
                withDefaultValue = True
            )

        if result:
            gltf2_material.extensions[AsoboMaterialGhostEffectExtension.ExtensionName] = Extension(
                name = AsoboMaterialGhostEffectExtension.ExtensionName,
                extension = result,
                required = False,
            )
