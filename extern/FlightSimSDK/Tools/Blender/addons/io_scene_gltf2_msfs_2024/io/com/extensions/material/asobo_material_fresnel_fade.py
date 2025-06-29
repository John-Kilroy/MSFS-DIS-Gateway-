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


class AsoboMaterialFresnelFadeExtension:

    ExtensionName = "ASOBO_material_fresnel_fade"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.fresnelFactor,
        MSFS2024_MaterialProperties.fresnelOpacityBias
    ]

    bpy.types.Material.msfs_fresnel_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.fresnelFactor.name(),
        min = 0.001,
        max = 100.0,
        default = MSFS2024_MaterialProperties.fresnelFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_fresnel_opacity_offset = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.fresnelOpacityBias.name(),
        min = -1.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.fresnelOpacityBias.defaultValue(),
        options = set()
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialFresnelFadeExtension.ExtensionName)
        if extension is None:
            return
        
        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.fresnelFade.value)

        for extensionParameter in AsoboMaterialFresnelFadeExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        if getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) != MSFS2024_MaterialTypes.fresnelFade.value:
            return

        result = {}
        
        for extensionParameter in AsoboMaterialFresnelFadeExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter,
                withDefaultValue = True
            )

        if result:
            gltf2_material.extensions[AsoboMaterialFresnelFadeExtension.ExtensionName] = Extension(
                name = AsoboMaterialFresnelFadeExtension.ExtensionName,
                extension = result,
                required = False,
            )
