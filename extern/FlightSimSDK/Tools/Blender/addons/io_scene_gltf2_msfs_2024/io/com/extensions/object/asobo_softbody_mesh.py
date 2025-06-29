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

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class AsoboSoftBodyMesh:
    bl_options = {"UNDO"}

    ExtensionName = "ASOBO_softbody_mesh"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def from_extension(gltf2_node, blender_object):
        if not gltf2_node:
            return

        if not gltf2_node.extensions:
            return

        extension = gltf2_node.extensions.get(AsoboSoftBodyMesh.ExtensionName)
        if not extension:
            return

        if blender_object.type == "MESH":
            blender_object.data.msfs_softbody = True

    @staticmethod
    def export(gltf2_object, blender_object):
        if blender_object.type != "MESH":
            return
        
        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}
        
        extension = {}

        if blender_object.data.msfs_softbody:
            extension["type"] = "balloon"
        
        if extension:
            gltf2_object.mesh.extensions[AsoboSoftBodyMesh.ExtensionName] = Extension(
                name=AsoboSoftBodyMesh.ExtensionName,
                extension=extension,
                required=False
            )