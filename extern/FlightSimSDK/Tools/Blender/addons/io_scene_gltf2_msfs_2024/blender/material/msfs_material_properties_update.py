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

from ..utils.msfs_material_utils import MSFS2024_MaterialProperties, MSFS2024_MaterialTypes

from .msfs_material import MSFS2024_Material
from .msfs_material_anisotropic import MSFS2024_Anisotropic
from .msfs_material_clearcoat import MSFS2024_Clearcoat
from .msfs_material_environment_occluder import MSFS2024_Environment_Occluder
from .msfs_material_fake_terrain import MSFS2024_Fake_Terrain
from .msfs_material_fresnel_fade import MSFS2024_Fresnel_Fade
from .msfs_material_geo_decal import MSFS2024_Geo_Decal
from .msfs_material_geo_decal_blendmasked import MSFS2024_Geo_Decal_BlendMasked
from .msfs_material_geo_decal_frosted import MSFS2024_Geo_Decal_Frosted
from .msfs_material_ghost import MSFS2024_Ghost
from .msfs_material_glass import MSFS2024_Glass
from .msfs_material_hair import MSFS2024_Hair
from .msfs_material_invisible import MSFS2024_Invisible
from .msfs_material_parallax import MSFS2024_Parallax
from .msfs_material_porthole import MSFS2024_Porthole
from .msfs_material_propeller import MSFS2024_Propeller
from .msfs_material_sail import MSFS2024_Sail
from .msfs_material_sss import MSFS2024_SSS
from .msfs_material_standard import MSFS2024_Standard
from .msfs_material_tree import MSFS2024_Tree
from .msfs_material_vegetation import MSFS2024_Vegetation
from .msfs_material_windshield import MSFS2024_Windshield


class MSFS2024_MaterialPropUpdate:
    @staticmethod
    def getMaterial(mat):
        match getattr(mat, MSFS2024_MaterialProperties.materialType.attributeName()):
            case MSFS2024_MaterialTypes.standard.value:
                return MSFS2024_Standard(mat)
            case MSFS2024_MaterialTypes.decal.value:
                return MSFS2024_Geo_Decal(mat)
            case MSFS2024_MaterialTypes.geoDecalFrosted.value:
                return MSFS2024_Geo_Decal_Frosted(mat)
            case MSFS2024_MaterialTypes.geoDecalBlendMasked.value:
                return MSFS2024_Geo_Decal_BlendMasked(mat)
            case MSFS2024_MaterialTypes.windshield.value:
                return MSFS2024_Windshield(mat)
            case MSFS2024_MaterialTypes.porthole.value:
                return MSFS2024_Porthole(mat)
            case MSFS2024_MaterialTypes.glass.value:
                return MSFS2024_Glass(mat)
            case MSFS2024_MaterialTypes.clearcoat.value:
                return MSFS2024_Clearcoat(mat)
            case MSFS2024_MaterialTypes.parallaxWindow.value:
                return MSFS2024_Parallax(mat)
            case MSFS2024_MaterialTypes.anisotripic.value:
                return MSFS2024_Anisotropic(mat)
            case MSFS2024_MaterialTypes.hair.value:
                return MSFS2024_Hair(mat)
            case MSFS2024_MaterialTypes.subSurfaceScattering.value:
                return MSFS2024_SSS(mat)
            case MSFS2024_MaterialTypes.invisible.value:
                return MSFS2024_Invisible(mat)
            case MSFS2024_MaterialTypes.fakeTerrain.value:
                return MSFS2024_Fake_Terrain(mat)
            case MSFS2024_MaterialTypes.fresnelFade.value:
                return MSFS2024_Fresnel_Fade(mat)
            case MSFS2024_MaterialTypes.environmentOccluder.value:
                return MSFS2024_Environment_Occluder(mat)
            case MSFS2024_MaterialTypes.ghost.value:
                return MSFS2024_Ghost(mat)
            case MSFS2024_MaterialTypes.sail.value:
                return MSFS2024_Sail(mat)
            case MSFS2024_MaterialTypes.propeller.value:
                return MSFS2024_Propeller(mat)
            case MSFS2024_MaterialTypes.tree.value:
                return MSFS2024_Tree(mat)
            case MSFS2024_MaterialTypes.vegetation.value:
                return MSFS2024_Vegetation(mat)
            case _:
                return None

    @staticmethod
    def update_msfs_material_type(self, context,rebuild_native_mat=True):
        match getattr(self, MSFS2024_MaterialProperties.materialType.attributeName()):
            case MSFS2024_MaterialTypes.standard.value:
                MSFS2024_Standard(self, buildTree = True)
            case MSFS2024_MaterialTypes.decal.value:
                MSFS2024_Geo_Decal(self, buildTree = True)
            case MSFS2024_MaterialTypes.geoDecalFrosted.value:
                MSFS2024_Geo_Decal_Frosted(self, buildTree = True)
            case MSFS2024_MaterialTypes.windshield.value:
                MSFS2024_Windshield(self, buildTree = True)
            case MSFS2024_MaterialTypes.porthole.value:
                MSFS2024_Porthole(self, buildTree = True)
            case MSFS2024_MaterialTypes.glass.value:
                MSFS2024_Glass(self, buildTree = True)
            case MSFS2024_MaterialTypes.clearcoat.value:
                MSFS2024_Clearcoat(self, buildTree = True)
            case MSFS2024_MaterialTypes.parallaxWindow.value:
                MSFS2024_Parallax(self, buildTree = True)
            case MSFS2024_MaterialTypes.anisotripic.value:
                MSFS2024_Anisotropic(self, buildTree = True)
            case MSFS2024_MaterialTypes.hair.value:
                MSFS2024_Hair(self, buildTree = True)
            case MSFS2024_MaterialTypes.subSurfaceScattering.value:
                MSFS2024_SSS(self, buildTree = True)
            case MSFS2024_MaterialTypes.invisible.value:
                MSFS2024_Invisible(self, buildTree = True)
            case MSFS2024_MaterialTypes.fakeTerrain.value:
                MSFS2024_Fake_Terrain(self, buildTree = True)
            case MSFS2024_MaterialTypes.fresnelFade.value:
                MSFS2024_Fresnel_Fade(self, buildTree = True)
            case MSFS2024_MaterialTypes.environmentOccluder.value:
                MSFS2024_Environment_Occluder(self, buildTree = True)
            case MSFS2024_MaterialTypes.ghost.value:
                MSFS2024_Ghost(self, buildTree = True)
            case MSFS2024_MaterialTypes.geoDecalBlendMasked.value:
                MSFS2024_Geo_Decal_BlendMasked(self, buildTree = True)
            case MSFS2024_MaterialTypes.sail.value:
                MSFS2024_Sail(self, buildTree = True)
            case MSFS2024_MaterialTypes.propeller.value:
                MSFS2024_Propeller(self, buildTree = True)
            case MSFS2024_MaterialTypes.tree.value:
                MSFS2024_Tree(self, buildTree = True)
            case MSFS2024_MaterialTypes.vegetation.value:
                MSFS2024_Vegetation(self, buildTree = True)
            case _:
                MSFS2024_Material(self, buildTree = False, revertToPBR=rebuild_native_mat)
                
    @staticmethod
    def update_base_color_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            if type(msfs) is not MSFS2024_Invisible:
                msfs.setBaseColorTex(getattr(self, MSFS2024_MaterialProperties.baseColorTexture.attributeName()))

    @staticmethod
    def update_comp_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            if type(msfs) is not MSFS2024_Invisible:
                msfs.setCompTex(getattr(self, MSFS2024_MaterialProperties.omrTexture.attributeName()))

    @staticmethod
    def update_normal_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            if type(msfs) is MSFS2024_Parallax:
                msfs.setNormalTex(getattr(self, MSFS2024_MaterialProperties.frontGlassNormalTexture.attributeName()))
            elif type(msfs) is not MSFS2024_Invisible:
                msfs.setNormalTex(getattr(self, MSFS2024_MaterialProperties.normalTexture.attributeName()))

    @staticmethod
    def update_emissive_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            if type(msfs) is MSFS2024_Parallax:
                msfs.setEmissiveTexture(getattr(self, MSFS2024_MaterialProperties.emissiveInsideWindowTexture.attributeName()))
            elif type(msfs) is not MSFS2024_Invisible:
                msfs.setEmissiveTexture(getattr(self, MSFS2024_MaterialProperties.emissiveTexture.attributeName()))

    @staticmethod
    def update_detail_color_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            if type(msfs) is MSFS2024_Parallax:
                msfs.setDetailColorTex(getattr(self, MSFS2024_MaterialProperties.behindGlassColorTexture.attributeName()))
            elif type(msfs) is not MSFS2024_Invisible:
                msfs.setDetailColorTex(getattr(self, MSFS2024_MaterialProperties.detailColorTexture.attributeName()))

    @staticmethod
    def update_detail_comp_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS2024_Invisible:
            msfs.setDetailCompTex(getattr(self, MSFS2024_MaterialProperties.detailOmrTexture.attributeName()))

    @staticmethod
    def update_occlusionUV2_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS2024_Invisible:
            msfs.setOcclusionUV2Tex(getattr(self, MSFS2024_MaterialProperties.occlusionUV2.attributeName()))

    @staticmethod
    def update_detail_normal_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS2024_Invisible:
            msfs.setDetailNormalTex(getattr(self, MSFS2024_MaterialProperties.detailNormalTexture.attributeName()))

    @staticmethod
    def update_blend_mask_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Standard:
            msfs.setBlendMaskTex(getattr(self, MSFS2024_MaterialProperties.blendMaskTexture.attributeName()))

    @staticmethod
    def update_decal_blend_mask_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Geo_Decal_BlendMasked:
            msfs.setDecalBlendMaskTex(getattr(self, MSFS2024_MaterialProperties.decalBlendMaskTexture.attributeName()))

    @staticmethod
    def update_blend_mask_threshold(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Standard:
            msfs.setBlendMaskThreshold(getattr(self, MSFS2024_MaterialProperties.detailBlendThreshold.attributeName()))
        if msfs is not None and type(msfs) is MSFS2024_Geo_Decal_BlendMasked:
            msfs.setBlendMaskThreshold(getattr(self, MSFS2024_MaterialProperties.decalblendMaskedThreshold.attributeName()))
    
    @staticmethod
    def update_freeze_factor(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Geo_Decal_Frosted:
            msfs.setFreezeFactor(getattr(self, MSFS2024_MaterialProperties.decalFreezeFactor.attributeName()))

    @staticmethod
    def update_blend_mask_sharpness(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Geo_Decal_BlendMasked:
            msfs.setBlendMaskSharpness(getattr(self, MSFS2024_MaterialProperties.decalblendSharpness.attributeName()))

    @staticmethod
    def update_alpha_mode(self, context):
        msfs_mat = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs_mat is not None:
            msfs_mat.setBlendMode(getattr(self, MSFS2024_MaterialProperties.alphaMode.attributeName()))

    @staticmethod
    def update_base_color(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setBaseColor(getattr(self, MSFS2024_MaterialProperties.baseColor.attributeName()))

    @staticmethod
    def get_base_color(self):
       return self.get(MSFS2024_MaterialProperties.baseColor.attributeName(), MSFS2024_MaterialProperties.baseColor.defaultValue())

    @staticmethod
    def set_base_color(self, value):
        msfs_mat = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs_mat is not None:
            msfs_mat.setBaseColor(value)

        self[MSFS2024_MaterialProperties.baseColor.attributeName()] = value

    @staticmethod
    def update_emissive_color(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setEmissiveColor(getattr(self, MSFS2024_MaterialProperties.emissiveColor.attributeName()))

    @staticmethod
    def get_emissive_color(self):
       return self.get(MSFS2024_MaterialProperties.emissiveColor.attributeName(), MSFS2024_MaterialProperties.emissiveColor.defaultValue())

    @staticmethod
    def set_emissive_color(self, value):
        msfs_mat = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs_mat is not None:
            msfs_mat.setEmissiveColor(value)

        self[MSFS2024_MaterialProperties.emissiveColor.attributeName()] = value

    @staticmethod
    def update_emissive_scale(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setEmissiveScale(getattr(self, MSFS2024_MaterialProperties.emissiveScale.attributeName()))

    @staticmethod
    def update_metallic_scale(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setMetallicScale(getattr(self, MSFS2024_MaterialProperties.metallicScale.attributeName()))

    @staticmethod
    def get_metallic_scale(self):
       return self.get(MSFS2024_MaterialProperties.metallicScale.attributeName(), MSFS2024_MaterialProperties.metallicScale.defaultValue())

    @staticmethod
    def set_metallic_scale(self, value):
        msfs_mat = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs_mat is not None:
            msfs_mat.setMetallicScale(value)

        self[MSFS2024_MaterialProperties.metallicScale.attributeName()] = value

    @staticmethod
    def update_roughness_scale(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setRoughnessScale(getattr(self, MSFS2024_MaterialProperties.roughnessScale.attributeName()))

    @staticmethod
    def get_roughness_scale(self):
       return self.get(MSFS2024_MaterialProperties.roughnessScale.attributeName(), MSFS2024_MaterialProperties.roughnessScale.defaultValue())

    @staticmethod
    def set_roughness_scale(self, value):
        msfs_mat = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs_mat is not None:
            msfs_mat.setRoughnessScale(value)

        self[MSFS2024_MaterialProperties.roughnessScale.attributeName()] = value

    @staticmethod
    def update_normal_scale(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setNormalScale(getattr(self, MSFS2024_MaterialProperties.normalScale.attributeName()))

    @staticmethod
    def update_color_sss(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_SSS:
            msfs.setSSSColor(getattr(self, MSFS2024_MaterialProperties.sssColor.attributeName()))

    @staticmethod
    def update_double_sided(self, context):
        doubleSidedValue = getattr(self, MSFS2024_MaterialProperties.doubleSided.attributeName())
        self.use_backface_culling = not doubleSidedValue
        setattr(self, MSFS2024_MaterialProperties.flipBackFaceNormal.attributeName(), doubleSidedValue)

    @staticmethod
    def update_alpha_cutoff(self, context):
        self.alpha_threshold = getattr(self, MSFS2024_MaterialProperties.alphaCutoff.attributeName())
        
    @staticmethod
    def update_detail_uv(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setDetailUVScale(getattr(self, MSFS2024_MaterialProperties.detailUVScale.attributeName()))
    
    @staticmethod
    def update_detail_normal_scale(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setDetailNormalScale(getattr(self, MSFS2024_MaterialProperties.detailNormalScale.attributeName()))

    @staticmethod
    def update_clearcoat_color_roughness_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Clearcoat:
            msfs.setClearcoatTexture(getattr(self, MSFS2024_MaterialProperties.clearcoatColorRoughnessTexture.attributeName()))

    @staticmethod
    def update_clearcoat_normal_texture(self, context):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS2024_Clearcoat:
            msfs.setClearcoatNormalTexture(getattr(self, MSFS2024_MaterialProperties.clearcoatNormalTexture.attributeName()))

    @staticmethod
    def get_uv_offset_u(self):
        return self.get(MSFS2024_MaterialProperties.uvOffsetU.attributeName(), MSFS2024_MaterialProperties.uvOffsetU.defaultValue())

    @staticmethod
    def set_uv_offset_u(self, value):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setUVOffsetU(value)

        self[MSFS2024_MaterialProperties.uvOffsetU.attributeName()] = value

    @staticmethod
    def get_uv_offset_v(self):
        return self.get(MSFS2024_MaterialProperties.uvOffsetV.attributeName(), MSFS2024_MaterialProperties.uvOffsetV.defaultValue())

    @staticmethod
    def set_uv_offset_v(self, value):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setUVOffsetV(value)

        self[MSFS2024_MaterialProperties.uvOffsetV.attributeName()] = value
    
    @staticmethod
    def get_uv_tiling_u(self):
        return self.get(MSFS2024_MaterialProperties.uvTilingU.attributeName(), MSFS2024_MaterialProperties.uvTilingU.defaultValue())

    @staticmethod
    def set_uv_tiling_u(self, value):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setUVTilingU(value)

        self[MSFS2024_MaterialProperties.uvTilingU.attributeName()] = value

    @staticmethod
    def get_uv_tiling_v(self):
        return self.get(MSFS2024_MaterialProperties.uvTilingV.attributeName(), MSFS2024_MaterialProperties.uvTilingV.defaultValue())

    @staticmethod
    def set_uv_tiling_v(self, value):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setUVTilingV(value)

        self[MSFS2024_MaterialProperties.uvTilingV.attributeName()] = value

    @staticmethod
    def get_uv_rotation(self):
        return self.get(MSFS2024_MaterialProperties.uvRotation.attributeName(), MSFS2024_MaterialProperties.uvRotation.defaultValue())

    @staticmethod
    def set_uv_rotation(self, value):
        msfs = MSFS2024_MaterialPropUpdate.getMaterial(self)
        if msfs is not None:
            msfs.setUVRotation(value)

        self[MSFS2024_MaterialProperties.uvRotation.attributeName()] = value
