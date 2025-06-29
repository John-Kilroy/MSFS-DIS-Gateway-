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
from .....blender.material.msfs_material_properties_update import \
    MSFS2024_MaterialPropUpdate

class AsoboExtraOcclusionExtension:

    ExtensionName = "ASOBO_extra_occlusion"

    ## Textures
    bpy.types.Material.msfs_occlusion_uv2 = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.occlusionUV2.name(), 
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_occlusionUV2_texture
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboExtraOcclusionExtension.ExtensionName)
        if extension is None:
            return

        MSFS2024_MaterialExtension.getExtensionTexture(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.occlusionUV2,
            settings = import_settings
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension
        result = {}

        MSFS2024_MaterialExtension.setExtensionTexture(
            extension = result,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.occlusionUV2,
            settings = export_settings,
            textureType = "DEFAULT"
        )

        if result:
            ## Something weard happens with the extra occlusion, the export set up the albedo and the occlusion texture
            ## We need to make sure to have only the occlusion uv2 to set the tex_coord to 1
            if result[MSFS2024_MaterialProperties.occlusionUV2.extensionName()].index.source.name == getattr(blender_material, MSFS2024_MaterialProperties.occlusionUV2.attributeName()).name :
                if hasattr(result[MSFS2024_MaterialProperties.occlusionUV2.extensionName()], "tex_coord"):
                    result[MSFS2024_MaterialProperties.occlusionUV2.extensionName()].tex_coord = 1
                
                gltf2_material.extensions[AsoboExtraOcclusionExtension.ExtensionName] = Extension(
                    name = AsoboExtraOcclusionExtension.ExtensionName, 
                    extension = result, 
                    required = False
                )
