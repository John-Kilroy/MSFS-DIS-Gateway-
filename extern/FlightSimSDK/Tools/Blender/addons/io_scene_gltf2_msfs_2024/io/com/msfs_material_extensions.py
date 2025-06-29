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
from ...blender.utils.msfs_material_nodes_utils import *

if bpy.app.version >= (3, 6, 0):
    from io_scene_gltf2.blender.exp.material.gltf2_blender_gather_texture_info import (
        gather_material_normal_texture_info_class, 
        gather_texture_info
        )
else:
    from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import (
        gather_material_normal_texture_info_class,
        gather_texture_info
    )

from io_scene_gltf2.blender.imp.gltf2_blender_image import BlenderImage

from .extensions.material.asobo_extra_occlusion import AsoboExtraOcclusionExtension
from .extensions.material.asobo_material_alphamode_dither import AsoboAlphaModeDither
from .extensions.material.asobo_material_anisotropic import AsoboAnisotropic
from .extensions.material.asobo_material_clear_coat import AsoboClearcoatExtension
from .extensions.material.asobo_material_code import AsoboMaterialCode
from .extensions.material.asobo_material_common import AsoboMaterialCommon
from .extensions.material.asobo_material_day_night_switch import AsoboDayNightCycleExtension
from .extensions.material.asobo_material_detail_map import AsoboMaterialDetailExtension
from .extensions.material.asobo_material_dirt import AsoboMaterialDirtExtension
from .extensions.material.asobo_material_disable_motion_blur import AsoboDisableMotionBlur
from .extensions.material.asobo_material_draw_order import AsoboMaterialDrawOrderExtension
from .extensions.material.asobo_material_environment_occluder import AsoboMaterialEnvironmentOccluderExtension
from .extensions.material.asobo_material_fake_terrain import AsoboMaterialFakeTerrainExtension
from .extensions.material.asobo_material_flip_back_face import AsoboFlipBackFaceExtension
from .extensions.material.asobo_material_foliage_mask import AsoboFoliageMaskExtension
from .extensions.material.asobo_material_fresnel_fade import AsoboMaterialFresnelFadeExtension
from .extensions.material.asobo_material_geometry_decal import AsoboMaterialGeometryDecalExtension
from .extensions.material.asobo_material_ghost_effect import AsoboMaterialGhostEffectExtension
from .extensions.material.asobo_material_glass import AsoboGlass
from .extensions.material.asobo_material_invisible import AsoboMaterialInvisible
from .extensions.material.asobo_material_iridescent import AsoboMaterialIridescentExtension
from .extensions.material.asobo_material_parallax_window import AsoboParallaxWindowExtension
from .extensions.material.asobo_material_pearlescent import AsoboPearlescentExtension
from .extensions.material.asobo_material_rain_options import AsoboRainOptionsExtension
from .extensions.material.asobo_material_sail import AsoboSailExtension
from .extensions.material.asobo_material_shadow_options import AsoboMaterialShadowOptionsExtension
from .extensions.material.asobo_material_sss import AsoboSSSExtension
from .extensions.material.asobo_material_uv_options import AsoboMaterialUVOptionsExtension
from .extensions.material.asobo_material_windshield import AsoboMaterialWindshieldExtension
from .extensions.material.asobo_occlusion_strength import AsoboOcclusionStrengthExtension
from .extensions.material.asobo_tags import AsoboTags


class MSFS2024_MaterialExtension:
    bl_options = {"UNDO"}

    extensions = [
        AsoboMaterialCommon,
        AsoboMaterialGeometryDecalExtension,
        AsoboMaterialGhostEffectExtension,
        AsoboMaterialDrawOrderExtension,
        AsoboDayNightCycleExtension,
        AsoboDisableMotionBlur,
        AsoboPearlescentExtension,
        AsoboAlphaModeDither,
        AsoboMaterialInvisible,
        AsoboMaterialEnvironmentOccluderExtension,
        AsoboMaterialUVOptionsExtension,
        AsoboMaterialShadowOptionsExtension,
        AsoboMaterialDetailExtension,
        AsoboMaterialFakeTerrainExtension,
        AsoboMaterialFresnelFadeExtension,
        AsoboSSSExtension,
        AsoboAnisotropic,
        AsoboMaterialWindshieldExtension,
        AsoboClearcoatExtension,
        AsoboParallaxWindowExtension,
        AsoboGlass,
        AsoboTags,
        AsoboMaterialCode,
        AsoboFlipBackFaceExtension,
        AsoboMaterialDirtExtension,
        AsoboExtraOcclusionExtension,
        AsoboOcclusionStrengthExtension,
        AsoboRainOptionsExtension,
        AsoboMaterialIridescentExtension,
        AsoboFoliageMaskExtension,
        AsoboSailExtension
    ]

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create_image(index, import_settings):
        pytexture = import_settings.data.textures[index]
        pyimg = import_settings.data.images[pytexture.source]
        
        if pyimg and pyimg.blender_image_name and pyimg.blender_image_name in bpy.data.images:
            return bpy.data.images[pyimg.blender_image_name]

        BlenderImage.create(import_settings, pytexture.source)
        return bpy.data.images[pyimg.blender_image_name]

    @staticmethod
    def export_image(blender_material, blender_image, type, export_settings, normal_scale=None):
        nodes = blender_material.node_tree.nodes
        links = blender_material.node_tree.links

        # Create a fake texture node temporarily (unfortunately this is the only solid way of doing this)
        textureNode = addNode(
            nodes = nodes,
            name = "Base Color Texture Output",
            typeNode = MSFS2024_ShaderNodeTypes.shaderNodeTexImage.value
        )
        textureNode.image = blender_image

        # Create shader to plug texture into
        principledBSDFNode = addNode(
                                nodes = nodes,
                                name = "Principled BSDF Temp Node",
                                typeNode = MSFS2024_ShaderNodeTypes.shadeNodeBsdfPrincipled.value
                            )
        tempLink = None
        
        # Gather texture info
        if type == "DEFAULT":
            tempLink = link(links, textureNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.baseColor.value])

            texture_info = gather_texture_info(
                principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.baseColor.value],
                (principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.baseColor.value],),
                export_settings
            )

        elif type == "NORMAL":
            normalNode = addNode(
                nodes = nodes,
                name = "Normal Texture Output",
                typeNode = MSFS2024_ShaderNodeTypes.shaderNodeNormalMap.value
            )

            if normal_scale:
                normalNode.inputs["Strength"].default_value = normal_scale

            tempLink = link(links, textureNode.outputs[0], normalNode.inputs["Color"])
            normal_blend_link = link(links, normalNode.outputs[0], principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.normal.value])

            texture_info = gather_material_normal_texture_info_class(
                principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.normal.value],
                (principledBSDFNode.inputs[MSFS2024_PrincipledBSDFInputs.normal.value],),
                export_settings
            )

            links.remove(normal_blend_link)

        # Delete temp nodes
        if tempLink:
            links.remove(tempLink)

        nodes.remove(textureNode)
        nodes.remove(principledBSDFNode)

        if type == "NORMAL":
            nodes.remove(normalNode)

        # Some versions of the Khronos exporter have gather_texture_info return a tuple
        if isinstance(texture_info, tuple):
            texture_info = texture_info[0]

        if hasattr(texture_info, "tex_coord"):
            texture_info.tex_coord = None
        
        return texture_info

    @staticmethod
    def getExtensionParameter(extension, material, attribute):
        if attribute.extensionName() and extension.get(attribute.extensionName()) is not None:
            setattr(
                material, 
                attribute.attributeName(), 
                extension.get(attribute.extensionName())
            )

    @staticmethod
    def getExtensionTexture(extension, material, attribute, settings):
        if attribute.extensionName() and extension.get(attribute.extensionName()) is not None:
            texture = MSFS2024_MaterialExtension.create_image(
                extension.get(attribute.extensionName(), {}).get("index"), 
                settings
            )

            setattr(
                material, 
                attribute.attributeName(),
                texture
            )

    @staticmethod
    def setExtensionParameter(extension, material, attribute, withDefaultValue = False):
        if attribute.extensionName() and (getattr(material, attribute.attributeName()) != attribute.defaultValue() or withDefaultValue):
            extension[attribute.extensionName()] = getattr(material, attribute.attributeName())

    @staticmethod
    def setExtensionTexture(extension, material, attribute, settings, textureType = "DEFAULT"):
        if attribute.extensionName() and getattr(material, attribute.attributeName()) != attribute.defaultValue():
            extension[attribute.extensionName()] = MSFS2024_MaterialExtension.export_image(
                material,
                getattr(material, attribute.attributeName()),
                textureType,
                settings
            )

    @staticmethod
    def create(gltf2_material, blender_material, import_settings):
        for extension in MSFS2024_MaterialExtension.extensions:
            extension.from_dict(blender_material, gltf2_material, import_settings)

    @staticmethod
    def export(gltf2_material, blender_material, export_settings):
        if gltf2_material.extensions is None:
            gltf2_material.extensions = {}
            
        for extension in MSFS2024_MaterialExtension.extensions:
            extension.to_extension(blender_material, gltf2_material, export_settings)
        
        
