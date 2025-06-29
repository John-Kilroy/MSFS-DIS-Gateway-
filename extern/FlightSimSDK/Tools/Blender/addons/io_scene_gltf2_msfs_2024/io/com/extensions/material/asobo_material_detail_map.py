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
from .....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties


class AsoboMaterialDetailExtension:

    ExtensionName = "ASOBO_material_detail_map"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.detailUVScale,
        MSFS2024_MaterialProperties.detailBlendThreshold
    ]

    ExtensionTextures = [
        MSFS2024_MaterialProperties.detailColorTexture,
        MSFS2024_MaterialProperties.detailOmrTexture,
        (MSFS2024_MaterialProperties.detailNormalTexture, "NORMAL"),
        MSFS2024_MaterialProperties.blendMaskTexture
    ]

    ## Parameters
    bpy.types.Material.msfs_detail_uv_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.detailUVScale.name(),
        min = 0.01,
        max = 100.0,
        default = MSFS2024_MaterialProperties.detailUVScale.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_detail_uv,
        precision = 3,
        options = set()
    )

    bpy.types.Material.msfs_detail_blend_threshold = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.detailBlendThreshold.name(),
        min = 0.001,
        max = 1.0,
        default = MSFS2024_MaterialProperties.detailBlendThreshold.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_blend_mask_threshold,
        precision = 3,
        options = set()
    )

    bpy.types.Material.msfs_detail_normal_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.detailNormalScale.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.detailNormalScale.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_detail_normal_scale,
        precision = 3,
        options = set()
    )

    ## Textures
    bpy.types.Material.msfs_detail_color_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.detailColorTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_detail_color_texture
    )

    bpy.types.Material.msfs_detail_occlusion_metallic_roughness_texture = bpy.props.PointerProperty(
            name = MSFS2024_MaterialProperties.detailOmrTexture.name(),
            type = bpy.types.Image,
            update = MSFS2024_MaterialPropUpdate.update_detail_comp_texture
    )

    bpy.types.Material.msfs_detail_normal_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.detailNormalTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_detail_normal_texture
    )

    bpy.types.Material.msfs_blend_mask_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.blendMaskTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_blend_mask_texture
    )
    
    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialDetailExtension.ExtensionName)
        if extension is None:
            return

        for extensionParameter in AsoboMaterialDetailExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )
        
        for extensionTexture in AsoboMaterialDetailExtension.ExtensionTextures:
            if type(extensionTexture) is tuple and len(extensionTexture) > 1:
                extensionTexture = extensionTexture[0]

            MSFS2024_MaterialExtension.getExtensionTexture(
                extension = extension,
                material = blender_material,
                attribute = extensionTexture,
                settings = import_settings
            )

        ## get the scale from the normal texture information
        # "detailNormalTexture": {
        #     "scale": 0.4,
        #     "index": 3
        #   }
        normalTextureExtension = extension.get(MSFS2024_MaterialProperties.detailNormalTexture.extensionName())
        if normalTextureExtension:
            MSFS2024_MaterialExtension.getExtensionParameter(
                    extension = normalTextureExtension,
                    material = blender_material,
                    attribute = MSFS2024_MaterialProperties.detailNormalScale
                )        

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        result = {}

        ## We need to look at textures first, we don't need to expot the parameters if we don't have any detail texture set  
        for extensionTexture in AsoboMaterialDetailExtension.ExtensionTextures:
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

        if getattr(blender_material, MSFS2024_MaterialProperties.detailNormalTexture.attributeName()) is not None:
            result[MSFS2024_MaterialProperties.detailNormalTexture.extensionName()].scale = getattr(
                blender_material, 
                MSFS2024_MaterialProperties.detailNormalScale.attributeName()
            )
        
        
        ## We need to look at textures first, we don't need to expot the parameters if we don't have any detail texture set
        if not result:
            return
            
        for extensionParameter in AsoboMaterialDetailExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter
            )

        if not result:
            return

        gltf2_material.extensions[AsoboMaterialDetailExtension.ExtensionName] = Extension(
            name = AsoboMaterialDetailExtension.ExtensionName,
            extension = result,
            required = False,
        )
