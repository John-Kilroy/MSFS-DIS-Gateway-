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

import datetime
import time
import os
import bpy

from json import load

from ....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties

from .msfs_bitmap_config import BitmapConfig
from .msfs_texture_xml import XmlSerializer
from .msfs_gltf_material import GltfMaterial
from .msfs_texture_config import TextureConfig


def get_texture_config_from_bl_material(texture_name, materials):
    texture_configs = dict()
    for material in materials:
        texture_configs[material] = None

        if hasattr(material, MSFS2024_MaterialProperties.baseColorTexture.attributeName()):
            texture = getattr(material, MSFS2024_MaterialProperties.baseColorTexture.attributeName())

            if texture.name == texture_name:
                texture_configs[material] = TextureConfig(BitmapConfig(1, "", False))

        print(material)


def get_gltf_material_config(material):
    """
        Convert the material definition in a gltf to texture index and flags
    """
    gltf_material = GltfMaterial(material)
    result = list()

    #region Material Textures
    # MTL_BITMAP_DECAL0
    texture_config = gltf_material.get_base_color_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    # MTL_BITMAP_METAL_ROUGH_AO
    metal_rough_texture_index = -1
    metal_rough_texture_config = gltf_material.get_metal_rough_ao_tex_config()
    if metal_rough_texture_config is not None:
        metal_rough_texture_index = metal_rough_texture_config.gltf_texture_id
        result.append(metal_rough_texture_config)

    # MTL_BITMAP_OCCLUSION        
    texture_config = gltf_material.get_occlusion_tex_config(metal_rough_texture_index)
    if texture_config is not None:
        result.append(texture_config)

    # MTL_BITMAP_NORMAL
    texture_config = gltf_material.get_normal_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    # MTL_BITMAP_EMISSIVE
    texture_config = gltf_material.get_emissive_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    if gltf_material.extensions is None:
        return result

    #region Extensions Texture

    #region Distance Field Layer
    texture_config = gltf_material.get_distance_field_layer_mask_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_distance_field_color_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Detail Map
    blend_mask_texture_index = -1
    blend_mask_texture_config = gltf_material.get_blend_mask_tex_config()
    if blend_mask_texture_config is not None:
        blend_mask_texture_index = blend_mask_texture_config.gltf_texture_id
        result.append(blend_mask_texture_config)

    
    texture_config = gltf_material.get_detail_color_tex_config(blend_mask_texture_index)
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_detail_normal_tex_config(blend_mask_texture_index)
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_detail_metal_rough_ao_tex_config(blend_mask_texture_index)
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Anisotropic
    texture_config = gltf_material.get_aniso_direction_roughness_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Parallax Window
    texture_config = gltf_material.get_behind_window_text_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Windshield
    texture_config = gltf_material.get_wiper_mask_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_windshield_detail_normal_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_scratches_normal_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_windshield_insects_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_windshield_insects_mask_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Foliage
    texture_config = gltf_material.get_foliage_mask_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Extra Occlusion
    texture_config = gltf_material.get_extra_occlusion_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Clearcoat
    texture_config = gltf_material.get_clearcoat_color_rough_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_clearcoat_normal_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Geometry Decal
    texture_config = gltf_material.get_dirt_mask_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Iridescent
    texture_config = gltf_material.get_iridescent_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Dirt
    texture_config = gltf_material.get_dirt_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_dirt_occ_rough_metal_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #region Tire
    texture_config = gltf_material.get_tire_details_tex_config()
    if texture_config is not None:
        result.append(texture_config)

    texture_config = gltf_material.get_tire_mud_normal_tex_config()
    if texture_config is not None:
        result.append(texture_config)
    #endregion

    #endregion
    return result

def get_texture_flags(texture_name):
    flags = ""
    if texture_name in bpy.data.images:
        blender_image = bpy.data.images[texture_name]
        flags = blender_image.msfs_flags.to_string()
    return flags

def get_gltf_texture_configs(gltf_path):
    """
        Return a dict of the texture with bitmap config associated from a gltf
        In : gltf_path -> str
        Out: dict[str, Tuple(BitmapConfig, image_path)]
    """
    texture_configs_result = dict()

    if not os.path.exists(gltf_path):
        return texture_configs_result

    json_file = None
    with open(gltf_path, 'r') as file:
        json_file = load(file)

    if json_file is None:
        return texture_configs_result
    
    gltf_materials = json_file.get("materials")
    gltf_textures = json_file.get("textures")
    gltf_images = json_file.get("images")

    if (gltf_materials is None) or (gltf_textures is None) or (gltf_images is None):
        print(f"[TEXTURELIB][GLTF][WARNING] No textures found in {gltf_path}.")
        return texture_configs_result

    for gltf_material in gltf_materials:
        texture_configs = get_gltf_material_config(gltf_material)

        for texture_config in texture_configs:
            gltf_texture_id = gltf_textures[texture_config.gltf_texture_id].get("source")

            image_path = gltf_images[gltf_texture_id].get("uri")
            image_path = str.replace(image_path, '/', '\\')
            image_path = os.path.join(os.path.dirname(gltf_path), image_path)
            image_name = os.path.basename(image_path)

            texture_config.bitmap_config.user_flags += get_texture_flags(image_name)

            if image_name not in texture_configs_result:
                texture_configs_result[image_name] = (texture_config.bitmap_config, image_path)
            
            else:
                saved_bmp_texture_config = texture_configs_result[image_name][0] # BitmapConfig
                has_same_configs = texture_config.bitmap_config.compare(saved_bmp_texture_config)
                has_compatible_configs = texture_config.bitmap_config.is_compatible_id(saved_bmp_texture_config)

                if not has_same_configs and not has_compatible_configs:
                    print(f"[TEXTURELIB][WARNING][{image_name}] Same image name for different config: \n \
                            - {texture_config.bitmap_config.__str__()} \n\
                            - {saved_bmp_texture_config.__str__()}"
                    )
                
    if len(gltf_images) > len(texture_configs_result):
        print(f"[GLTF][WARNING] Some images used in the gltf {gltf_path} aren't referenced by any material")
        
    return texture_configs_result

def get_gltfs_texture_configs(gltf_paths, keep_originals=True, texture_dst_dir=''):
    """
        Out: dict[name of texture: str, tuple(BitmapConfig, texture_folder_path)]
    """
    result = dict()
    for gltf_path in gltf_paths:
        try:
            texture_configs = get_gltf_texture_configs(gltf_path)       
        except:
            print(f"[TEXTURELIB][GLTF][ERROR] Something went wrong, failed parsing the gltf {gltf_path}.")
            continue

        gltf_dir_path = os.path.dirname(gltf_path)
        if not os.path.isabs(texture_dst_dir):
            texture_dst_dir = os.path.join(gltf_dir_path, texture_dst_dir)

        if not keep_originals and texture_dst_dir != '':
            for texture_name, texture_config in texture_configs.items():
                new_texture_path = os.path.join(texture_dst_dir, texture_name)
                new_texture_config = (texture_config[0], new_texture_path)
                texture_config = new_texture_config
        
        result.update(texture_configs)     
    return result

def create_xml(texture_config):
    """
        Write a new xml with the textureConfig at the xmlPath location
        Return True when succesfully created
        In:
            texture_config : Tuple(BitmapConfig, path: str)
    """
    texture_path = texture_config[1]
    if not os.path.exists(texture_path):
        print(f"[TEXTURELIB][ERROR] Path: {texture_path} does not exists.")
        return

    xml_path = texture_path + ".xml"
    xml_name = os.path.basename(xml_path)
    serializer = XmlSerializer(xml_path)

    texture_bmp_config = texture_config[0]
    if os.path.exists(xml_path):
        if serializer.open():
            if serializer.bmp_config.compare(texture_bmp_config):
                print(f"[TEXTURELIB][{xml_name}] Done (skip).")
                return
        else:
            os.remove(xml_path)

    if serializer.bmp_config.is_compatible_id(texture_bmp_config):
        serializer.bmp_config.combine(texture_bmp_config)
        print(f"[TEXTURELIB][{xml_name}] Done (overwriting compatible).")
    else:
        serializer.bmp_config = texture_bmp_config.copy()
        print(f"[TEXTURELIB][{xml_name}] Done (created).")

    if not serializer.save():
        print(f"[TEXTURELIB][ERROR][{xml_name}] Failed (writing went wrong).")
    return

def export_texturelib_with_gltf(gltf_paths, keep_originals=True, texture_dst_dir=''):
    """
        Use a list of gltf paths to parse them and create the xml textures 
        needed next to all textures found in the devmod project
    """
    if len(gltf_paths) < 1:
        return
    
    print(f"[TEXTURELIB] New TextureLib generation started at {str(datetime.datetime.now())}")
    time_start = time.time()

    texture_configs = get_gltfs_texture_configs(gltf_paths, keep_originals, texture_dst_dir)

    for texture_name, texture_config in texture_configs.items():
        if ' ' in texture_name:
            print(f"[TEXTURELIB][ERROR] Failed : Texture name '{texture_name}' contains whitespace(s), \
                    so the XML will not be generated for it. Please remove them before regenerating."
            )
            continue

        print(f"[TEXTURELIB] Generating XML for texture {texture_name}:")
        create_xml(texture_config)
    
    delta = round(time.time() - time_start, 3)
    print(f"[TEXTURELIB] Operation completed in {delta}")
