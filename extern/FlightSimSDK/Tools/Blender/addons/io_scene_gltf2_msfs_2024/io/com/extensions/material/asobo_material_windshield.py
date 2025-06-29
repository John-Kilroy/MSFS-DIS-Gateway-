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

from .....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties, MSFS2024_MaterialTypes


class AsoboMaterialWindshieldExtension:

    ExtensionName = "ASOBO_material_windshield_v3"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.windshieldDetailRoughness1,
        MSFS2024_MaterialProperties.windshieldDetailRoughness2,
        MSFS2024_MaterialProperties.windshieldDetailOpacity1,
        MSFS2024_MaterialProperties.windshieldDetailOpacity2,
        MSFS2024_MaterialProperties.windshieldMicroScratchTiling,
        MSFS2024_MaterialProperties.windshieldMicroScratchStrength,
        MSFS2024_MaterialProperties.windshieldDetailNormalRefractScale,
        MSFS2024_MaterialProperties.windshieldWiperLines,
        MSFS2024_MaterialProperties.windshieldWiperLinesStrength,
        MSFS2024_MaterialProperties.windshieldWiperLinesTiling,
        MSFS2024_MaterialProperties.windshieldWiper1State
    ]

    ExtensionTextures = [
        MSFS2024_MaterialProperties.windshieldWiperMaskTexture,
        (MSFS2024_MaterialProperties.windshiledDetailNormalTexture, "NORMAL"),
        (MSFS2024_MaterialProperties.windshieldScrachesNormaltexture , "NORMAL"),
        MSFS2024_MaterialProperties.windshieldInsectsAlbedoTexture,
        MSFS2024_MaterialProperties.windshieldInsectsMaskTexture
    ]

    bpy.types.Material.msfs_windshield_detail_rough_1 = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldDetailRoughness1.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldDetailRoughness1.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_detail_rough_2 = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldDetailRoughness2.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldDetailRoughness2.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_detail_opacity_1 = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldDetailOpacity1.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldDetailOpacity1.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_detail_opacity_2 = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldDetailOpacity2.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldDetailOpacity2.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_micro_scratches_tiling = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldMicroScratchTiling.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldMicroScratchTiling.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_micro_scratches_strength = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldMicroScratchStrength.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldMicroScratchStrength.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_detail_normal_refract_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldDetailNormalRefractScale.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldDetailNormalRefractScale.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_wiper_lines = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.windshieldWiperLines.name(),
        default = MSFS2024_MaterialProperties.windshieldWiperLines.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_wiper_lines_strength = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldWiperLinesStrength.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldWiperLinesStrength.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_wiper_lines_tiling = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldWiperLinesTiling.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldWiperLinesTiling.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_windshield_wiper_1_state = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.windshieldWiper1State.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.windshieldWiper1State.defaultValue(),
        options = set()
    )

    ## Textures
    bpy.types.Material.msfs_windshield_wiper_mask_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.windshieldWiperMaskTexture.name(),
        type = bpy.types.Image
    )

    bpy.types.Material.msfs_windshield_detail_normal_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.windshiledDetailNormalTexture.name(),
        type = bpy.types.Image
    )

    bpy.types.Material.msfs_windshield_scratches_normal_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.windshieldScrachesNormaltexture.name(),
        type = bpy.types.Image
    )

    bpy.types.Material.msfs_windshield_insects_albedo_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.windshieldInsectsAlbedoTexture.name(),
        type = bpy.types.Image
    )

    bpy.types.Material.msfs_windshield_insects_mask_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.windshieldInsectsMaskTexture.name(),
        type = bpy.types.Image
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialWindshieldExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.windshield.value)
        
        for extensionParameter in AsoboMaterialWindshieldExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )

        for extensionTexture in AsoboMaterialWindshieldExtension.ExtensionTextures:
            if type(extensionTexture) is tuple and len(extensionTexture) > 1:
                extensionTexture = extensionTexture[0]

            MSFS2024_MaterialExtension.getExtensionTexture(
                extension = extension,
                material = blender_material,
                attribute = extensionTexture,
                settings = import_settings
            )

        ## Get Windshield Detail Normal Scale
        normalDetailTextureExtension = extension.get(MSFS2024_MaterialProperties.windshiledDetailNormalTexture.extensionName())
        if normalDetailTextureExtension:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = normalDetailTextureExtension,
                material = blender_material,
                attribute = MSFS2024_MaterialProperties.detailNormalScale
            )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        if getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) != MSFS2024_MaterialTypes.windshield.value:
            return

        result = {}
        for extensionParameter in AsoboMaterialWindshieldExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter,
                withDefaultValue = True
            )

        for extensionTexture in AsoboMaterialWindshieldExtension.ExtensionTextures:
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
            gltf2_material.extensions[AsoboMaterialWindshieldExtension.ExtensionName] = Extension(
                name = AsoboMaterialWindshieldExtension.ExtensionName, extension = result, required = False
            )
