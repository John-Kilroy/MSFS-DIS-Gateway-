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


class MSFS2024ObjectProperties():
    bpy.types.Object.msfs_override_unique_id = bpy.props.BoolProperty(name='Override Unique ID', default=False)
    bpy.types.Object.msfs_unique_id = bpy.props.StringProperty(name='ID', default="")
    
    bpy.types.Object.msfs_collision_is_road_collider = bpy.props.BoolProperty(name="Road Collider", default=False)

class MSFS2024MeshProperties():
    bpy.types.Mesh.msfs_softbody = bpy.props.BoolProperty(name="Is SoftBody Mesh", default=False)

class MSFS2024BoneProperties():
    bpy.types.Bone.msfs_override_unique_id = bpy.props.BoolProperty(name='Override Unique ID',default=False)
    bpy.types.Bone.msfs_unique_id = bpy.props.StringProperty(name='ID',default="")

    bpy.types.Bone.msfs_facial_animation = bpy.props.BoolProperty(name='Enable Facial Animation',default=False)

class MSFS2024ActionProperties():
    bpy.types.Action.msfs_facial_animation = bpy.props.BoolProperty(name='Enable Facial Animation',default=False)
