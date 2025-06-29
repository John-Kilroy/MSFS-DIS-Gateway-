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


class AsoboClearcoatExtension:

    ExtensionName = "ASOBO_material_clear_coat_v2"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.clearcoatRoughnessFactor,
        MSFS2024_MaterialProperties.clearcoatNormalFactor,
        MSFS2024_MaterialProperties.clearcoatColorRoughnessTiling,
        MSFS2024_MaterialProperties.clearcoatNormalTiling,
        MSFS2024_MaterialProperties.clearcoatInverseRoughness,
        MSFS2024_MaterialProperties.clearcoatBaseRoughness,

    ]

    ExtensionTextures = [
        MSFS2024_MaterialProperties.clearcoatColorRoughnessTexture,
        (MSFS2024_MaterialProperties.clearcoatNormalTexture, "NORMAL")
    ]

    bpy.types.Material.msfs_clearcoat_roughness_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.clearcoatRoughnessFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.clearcoatRoughnessFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_clearcoat_normal_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.clearcoatNormalFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.clearcoatNormalFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_clearcoat_color_roughness_tiling = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.clearcoatColorRoughnessTiling.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.clearcoatColorRoughnessTiling.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_clearcoat_normal_tiling = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.clearcoatNormalTiling.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.clearcoatNormalTiling.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_clearcoat_inverse_roughness = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.clearcoatInverseRoughness.name(),
        default = MSFS2024_MaterialProperties.clearcoatInverseRoughness.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_clearcoat_base_roughness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.clearcoatBaseRoughness.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.clearcoatBaseRoughness.defaultValue(),
        options = set()
    )

    ## Textures
    bpy.types.Material.msfs_clearcoat_color_roughness_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.clearcoatColorRoughnessTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_clearcoat_color_roughness_texture
    )

    bpy.types.Material.msfs_clearcoat_normal_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.clearcoatNormalTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_clearcoat_normal_texture
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboClearcoatExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.clearcoat.value)
        
        for extensionParameter in AsoboClearcoatExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )

        for extensionTexture in AsoboClearcoatExtension.ExtensionTextures:
            if type(extensionTexture) is tuple and len(extensionTexture) > 1:
                extensionTexture = extensionTexture[0]

            MSFS2024_MaterialExtension.getExtensionTexture(
                extension = extension,
                material = blender_material,
                attribute = extensionTexture,
                settings = import_settings
            )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        if getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) != MSFS2024_MaterialTypes.clearcoat.value:
            return
            
        result = {}
        ## We need to at textures first, we don't need to expot the parameters if we don't have any detail texture set  
        for extensionTexture in AsoboClearcoatExtension.ExtensionTextures:
            textureType = "DEFAULT"
            
            if type(extensionTexture) is tuple and len(extensionTexture) > 1:
                textureType = extensionTexture[1]
                extensionTexture = extensionTexture[0]

            MSFS2024_MaterialExtension.setExtensionTexture(
                extension = result,
                material = blender_material,
                attribute = extensionTexture,
                settings = export_settings,
                textureType = textureType
            )

        if result:
            for extensionParameter in AsoboClearcoatExtension.ExtensionParameters:
                MSFS2024_MaterialExtension.setExtensionParameter(
                    extension = result,
                    material = blender_material,
                    attribute = extensionParameter,
                    withDefaultValue = True
                )
        else:
            result = {'dummy': None}

        gltf2_material.extensions[AsoboClearcoatExtension.ExtensionName] = Extension(
            name = AsoboClearcoatExtension.ExtensionName, 
            extension = result, 
            required = False
        )

