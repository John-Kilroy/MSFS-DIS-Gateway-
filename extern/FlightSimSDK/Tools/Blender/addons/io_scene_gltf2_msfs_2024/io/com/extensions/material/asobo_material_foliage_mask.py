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


class AsoboFoliageMaskExtension:

    ExtensionName = "ASOBO_material_foliage_mask"

    ## Textures
    bpy.types.Material.msfs_foliage_mask_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.foliageMaskTexture.name(), 
        type = bpy.types.Image
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ...msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboFoliageMaskExtension.ExtensionName)
        if extension is None:
            return

        MSFS2024_MaterialExtension.getExtensionTexture(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.foliageMaskTexture,
            settings = import_settings
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ...msfs_material_extensions import MSFS2024_MaterialExtension
        result = {}

        MSFS2024_MaterialExtension.setExtensionTexture(
            extension = result,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.foliageMaskTexture,
            settings = export_settings,
            textureType = "DEFAULT"
        )

        if result:            
            gltf2_material.extensions[AsoboFoliageMaskExtension.ExtensionName] = Extension(
                name = AsoboFoliageMaskExtension.ExtensionName, 
                extension = result, 
                required = False
            )
