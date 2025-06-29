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

from .....blender.material.msfs_material_properties_update import MSFS2024_MaterialPropUpdate
from .....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties



class AsoboMaterialUVOptionsExtension:

    ExtensionName = "ASOBO_material_UV_options"

    ExtensionParameters = [
        MSFS2024_MaterialProperties.clampUVX,
        MSFS2024_MaterialProperties.clampUVY,
        MSFS2024_MaterialProperties.uvOffsetU,
        MSFS2024_MaterialProperties.uvOffsetV,
        MSFS2024_MaterialProperties.uvTilingU,
        MSFS2024_MaterialProperties.uvTilingV,
        MSFS2024_MaterialProperties.uvRotation
    ]

    bpy.types.Material.msfs_clamp_uv_x = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.clampUVX.name(),
        default = MSFS2024_MaterialProperties.clampUVX.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_clamp_uv_y = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.clampUVY.name(),
        default = MSFS2024_MaterialProperties.clampUVY.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_uv_offset_u = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.uvOffsetU.name(),
        min = -10.0,
        max = 10.0,
        default = MSFS2024_MaterialProperties.uvOffsetU.defaultValue(),
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_uv_offset_u,
        get = MSFS2024_MaterialPropUpdate.get_uv_offset_u,
        precision = 3
    )

    bpy.types.Material.msfs_uv_offset_v = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.uvOffsetV.name(),
        min = -10.0,
        max = 10.0,
        default = MSFS2024_MaterialProperties.uvOffsetV.defaultValue(),
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_uv_offset_v,
        get = MSFS2024_MaterialPropUpdate.get_uv_offset_v,
        precision = 3
    )

    bpy.types.Material.msfs_uv_tiling_u = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.uvTilingU.name(),
        min = -10.0,
        max = 10.0,
        default = MSFS2024_MaterialProperties.uvTilingU.defaultValue(),
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_uv_tiling_u,
        get = MSFS2024_MaterialPropUpdate.get_uv_tiling_u,
        precision = 3
    )

    bpy.types.Material.msfs_uv_tiling_v = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.uvTilingV.name(),
        min = -10.0,
        max = 10.0,
        default = MSFS2024_MaterialProperties.uvTilingV.defaultValue(),
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_uv_tiling_v,
        get = MSFS2024_MaterialPropUpdate.get_uv_tiling_v,
        precision = 3
    )

    bpy.types.Material.msfs_uv_rotation = bpy.props.FloatProperty(
        name = MSFS2024_MaterialProperties.uvRotation.name(),
        min = -360.0,
        max = 360.0,
        default = MSFS2024_MaterialProperties.uvRotation.defaultValue(),
        options = {"ANIMATABLE"},
        set = MSFS2024_MaterialPropUpdate.set_uv_rotation,
        get = MSFS2024_MaterialPropUpdate.get_uv_rotation,
        precision = 3
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialUVOptionsExtension.ExtensionName)
        
        if extension is None:
            return

        for extensionParameter in AsoboMaterialUVOptionsExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.getExtensionParameter(
                extension = extension,
                material = blender_material,
                attribute = extensionParameter
            )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        result = {}
        
        for extensionParameter in AsoboMaterialUVOptionsExtension.ExtensionParameters:
            MSFS2024_MaterialExtension.setExtensionParameter(
                extension = result,
                material = blender_material,
                attribute = extensionParameter
            )

        if result:
            gltf2_material.extensions[AsoboMaterialUVOptionsExtension.ExtensionName] = Extension(
                name = AsoboMaterialUVOptionsExtension.ExtensionName,
                extension = result,
                required = False,
            )

