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


class AsoboMaterialIridescentExtension:

    ExtensionName = "ASOBO_material_iridescent"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.iridescentMinThickness,
        MSFS2024_MaterialProperties.iridescentMaxThickness,
        MSFS2024_MaterialProperties.iridescentBrightness
    ]

    bpy.types.Material.msfs_use_iridescent = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.useIridescent.name(),
        default = MSFS2024_MaterialProperties.useIridescent.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_iridescent_min_thickness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.iridescentMinThickness.name(),
        min = 0.0,
        max = 2000.0,
        default = MSFS2024_MaterialProperties.iridescentMinThickness.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_iridescent_max_thickness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.iridescentMaxThickness.name(),
        min = 0.0,
        max = 2000.0,
        default = MSFS2024_MaterialProperties.iridescentMaxThickness.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_iridescent_brightness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.iridescentBrightness.name(),
        min = 0.0,
        max = 10.0,
        default = MSFS2024_MaterialProperties.iridescentBrightness.defaultValue(),
        options = set(),
    )

    ## Textures
    bpy.types.Material.msfs_iridescent_thickness_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.iridescentThicknessTexture.name(),
        type = bpy.types.Image,
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialIridescentExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.windshield.value)
        setattr(blender_material, MSFS2024_MaterialProperties.useIridescent.attributeName(), True)

        for extensionParameter in AsoboMaterialIridescentExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension, 
                material = blender_material, 
                attribute = extensionParameter
            )

        MSFS2024_MaterialExtension.getExtensionTexture(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.iridescentThicknessTexture,
            settings = import_settings
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        result = {}

        if getattr(blender_material, MSFS2024_MaterialProperties.useIridescent.attributeName()):
            for extensionParameter in AsoboMaterialIridescentExtension.ExtensionParameters:
                MSFS2024_MaterialExtension.setExtensionParameter(extension = result, material = blender_material, attribute = extensionParameter)
            
            MSFS2024_MaterialExtension.setExtensionTexture(
                extension = result,
                material = blender_material,
                attribute = MSFS2024_MaterialProperties.iridescentThicknessTexture,
                settings = export_settings
            )

            gltf2_material.extensions[AsoboMaterialIridescentExtension.ExtensionName] = Extension(
                name = AsoboMaterialIridescentExtension.ExtensionName, 
                extension = result, 
                required = False
            )