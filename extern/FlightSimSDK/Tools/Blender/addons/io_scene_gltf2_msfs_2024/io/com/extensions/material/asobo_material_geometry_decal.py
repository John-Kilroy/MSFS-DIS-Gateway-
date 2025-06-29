
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
from .....blender.material.msfs_material_properties_update import MSFS2024_MaterialPropUpdate

class AsoboMaterialGeometryDecalExtension:

    ExtensionName = "ASOBO_material_geometry_decal"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.baseColorBlendFactor,
        MSFS2024_MaterialProperties.metallicBlendFactor,
        MSFS2024_MaterialProperties.roughnessBlendFactor,
        MSFS2024_MaterialProperties.normalBlendFactor,
        MSFS2024_MaterialProperties.emissiveBlendFactor,
        MSFS2024_MaterialProperties.occlusionBlendFactor,
        MSFS2024_MaterialProperties.normalOverrideFactor,
        MSFS2024_MaterialProperties.decalblendSharpness,
        MSFS2024_MaterialProperties.underClearCoat
    ]

    bpy.types.Material.msfs_base_color_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.baseColorBlendFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.baseColorBlendFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_metallic_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.metallicBlendFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.metallicBlendFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_roughness_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.roughnessBlendFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.roughnessBlendFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_normal_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.normalBlendFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.normalBlendFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_emissive_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.emissiveBlendFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.emissiveBlendFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_occlusion_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.occlusionBlendFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.occlusionBlendFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_normal_override_blend_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.normalOverrideFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.normalOverrideFactor.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_decal_blend_sharpness = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.decalblendSharpness.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.decalblendSharpness.defaultValue(),
        options = set(),
        update = MSFS2024_MaterialPropUpdate.update_blend_mask_sharpness
    )

    bpy.types.Material.msfs_under_clearcoat = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.underClearCoat.name(),
        default = MSFS2024_MaterialProperties.underClearCoat.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_decal_mode = bpy.props.StringProperty(
        name = MSFS2024_MaterialProperties.decalMode.name(),
        default = MSFS2024_MaterialProperties.decalMode.defaultValue(),
        options = set()
    )

    ## Textures
    bpy.types.Material.msfs_decal_blend_mask_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.decalBlendMaskTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_decal_blend_mask_texture
    )

    # Debug Shader
    bpy.types.Material.msfs_decal_freeze_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.decalFreezeFactor.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.decalFreezeFactor.defaultValue(),
        options = set(),
        update = MSFS2024_MaterialPropUpdate.update_freeze_factor
    )

    bpy.types.Material.msfs_decal_blend_masked_threshold = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.decalblendMaskedThreshold.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.decalblendMaskedThreshold.defaultValue(),
        options = set(),
        update = MSFS2024_MaterialPropUpdate.update_blend_mask_threshold
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialGeometryDecalExtension.ExtensionName)
        if extension is None:
            return

        decalMode = extension.get(MSFS2024_MaterialProperties.decalMode.extensionName())
        if decalMode == "default":
            setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.decal.value)
        elif decalMode == "frosted":
            setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.geoDecalFrosted.value)
        elif decalMode == "blendMasked":
            setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.geoDecalBlendMasked.value)

        for extensionParameter in AsoboMaterialGeometryDecalExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )
        
        MSFS2024_MaterialExtension.getExtensionTexture(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.decalBlendMaskTexture,
            settings = import_settings
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        result = {}

        for extensionParameter in AsoboMaterialGeometryDecalExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter
            )

        MSFS2024_MaterialExtension.setExtensionTexture(
                extension = result,
                material = blender_material,
                attribute = MSFS2024_MaterialProperties.decalBlendMaskTexture,
                settings = export_settings,
                textureType = "DEFAULT"
            )
                
        if result:
            ## Set Decal Mode
            result[MSFS2024_MaterialProperties.decalMode.extensionName()] = getattr(blender_material, MSFS2024_MaterialProperties.decalMode.attributeName())

            gltf2_material.extensions[AsoboMaterialGeometryDecalExtension.ExtensionName] = Extension(
                name = AsoboMaterialGeometryDecalExtension.ExtensionName,
                extension = result,
                required = False,
            )

