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


class AsoboMaterialCommon:
    
    ## WARNING - Here the order of the items matters for retro-compatibility of scenes 
    bpy.types.Material.msfs_material_type = bpy.props.EnumProperty(
        name = "Type",
        items = (
            ("NONE", "Disabled", ""),
            ("msfs_standard", "Standard", ""),
            ("msfs_decal", "Decal", ""),
            ("msfs_geo_decal_frosted", "Geo Decal Frosted", ""),
            ("msfs_windshield", "Windshield", ""),
            ("msfs_porthole", "Porthole", ""),
            ("msfs_glass", "Glass", ""),
            ("msfs_clearcoat", "Clearcoat", ""),
            ("msfs_parallax_window", "Parallax Window", ""),
            ("msfs_anisotropic", "Anisotropic", ""),
            ("msfs_hair", "Hair", ""),
            ("msfs_sss", "Sub-surface Scattering", ""),
            ("msfs_invisible", "Invisible", ""),
            ("msfs_fake_terrain", "Fake Terrain", ""),
            ("msfs_fresnel_fade", "Fresnel Fade", ""),
            ("msfs_environment_occluder", "Environment Occluder", ""),
            ("msfs_ghost", "Ghost", ""),
            ("msfs_geo_decal_blendmasked", "Geo Decal BlendMasked", ""),
            ("msfs_sail", "Sail", ""),
            ("msfs_propeller", "Propeller", ""),
            ("msfs_tree", "Tree", ""),
            ("msfs_vegetation", "Vegetation", "")
        ),
        default = MSFS2024_MaterialProperties.materialType.defaultValue(),
        update = lambda self,context:MSFS2024_MaterialPropUpdate.update_msfs_material_type(self,context),#use lambda because update fonction only accept functions with two args
        options = set()  # ANIMATABLE is a default item in options, so for properties that shouldn't be animatable, we have to overwrite this.
    )

    bpy.types.Material.msfs_base_color_factor = bpy.props.FloatVectorProperty(
        name = MSFS2024_MaterialProperties.baseColor.name(),
        description = "The RGBA components of the base color of the material. The fourth component (A) is the alpha coverage of the material. The alphaMode property specifies how alpha is interpreted. These values are linear. If a baseColorTexture is specified, this value is multiplied with the texel values",
        subtype = "COLOR",
        min = 0.0,
        max = 1.0,
        size = 4,
        default = MSFS2024_MaterialProperties.baseColor.defaultValue(),
        # update = MSFS2024_MaterialPropUpdate.update_base_color,
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_base_color,
        get = MSFS2024_MaterialPropUpdate.get_base_color,
        precision = 3
    )

    bpy.types.Material.msfs_emissive_factor = bpy.props.FloatVectorProperty(
        name = MSFS2024_MaterialProperties.emissiveColor.name(),
        description = "The RGB components of the emissive color of the material. These values are linear. If an emissiveTexture is specified, this value is multiplied with the texel values",
        subtype = "COLOR",
        min = 0.0,
        max = 1.0,
        size = 3,
        default = MSFS2024_MaterialProperties.emissiveColor.defaultValue(),
        # update = MSFS2024_MaterialPropUpdate.update_emissive_color,
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_emissive_color,
        get = MSFS2024_MaterialPropUpdate.get_emissive_color,
        precision = 3
    )

    bpy.types.Material.msfs_metallic_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.metallicScale.name(),
        description = "The metalness of the material. A value of 1.0 means the material is a metal. A value of 0.0 means the material is a dielectric. Values in between are for blending between metals and dielectrics such as dirty metallic surfaces. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the metallic texel values",
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.metallicScale.defaultValue(),
        # update = MSFS2024_MaterialPropUpdate.update_metallic_scale,
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_metallic_scale,
        get = MSFS2024_MaterialPropUpdate.get_metallic_scale,
        precision = 3,
    )

    bpy.types.Material.msfs_roughness_factor = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.roughnessScale.name(),
        description = "The roughness of the material. A value of 1.0 means the material is completely rough. A value of 0.0 means the material is completely smooth. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the roughness texel values",
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.roughnessScale.defaultValue(),
        # update = MSFS2024_MaterialPropUpdate.update_roughness_scale,
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_roughness_scale,
        get = MSFS2024_MaterialPropUpdate.get_roughness_scale,
        precision = 3,
    )

    bpy.types.Material.msfs_normal_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.normalScale.name(),
        description = "The scalar multiplier applied to each normal vector of the texture. This value is ignored if normalTexture is not specified",
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.normalScale.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_normal_scale,
        options = set(),
        precision = 3,
    )

    bpy.types.Material.msfs_emissive_scale = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.emissiveScale.name(),
        description = "Controls the intensity of the emission. A value of 1.0 means that the material is fully emissive. This can be used in addition to an emissive texture and in this case, it will control the emission Strenght of this one.",
        min = 0.0,
        max = 200000.0,
        default = MSFS2024_MaterialProperties.emissiveScale.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_emissive_scale,
        options = set(),
        precision = 3,
    )

    bpy.types.Material.msfs_alpha_mode = bpy.props.EnumProperty(
        name = MSFS2024_MaterialProperties.alphaMode.name(),
        items = (
            (
                "OPAQUE",
                "Opaque",
                "The rendered output is fully opaque and any alpha value is ignored",
            ),
            (
                "MASK",
                "Mask",
                "The rendered output is either fully opaque or fully transparent depending on the alpha value and the specified alpha cutoff value. This mode is used to simulate geometry such as tree leaves or wire fences",
            ),
            (
                "BLEND",
                "Blend",
                "The rendered output is combined with the background using the normal painting operation (i.e. the Porter and Duff over operator). This mode is used to simulate geometry such as gauze cloth or animal fur",
            ),
            (
                "DITHER",
                "Dither",
                "The rendered output is blend with dithering dot pattern",
            ),
        ),
        default = MSFS2024_MaterialProperties.alphaMode.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_alpha_mode,
        options = set()
    )

    bpy.types.Material.msfs_alpha_cutoff = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.alphaCutoff.name(),
        description = "When alpha mode is set to MASK the alphaCutoff property specifies the cutoff threshold. If the alpha value is greater than or equal to the alphaCutoff value then it is rendered as fully opaque, otherwise, it is rendered as fully transparent. alphaCutoff value is ignored for other modes",
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.alphaCutoff.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_alpha_cutoff,
        options = set(),
        precision = 3,
    )

    bpy.types.Material.msfs_double_sided = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.doubleSided.name(),
        description = "The double sided property specifies whether the material is double sided. When this value is false, back-face culling is enabled. When this value is true, back-face culling is disabled and double sided lighting is enabled. The back-face must have its normals reversed before the lighting equation is evaluated",
        default = MSFS2024_MaterialProperties.doubleSided.defaultValue(),
        update = MSFS2024_MaterialPropUpdate.update_double_sided,
        options = set()
    )

    bpy.types.Material.msfs_base_color_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.baseColorTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_base_color_texture,
    )
    bpy.types.Material.msfs_occlusion_metallic_roughness_texture = bpy.props.PointerProperty(
            name = MSFS2024_MaterialProperties.omrTexture.name(),
            type = bpy.types.Image,
            update = MSFS2024_MaterialPropUpdate.update_comp_texture,
    )
    bpy.types.Material.msfs_normal_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.normalTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_normal_texture,
    )
    bpy.types.Material.msfs_emissive_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.emissiveTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_emissive_texture,
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        # Every flight sim asset has ASOBO_normal_map_convention, so we check if it's being used to set material. 
        # We set blender_material to standard. 
        # If the blender_material is another type, it will get changed later.
        if "ASOBO_normal_map_convention" in import_settings.data.extensions_used:

            setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.standard.value)
            
            if gltf2_material.pbr_metallic_roughness:

                if gltf2_material.pbr_metallic_roughness.base_color_factor is not None:
                    setattr(
                        blender_material, 
                        MSFS2024_MaterialProperties.baseColor.attributeName(), 
                        gltf2_material.pbr_metallic_roughness.base_color_factor
                    )
                
                if gltf2_material.pbr_metallic_roughness.metallic_factor is not None:
                    setattr(
                        blender_material, 
                        MSFS2024_MaterialProperties.metallicScale.attributeName(), 
                        gltf2_material.pbr_metallic_roughness.metallic_factor
                    )
                    
                if gltf2_material.pbr_metallic_roughness.roughness_factor is not None:
                    setattr(
                        blender_material, 
                        MSFS2024_MaterialProperties.roughnessScale.attributeName(), 
                        gltf2_material.pbr_metallic_roughness.roughness_factor
                    )

                if gltf2_material.pbr_metallic_roughness.base_color_texture is not None:
                    setattr(
                        blender_material,
                        MSFS2024_MaterialProperties.baseColorTexture.attributeName(), 
                        MSFS2024_MaterialExtension.create_image(gltf2_material.pbr_metallic_roughness.base_color_texture.index, import_settings)
                    )

                if gltf2_material.pbr_metallic_roughness.metallic_roughness_texture is not None:
                    setattr(
                        blender_material,
                        MSFS2024_MaterialProperties.omrTexture.attributeName(), 
                        MSFS2024_MaterialExtension.create_image(gltf2_material.pbr_metallic_roughness.metallic_roughness_texture.index, import_settings)
                    )

            if gltf2_material.emissive_factor is not None:
                setattr(
                    blender_material, 
                    MSFS2024_MaterialProperties.emissiveScale.attributeName(), 
                    gltf2_material.emissive_factor[0]
                )
                
            if gltf2_material.alpha_mode is not None:
                setattr(
                    blender_material, 
                    MSFS2024_MaterialProperties.alphaMode.attributeName(), 
                    gltf2_material.alpha_mode
                )
                
            if gltf2_material.alpha_cutoff is not None:
                setattr(
                    blender_material, 
                    MSFS2024_MaterialProperties.alphaCutoff.attributeName(), 
                    gltf2_material.alpha_cutoff
                )
                
            if gltf2_material.double_sided is not None:
                setattr(
                    blender_material, 
                    MSFS2024_MaterialProperties.doubleSided.attributeName(), 
                    gltf2_material.double_sided
                )

            if gltf2_material.normal_texture is not None:
                setattr(
                    blender_material, 
                    MSFS2024_MaterialProperties.normalTexture.attributeName(), 
                    MSFS2024_MaterialExtension.create_image(gltf2_material.normal_texture.index, import_settings)
                )

                if gltf2_material.normal_texture.scale is not None:
                    setattr(
                        blender_material, 
                        MSFS2024_MaterialProperties.normalScale.attributeName(), 
                        gltf2_material.normal_texture.scale
                    )
            
            if gltf2_material.emissive_texture is not None:
                setattr(
                    blender_material, 
                    MSFS2024_MaterialProperties.emissiveTexture.attributeName(), 
                    MSFS2024_MaterialExtension.create_image(gltf2_material.emissive_texture.index, import_settings)
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        ## PBR Textures are handled by Khronos Exporter 
        if gltf2_material.pbr_metallic_roughness:
            gltf2_material.pbr_metallic_roughness.base_color_factor = [f for f in getattr(blender_material, MSFS2024_MaterialProperties.baseColor.attributeName())] 
            gltf2_material.emissive_factor = [f * getattr(blender_material, MSFS2024_MaterialProperties.emissiveScale.attributeName()) for f in getattr(blender_material, MSFS2024_MaterialProperties.emissiveColor.attributeName())]
            gltf2_material.pbr_metallic_roughness.metallic_factor = getattr(blender_material, MSFS2024_MaterialProperties.metallicScale.attributeName())
            gltf2_material.pbr_metallic_roughness.roughness_factor = getattr(blender_material, MSFS2024_MaterialProperties.roughnessScale.attributeName())
        
        if gltf2_material.normal_texture:
            gltf2_material.normal_texture.scale = getattr(blender_material, MSFS2024_MaterialProperties.normalScale.attributeName())

        if "KHR_materials_emissive_strength" in gltf2_material.extensions:
            gltf2_material.extensions.pop("KHR_materials_emissive_strength")

        pass
