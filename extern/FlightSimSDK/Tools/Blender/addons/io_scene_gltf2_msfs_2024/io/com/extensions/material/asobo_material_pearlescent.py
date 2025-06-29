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

from .....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties



class AsoboPearlescentExtension:

    ExtensionName = "ASOBO_material_pearlescent"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.pearlColorShift,
        MSFS2024_MaterialProperties.pearlColorRange,
        MSFS2024_MaterialProperties.pearlColorRange
    ]

    bpy.types.Material.msfs_use_pearl = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.usePearlEffect.name(),
        default = MSFS2024_MaterialProperties.usePearlEffect.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_pearl_shift = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.pearlColorShift.name(),
        min = -999.0,
        max = 999.0,
        default = MSFS2024_MaterialProperties.pearlColorShift.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_pearl_range = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.pearlColorRange.name(),
        min = -999.0,
        max = 999.0,
        default = MSFS2024_MaterialProperties.pearlColorRange.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_pearl_brightness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.pearlColorBrightness.name(),
        min = -1.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.pearlColorBrightness.defaultValue(),
        options = set()
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboPearlescentExtension.ExtensionName)
        if extension is None:
            return
        
        setattr(blender_material, MSFS2024_MaterialProperties.usePearlEffect.attributeName(), True)

        for extensionParameter in AsoboPearlescentExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(extension, blender_material, extensionParameter)

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension
        
        if not getattr(blender_material, MSFS2024_MaterialProperties.usePearlEffect.attributeName()):
            return

        result = {}
        for extensionParameter in AsoboPearlescentExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter,
                withDefaultValue = True
            )

        if result:
            gltf2_material.extensions[AsoboPearlescentExtension.ExtensionName] = Extension(
                name = AsoboPearlescentExtension.ExtensionName, 
                extension = result, 
                required = False
            )
