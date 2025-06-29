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



class AsoboTags:

    ExtensionName = "ASOBO_tags"

    class AsoboTag:
        Collision = "Collision"
        Road = "Road"

    bpy.types.Material.msfs_collision_material = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.collisionMaterial.name(),
        default = MSFS2024_MaterialProperties.collisionMaterial.defaultValue(),
        options = set()
    )

    bpy.types.Material.msfs_road_collision_material = bpy.props.BoolProperty(
        name = MSFS2024_MaterialProperties.roadCollisionMaterial.name(),
        default = MSFS2024_MaterialProperties.roadCollisionMaterial.defaultValue(),
        options = set()
    )

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboTags.ExtensionName)
        if extension is None:
            return

        if AsoboTags.AsoboTag.Collision in extension.get("tags"):
            blender_material.msfs_collision_material = True
            
        if AsoboTags.AsoboTag.Road in extension.get("tags"):
            blender_material.msfs_road_collision_material = True

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}

        tags = []

        if getattr(blender_material, MSFS2024_MaterialProperties.collisionMaterial.attributeName()):
            tags.append(AsoboTags.AsoboTag.Collision)
            
        if getattr(blender_material, MSFS2024_MaterialProperties.roadCollisionMaterial.attributeName()):
            tags.append(AsoboTags.AsoboTag.Road)

        if len(tags) > 0:
            result["tags"] = tags

            gltf2_material.extensions[AsoboTags.ExtensionName] = Extension(
                name = AsoboTags.ExtensionName, 
                extension = result, 
                required = False
            )

