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


class AsoboFacialAnimation:
    bl_options = {"UNDO"}

    ExtensionName = "ASOBO_facial_animation"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def from_extension(gltf2_node, blender_object):
        if not gltf2_node:
            return

        if not gltf2_node.extensions:
            return

        extension = gltf2_node.extensions.get(AsoboFacialAnimation.ExtensionName)
        if not extension:
            return

        blender_object.msfs_facial_animation = True

    @staticmethod
    def export(gltf2_object, blender_object):
        extension = {}

        if type(blender_object) == bpy.types.PoseBone:
            blender_object = blender_object.bone

        if blender_object.msfs_facial_animation:
            extension["enabled"] = True
        
            gltf2_object.extensions[AsoboFacialAnimation.ExtensionName] = Extension(
                name=AsoboFacialAnimation.ExtensionName,
                extension=extension,
                required=False
            )