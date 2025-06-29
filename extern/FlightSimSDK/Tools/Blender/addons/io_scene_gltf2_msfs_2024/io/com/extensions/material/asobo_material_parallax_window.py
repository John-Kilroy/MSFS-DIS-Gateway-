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
from .....blender.utils.msfs_material_utils import (MSFS2024_MaterialProperties,
                                                  MSFS2024_MaterialTypes)


class AsoboParallaxWindowExtension:

    ExtensionName = "ASOBO_material_parallax_window"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.parallaxRoomSizeX,
        MSFS2024_MaterialProperties.parallaxRoomSizeY,
        MSFS2024_MaterialProperties.parallaxRoomSizeZ,
        MSFS2024_MaterialProperties.parallaxRoomCount,
        MSFS2024_MaterialProperties.parallaxCorridor
    ]
    
    bpy.types.Material.msfs_parallax_room_size_x = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.parallaxRoomSizeX.name(),
        min = 0.01,
        max = 10.0,
        default = MSFS2024_MaterialProperties.parallaxRoomSizeX.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_parallax_room_size_y = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.parallaxRoomSizeY.name(),
        min = 0.01,
        max = 10.0,
        default = MSFS2024_MaterialProperties.parallaxRoomSizeY.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_parallax_room_size_z = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.parallaxRoomSizeZ.name(),
        min = 0.0,
        max = 1.0,
        default = MSFS2024_MaterialProperties.parallaxRoomSizeZ.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_parallax_room_count_xy = bpy.props.IntProperty(
        name = MSFS2024_MaterialProperties.parallaxRoomCount.name(),
        min = 1,
        max = 16,
        default = MSFS2024_MaterialProperties.parallaxRoomCount.defaultValue(),
        options = set(),
    )

    bpy.types.Material.msfs_parallax_corridor = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.parallaxCorridor.name(),
        default = MSFS2024_MaterialProperties.parallaxCorridor.defaultValue(),
        options = set(),
    )

    ## Textures
    bpy.types.Material.msfs_behind_glass_color_texture = bpy.props.PointerProperty(
        name = MSFS2024_MaterialProperties.behindGlassColorTexture.name(),
        type = bpy.types.Image,
        update = MSFS2024_MaterialPropUpdate.update_detail_color_texture
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboParallaxWindowExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.parallaxWindow.value)
        
        for extensionParameter in AsoboParallaxWindowExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension, 
                material = blender_material,
                attribute = extensionParameter
            )

        MSFS2024_MaterialExtension.getExtensionTexture(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.behindGlassColorTexture,
            settings = import_settings
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        if getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) != MSFS2024_MaterialTypes.parallaxWindow.value:
            return

        result = {}

        for extensionParameter in AsoboParallaxWindowExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter,
                withDefaultValue = True
            )

        MSFS2024_MaterialExtension.setExtensionTexture(result, blender_material, MSFS2024_MaterialProperties.behindGlassColorTexture, export_settings)

        gltf2_material.extensions[AsoboParallaxWindowExtension.ExtensionName] = Extension(
            name = AsoboParallaxWindowExtension.ExtensionName,
            extension = result,
            required = False,
        )

