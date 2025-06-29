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


from .msfs_bitmap_config import BitmapConfig
from .msfs_texture_config import TextureConfig

class GltfMaterial:
    def __init__(self, gltf_material) -> None:
        self.gltf_material = gltf_material
        self.extensions = gltf_material.get("extensions")
        self.pbr_metallic_roughness = self.gltf_material.get("pbrMetallicRoughness")

    def get_base_color_tex_config(self):
        if self.pbr_metallic_roughness is None:
            return None
        
        base_color_texture = self.pbr_metallic_roughness.get("baseColorTexture")
        if base_color_texture is None:
            return None

        # MTL_BITMAP_DECAL0
        bmp_config = BitmapConfig(1, "", False)
        texture_config = TextureConfig(base_color_texture.get("index"), bmp_config)
        return texture_config

    def get_metal_rough_ao_tex_config(self):
        if self.pbr_metallic_roughness is None:
            return None
        
        metallic_roughness_Texture = self.pbr_metallic_roughness.get("metallicRoughnessTexture")
        if metallic_roughness_Texture is None:
            return None

        # MTL_BITMAP_METAL_ROUGH_AO
        bmp_config = BitmapConfig(11, "", True)
        texture_config = TextureConfig(metallic_roughness_Texture.get("index"), bmp_config)
        return texture_config

    def get_occlusion_tex_config(self, metal_roughness_texture_index=-1):
        occlusion_texture = self.gltf_material.get("occlusionTexture")
        if occlusion_texture is None:
            return None

        if metal_roughness_texture_index == -1:
            return None

        occlusion_texture_index = occlusion_texture.get("index")
        if occlusion_texture_index == metal_roughness_texture_index:
            return None
        
        # MTL_BITMAP_OCCLUSION
        bmp_config = BitmapConfig(14, "", True)
        texture_config = TextureConfig(occlusion_texture_index, bmp_config)
        return texture_config

    def get_normal_tex_config(self):
        normal_texture = self.gltf_material.get("normalTexture")
        if normal_texture is None:
            return None

        # MTL_BITMAP_NORMAL
        bmp_config = BitmapConfig(3, "", False)
        texture_config = TextureConfig(normal_texture.get("index"), bmp_config)
        return texture_config

    def get_emissive_tex_config(self):
        emissive_texture = self.gltf_material.get("emissiveTexture")
        if emissive_texture is None:
            return None

        # MTL_BITMAP_EMISSIVE
        bmp_config = BitmapConfig(7, "", False)
        texture_config = TextureConfig(emissive_texture.get("index"), bmp_config)
        return texture_config

    def get_distance_field_layer_mask_tex_config(self):
        distance_field_layer = self.extensions.get("ASOBO_material_distance_field_layer")
        if distance_field_layer is None:
            return None

        distance_field_texture = distance_field_layer.get("distanceFieldLayerMaskTexture")
        if distance_field_texture is None:
            return None
        
        # MTL_BITMAP_BLENDMASK
        bmp_config = BitmapConfig(2, "FL_BITMAP_SDF", False)
        texture_config = TextureConfig(distance_field_texture.get("index"), bmp_config)
        return texture_config

    def get_distance_field_color_tex_config(self):
        distance_field_layer = self.extensions.get("ASOBO_material_distance_field_layer")
        if distance_field_layer is None:
            return None

        layer_texture = distance_field_layer.get("layerColorTexture")
        if layer_texture is None:
            return None
        
        # MTL_BITMAP_ADD_DECAL0
        bmp_config = BitmapConfig(5, "", False)
        texture_config = TextureConfig(layer_texture.get("index"), bmp_config)
        return texture_config

    def get_blend_mask_tex_config(self):
        detail_map = self.extensions.get("ASOBO_material_detail_map")
        if detail_map is None:
            return None
        
        blend_mask_texture = detail_map.get("blendMaskTexture")
        if blend_mask_texture is None:
            return None

        # MTL_BITMAP_BLENDMASK
        bmp_config = BitmapConfig(2, "", False)
        texture_config = TextureConfig(blend_mask_texture.get("index"), bmp_config)
        return texture_config

    def get_detail_color_tex_config(self, blend_mask_texture_index=-1):
        detail_map = self.extensions.get("ASOBO_material_detail_map")
        if detail_map is None:
            return None

        detail_color_texture = detail_map.get("detailColorTexture")
        if detail_color_texture is None:
            return None
        
        if blend_mask_texture_index == -1:
            # MTL_BITMAP_DETAILDIFFUSE
            bmp_config = BitmapConfig(8, "", False)
        else:
            # MTL_BITMAP_ADD_DECAL0
            bmp_config = BitmapConfig(5, "", False)

        texture_config = TextureConfig(detail_color_texture.get("index"), bmp_config)
        return texture_config

    def get_detail_normal_tex_config(self, blend_mask_texture_index=-1):
        detail_map = self.extensions.get("ASOBO_material_detail_map")
        if detail_map is None:
            return None

        detail_normal_texture = detail_map.get("detailNormalTexture")
        if detail_normal_texture is None:
            return None

        if blend_mask_texture_index == -1:
            # MTL_BITMAP_DETAILNORMAL
            bmp_config = BitmapConfig(6, "", False)
        else:
            # MTL_BITMAP_ADD_NORMAL
            bmp_config = BitmapConfig(9, "", False)

        texture_config = TextureConfig(detail_normal_texture.get("index"), bmp_config)
        return texture_config

    def get_detail_metal_rough_ao_tex_config(self, blend_mask_texture_index=-1):
        detail_map = self.extensions.get("ASOBO_material_detail_map")
        if detail_map is None:
            return None

        detail_metal_rough_ao_texture = detail_map.get("detailMetalRoughAOTexture")
        if detail_metal_rough_ao_texture is None:
            return None

        if blend_mask_texture_index == -1:
            # MTL_BITMAP_DETAIL_METAL_ROUGH_AO
            bmp_config = BitmapConfig(12, "", False)
        else:
            # MTL_BITMAP_ADD_METAL_ROUGH_AO
            bmp_config = BitmapConfig(13, "", False)

        texture_config = TextureConfig(detail_metal_rough_ao_texture.get("index"), bmp_config)
        return texture_config

    def get_aniso_direction_roughness_tex_config(self):
        anisotropic = self.extensions.get("ASOBO_material_anisotropic_v2")
        if anisotropic is None:
            return None
        
        aniso_direction_roughness_texture = anisotropic.get("anisoDirectionRoughnessTexture")
        if aniso_direction_roughness_texture is None:
            return None

        # MTL_BITMAP_ANISO_DIR_ROUGH
        bmp_config = BitmapConfig(17, "", True)
        texture_config = TextureConfig(aniso_direction_roughness_texture.get("index"), bmp_config)
        return texture_config

    def get_behind_window_text_config(self):
        parallax_window = self.extensions.get("ASOBO_material_parallax_window")
        if parallax_window is None:
            return None
        
        behind_window_texture = parallax_window.get("behindWindowMapTexture")
        if behind_window_texture is None:
            return None

        # MTL_BITMAP_ADD_DECAL0
        bmp_config = BitmapConfig(5, "", False)
        texture_config = TextureConfig(behind_window_texture.get("index"), bmp_config)
        return texture_config

    def get_wiper_mask_tex_config(self):
        windshield_v3 = self.extensions.get("ASOBO_material_windshield_v3")
        if windshield_v3 is None:
            return None
        
        wiper_mask_texture = windshield_v3.get("wiperMaskTexture")
        if wiper_mask_texture is None:
            return None
        
        # MTL_BITMAP_WIPERMASK
        bmp_config = BitmapConfig(18, "", False)
        texture_config = TextureConfig(wiper_mask_texture.get("index"), bmp_config)
        return texture_config

    def get_windshield_detail_normal_tex_config(self):
        windshield_v3 = self.extensions.get("ASOBO_material_windshield_v3")
        if windshield_v3 is None:
            return None
        
        windshield_detail_normal_texture = windshield_v3.get("windshieldDetailNormalTexture")
        if windshield_detail_normal_texture is None:
            return None
        
        # MTL_BITMAP_WINDSHIELDDETAILNORMAL
        bmp_config = BitmapConfig(19, "", False)
        texture_config = TextureConfig(windshield_detail_normal_texture.get("index"), bmp_config)
        return texture_config

    def get_scratches_normal_tex_config(self):
        windshield_v3 = self.extensions.get("ASOBO_material_windshield_v3")
        if windshield_v3 is None:
            return None
        
        scratches_normal_texture = windshield_v3.get("scratchesNormalTexture")
        if scratches_normal_texture is None:
            return None
        
        # MTL_BITMAP_SCRATCHESNORMAL
        bmp_config = BitmapConfig(20, "", False)
        texture_config = TextureConfig(scratches_normal_texture.get("index"), bmp_config)
        return texture_config

    def get_windshield_insects_tex_config(self):
        windshield_v3 = self.extensions.get("ASOBO_material_windshield_v3")
        if windshield_v3 is None:
            return None
        
        windshield_insects_texture = windshield_v3.get("windshieldInsectsTexture")
        if windshield_insects_texture is None:
            return None
        
        # MTL_BITMAP_WINDSHIELDINSECTS
        bmp_config = BitmapConfig(23, "", False)
        texture_config = TextureConfig(windshield_insects_texture.get("index"), bmp_config)
        return texture_config

    def get_windshield_insects_mask_tex_config(self):
        windshield_v3 = self.extensions.get("ASOBO_material_windshield_v3")
        if windshield_v3 is None:
            return None
        
        windshield_insects_mask_texture = windshield_v3.get("windshieldInsectsMaskTexture")
        if windshield_insects_mask_texture is None:
            return None
        
        # MTL_BITMAP_WINDSHIELDINSECTSMASK
        bmp_config = BitmapConfig(24, "", False)
        texture_config = TextureConfig(windshield_insects_mask_texture.get("index"), bmp_config)
        return texture_config

    def get_foliage_mask_tex_config(self):
        foliage = self.extensions.get("ASOBO_material_foliage_mask")
        if foliage is None:
            return None

        foliage_mask_texture = foliage.get("foliageMaskTexture")
        if foliage_mask_texture is None:
            return None

        # MTL_BITMAP_ALPHABLENDMASK
        bmp_config = BitmapConfig(21, "", False)
        texture_config = TextureConfig(foliage_mask_texture.get("index"), bmp_config)
        return texture_config

    def get_extra_occlusion_tex_config(self):
        extra_occlusion = self.extensions.get("ASOBO_extra_occlusion")
        if extra_occlusion is None:
            return None

        extra_occlusion_texture = extra_occlusion.get("extraOcclusionTexture")
        if extra_occlusion_texture is None:
            return None
        
        # MTL_BITMAP_OCCLUSION
        bmp_config = BitmapConfig(14, "", False)
        texture_config = TextureConfig(extra_occlusion_texture.get("index"), bmp_config)
        return texture_config

    def get_clearcoat_color_rough_tex_config(self):
        clear_coat2 = self.extensions.get("ASOBO_material_clear_coat_v2")
        if clear_coat2 is None:
            return None
        
        clearcoat_color_roughness_texture = clear_coat2.get("clearcoatColorRoughnessTexture")
        if clearcoat_color_roughness_texture is None:
            return None
        
        # MTL_BITMAP_CLEARCOATCOLORROUGHNESS
        bmp_config = BitmapConfig(15, "", False)
        texture_config = TextureConfig(clearcoat_color_roughness_texture.get("index"), bmp_config)
        return texture_config

    def get_clearcoat_normal_tex_config(self):
        clear_coat2 = self.extensions.get("ASOBO_material_clear_coat_v2")
        if clear_coat2 is None:
            return None
        
        clearcoat_normal_texture = clear_coat2.get("clearcoatNormalTexture")
        if clearcoat_normal_texture is None:
            return None
        
        # MTL_BITMAP_CLEARCOATNORMAL
        bmp_config = BitmapConfig(16, "", False)
        texture_config = TextureConfig(clearcoat_normal_texture.get("index"), bmp_config)
        return texture_config

    def get_dirt_mask_tex_config(self):
        geometry_decal = self.extensions.get("ASOBO_material_geometry_decal")
        if geometry_decal is None:
            return None

        dirt_mask_texture = geometry_decal.get("blendMaskTexture")
        if dirt_mask_texture is None:
            return None
        
        # MTL_BITMAP_BLENDMASK
        bmp_config = BitmapConfig(2, "", False)
        texture_config = TextureConfig(dirt_mask_texture.get("index"), bmp_config)
        return texture_config

    def get_iridescent_tex_config(self):
        iridescent = self.extensions.get("ASOBO_material_iridescent")
        if iridescent is None:
            return None

        iridescent_thickness_texture = iridescent.get("iridescentThicknessTexture")
        if iridescent_thickness_texture is None:
            return None
        
        # MTL_BITMAP_IRIDESCENTTHICKNESS
        bmp_config = BitmapConfig(22, "", False)
        texture_config = TextureConfig(iridescent_thickness_texture.get("index"), bmp_config)
        return texture_config

    def get_dirt_tex_config(self):
        dirt = self.extensions.get("ASOBO_material_dirt")
        if dirt is None:
            return None

        dirt_texture = dirt.get("dirtTexture")
        if dirt_texture is None:
            return None
        
        # MTL_BITMAP_DIRTOVERLAY
        bmp_config = BitmapConfig(28, "", False)
        texture_config = TextureConfig(dirt_texture.get("index"), bmp_config)
        return texture_config
        
    def get_dirt_occ_rough_metal_tex_config(self):
        dirt = self.extensions.get("ASOBO_material_dirt")
        if dirt is None:
            return None

        dirt_occ_rough_metal_texture = dirt.get("dirtOcclusionRoughnessMetallicTexture")
        if dirt_occ_rough_metal_texture is None:
            return None

        # MTL_BITMAP_DIRTOVERLAY_METAL_ROUGH_AO
        bmp_config = BitmapConfig(25, "", False)
        texture_config = TextureConfig(dirt_occ_rough_metal_texture.get("index"), bmp_config)
        return texture_config

    def get_tire_details_tex_config(self):
        tire = self.extensions.get("ASOBO_material_tire")
        if tire is None:
            return None

        tire_details_texture = tire.get("tireDetailsTexture")
        if tire_details_texture is None:
            return None

        # MTL_BITMAP_TIREDETAILS
        bmp_config = BitmapConfig(26, "", False)
        texture_config = TextureConfig(tire_details_texture.get("index"), bmp_config)
        return texture_config

    def get_tire_mud_normal_tex_config(self):
        tire = self.extensions.get("ASOBO_material_tire")
        if tire is None:
            return None

        tire_mud_normal_texture = tire.get("tireMudNormalTexture")
        if tire_mud_normal_texture is None:
            return None

        # MTL_BITMAP_TIREMUDNORMAL
        bmp_config = BitmapConfig(27, "", False)
        texture_config = TextureConfig(tire_mud_normal_texture.get("index"), bmp_config)
        return texture_config
        
