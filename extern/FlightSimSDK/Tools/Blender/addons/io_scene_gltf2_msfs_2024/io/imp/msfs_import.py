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

from ..com.extensions.object.asobo_facial_animation import AsoboFacialAnimation
from ..com.extensions.object.asobo_gizmo_object import AsoboGizmoObject
from ..com.extensions.object.asobo_softbody_mesh import AsoboSoftBodyMesh
from ..com.msfs_material_extensions import MSFS2024_MaterialExtension
from .. com.msfs_light_extensions import MSFS2024_LightExtension


class Import:

    def __init__(self):
        pass

    
    def gather_import_scene_before_hook(self, gltf_scene, blender_scene, import_settings):
        use_msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings.enable_msfs_extension
        if use_msfs_parameters:
            # Create gizmos
            AsoboGizmoObject.create(gltf_scene, blender_scene, import_settings)

    def gather_import_node_before_hook(self, vnode, gltf_node, gltf):
        use_msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings.enable_msfs_extension
        if use_msfs_parameters:
            MSFS2024_LightExtension.create(vnode, gltf_node)

    
    def gather_import_node_after_hook(self, vnode, gltf2_node, blender_object, import_settings):
        use_msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings.enable_msfs_extension
        if use_msfs_parameters:
            # Set proper gizmo blender object properties
            AsoboGizmoObject.from_extension(gltf2_node, blender_object)

            AsoboFacialAnimation.from_extension(gltf2_node, blender_object)
            AsoboSoftBodyMesh.from_extension(gltf2_node, blender_object)

            MSFS2024_LightExtension.removeLightObject(vnode, gltf2_node, blender_object)

    def gather_import_material_after_hook(self, gltf2_material, vertex_color, blender_material, import_settings):
        use_msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings.enable_msfs_extension
        if use_msfs_parameters:
            # Create materials
            MSFS2024_MaterialExtension.create(gltf2_material, blender_material, import_settings)

    def gather_import_animation_channel_after_hook(self, gltf_animation, gltf_node, path, channel, blender_action, gltf):
        use_msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings.enable_msfs_extension
        if use_msfs_parameters:
            AsoboFacialAnimation.from_extension(gltf_animation, blender_action)