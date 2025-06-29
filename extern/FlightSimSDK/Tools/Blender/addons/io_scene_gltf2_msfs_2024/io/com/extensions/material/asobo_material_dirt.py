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


class AsoboMaterialDirtExtension:

    ExtensionName = "ASOBO_material_dirt"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.wearOverlayUVScale,
        MSFS2024_MaterialProperties.wearBlendSharpness,
        MSFS2024_MaterialProperties.wearAmount
    ]

    ExtensionTextures = [
        MSFS2024_MaterialProperties.wearAlbedoMaskTexture,
        MSFS2024_MaterialProperties.wearOmrIntensityTexture
    ]

    bpy.types.Material.msfs_wear_overlay_uv_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.wearOverlayUVScale.name(),
        description = "",
        min = 0.0,
        max = 10.0,
        default = MSFS2024_MaterialProperties.wearOverlayUVScale.defaultValue(),
        # update = 
        options = set(),
        precision = 3
    )

    bpy.types.Material.msfs_wear_blend_sharpness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.wearBlendSharpness.name(),
        description = "",
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.wearBlendSharpness.defaultValue(),
        # update = 
        options = set(),
        precision = 3
    )

    bpy.types.Material.msfs_wear_amount = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.wearAmount.name(),
        description = "",
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.wearAmount.defaultValue(),
        # update = 
        options = set(),
        precision = 3
    )

    ## Textures
    bpy.types.Material.msfs_wear_albedo_mask = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.wearAlbedoMaskTexture.name(), 
        type = bpy.types.Image
    )

    bpy.types.Material.msfs_wear_omr_intensity = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.wearOmrIntensityTexture.name(), 
        type = bpy.types.Image
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialDirtExtension.ExtensionName)
        if extension is None:
            return

        for extensionParameter in AsoboMaterialDirtExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )

        for extensionTexture in AsoboMaterialDirtExtension.ExtensionTextures:
            MSFS2024_MaterialExtension.getExtensionTexture(
                extension = extension,
                material = blender_material,
                attribute = extensionTexture,
                settings = import_settings
            )
        
    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        result = {}

        for extensionParameter in AsoboMaterialDirtExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter
            )

        for extensionTexture in AsoboMaterialDirtExtension.ExtensionTextures:
            MSFS2024_MaterialExtension.setExtensionTexture(
                extension = result,
                material = blender_material,
                attribute = extensionTexture,
                settings = export_settings
            )
        
        if result:
            gltf2_material.extensions[AsoboMaterialDirtExtension.ExtensionName] = Extension(
                name = AsoboMaterialDirtExtension.ExtensionName,
                extension = result,
                required = False,
            )

            