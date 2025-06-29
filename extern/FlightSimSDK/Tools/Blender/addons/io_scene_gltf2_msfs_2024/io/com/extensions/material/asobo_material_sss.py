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

from .....blender.material.msfs_material_properties_update import \
    MSFS2024_MaterialPropUpdate
from .....blender.utils.msfs_material_utils import (
    MSFS2024_MaterialProperties, MSFS2024_MaterialTypes)


class AsoboSSSExtension:

    ExtensionName = "ASOBO_material_SSS"

    ## Parameters
    bpy.types.Material.msfs_sss_color = bpy.props.FloatVectorProperty(
        name = MSFS2024_MaterialProperties.sssColor.name(),
        description = "The RGBA components of the SSS color of the material. These values are linear. If a SSSTexture is specified, this value is multiplied with the texel values",
        subtype = "COLOR",
        min = 0.0,
        max = 1.0,
        size = 4,
        default = MSFS2024_MaterialProperties.sssColor.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_color_sss,
        options = set()
    )

    ## Textures
    bpy.types.Material.msfs_opacity_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.opacityTexture.name(), 
        type = bpy.types.Image
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboSSSExtension.ExtensionName)

        if extension is None:
            return

        ## Set Material Type To SSS
        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.subSurfaceScattering.value)

        MSFS2024_MaterialExtension.getExtensionParameter(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.sssColor
        )
        
        MSFS2024_MaterialExtension.getExtensionTexture(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.opacityTexture,
            settings = import_settings
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension
        result = {}

        if (
            getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) == MSFS2024_MaterialTypes.subSurfaceScattering.value 
            or getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) == MSFS2024_MaterialTypes.hair.value
        ):
            result[MSFS2024_MaterialProperties.sssColor.extensionName()] = list(getattr(blender_material, MSFS2024_MaterialProperties.sssColor.attributeName()))

            MSFS2024_MaterialExtension.setExtensionTexture(
                extension = result,
                material = blender_material,
                attribute = MSFS2024_MaterialProperties.opacityTexture,
                settings = export_settings
            )
            
            gltf2_material.extensions[AsoboSSSExtension.ExtensionName] = Extension(
                name = AsoboSSSExtension.ExtensionName, 
                extension = result, 
                required = False
            )

