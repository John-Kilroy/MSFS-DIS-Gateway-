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

from .....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties



class AsoboMaterialDrawOrderExtension:

    ExtensionName = "ASOBO_material_draw_order"

    bpy.types.Material.msfs_draw_order_offset = bpy.props.IntProperty(
        name = MSFS2024_MaterialProperties.drawOrderOffset.name(),
        description = "Draw Order Offset, to manually sort decals draw order for example",
        min = -999,
        max = 999,
        default = MSFS2024_MaterialProperties.drawOrderOffset.defaultValue(),
        options = set()
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialDrawOrderExtension.ExtensionName)
        if extension is None:
            return

        MSFS2024_MaterialExtension.getExtensionParameter(
            extension = extension,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.drawOrderOffset
        )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        from ....com.msfs_material_extensions import MSFS2024_MaterialExtension

        result = {}

        MSFS2024_MaterialExtension.setExtensionParameter(
            extension = result,
            material = blender_material,
            attribute = MSFS2024_MaterialProperties.drawOrderOffset
        )

        if result:
            gltf2_material.extensions[AsoboMaterialDrawOrderExtension.ExtensionName] = Extension(
                name = AsoboMaterialDrawOrderExtension.ExtensionName,
                extension = result,
                required = False,
            )

