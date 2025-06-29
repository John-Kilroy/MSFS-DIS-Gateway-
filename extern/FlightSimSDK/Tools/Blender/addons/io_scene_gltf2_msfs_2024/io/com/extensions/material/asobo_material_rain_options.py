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



class AsoboRainOptionsExtension:

    ExtensionName = "ASOBO_material_rain_options"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.rainDropTiling,
        MSFS2024_MaterialProperties.rainOnBackFace
    ]

    bpy.types.Material.msfs_receive_rain = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.receiveRain.name(),
        default = MSFS2024_MaterialProperties.receiveRain.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_rain_drop_tiling = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.rainDropTiling.name(),
        min = 0.0,
        max = 100.0,
        default = MSFS2024_MaterialProperties.rainDropTiling.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_rain_on_backface = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.rainOnBackFace.name(),
        min = 0.0,
        max = 100.0, ## TODO - Check this max
        default = MSFS2024_MaterialProperties.rainOnBackFace.defaultValue(),
        options = set(),
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboRainOptionsExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.receiveRain.attributeName(), True)

        for extensionParameter in AsoboRainOptionsExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension, 
                material = blender_material,
                attribute = extensionParameter
            )
    
    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        if not getattr(blender_material, MSFS2024_MaterialProperties.receiveRain.attributeName()):
            return

        result = {}

        if getattr(blender_material, MSFS2024_MaterialProperties.receiveRain.attributeName()):
            for extensionParameter in AsoboRainOptionsExtension.ExtensionParameters:
                MSFS2024_MaterialExtension.setExtensionParameter(
                    extension = result,
                    material = blender_material,
                    attribute = extensionParameter,
                    withDefaultValue = True
                )
        
        if result:
            gltf2_material.extensions[AsoboRainOptionsExtension.ExtensionName] = Extension(
                name = AsoboRainOptionsExtension.ExtensionName,
                extension = result,
                required = False,
            )
    