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

from .....blender.utils.msfs_material_utils import (
    MSFS2024_MaterialProperties, MSFS2024_MaterialTypes)


class AsoboSailExtension:

    ExtensionName = "ASOBO_material_sail"

    ## Parameters
    bpy.types.Material.msfs_sail_light_absorption = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.sailLightAbsorption.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.sailLightAbsorption.defaultValue(),
        options = set()
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboSailExtension.ExtensionName)

        if extension is None:
            return

        ## Set Material Type To Sail
        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.sail.value)

        MSFS2024_MaterialExtension.getExtensionParameter(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.sailLightAbsorption
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension
        result = {}

        MSFS2024_MaterialExtension.setExtensionParameter(
            extension = result,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.sailLightAbsorption
        )
        
        if result:
            gltf2_material.extensions[AsoboSailExtension.ExtensionName] = Extension(
                name = AsoboSailExtension.ExtensionName, 
                extension = result, 
                required = False
            )

