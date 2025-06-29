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

from ... import get_version_string
from ..com.extensions.object.asobo_facial_animation import AsoboFacialAnimation
from ..com.extensions.object.asobo_gizmo_object import AsoboGizmoObject
from ..com.extensions.object.asobo_softbody_mesh import AsoboSoftBodyMesh
from ..com.extensions.object.asobo_unique_id import AsoboUniqueId
from ..com.extensions.asobo_property_animation import AsoboPropertyAnimation
from ..com.msfs_material_extensions import MSFS2024_MaterialExtension
from ..com.msfs_light_extensions import MSFS2024_LightExtension
from ..com.msfs_nodes_utils import MSFS2024_NodeUtils
from ..com.msfs_mesh_utils import  MSFS2024_MeshUtils

def get_blender_version_string():
    return str(bpy.data.version[0]) + '.' + str(bpy.data.version[1]) + '.' + str(bpy.data.version[2])

class Export:

    def gather_asset_hook(self, gltf2_asset, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return

        if gltf2_asset.extensions is None:
            gltf2_asset.extensions = {}
            
        gltf2_asset.extensions["ASOBO_normal_map_convention"] = self.Extension(
            name="ASOBO_normal_map_convention",
            extension={"tangent_space_convention": "DirectX"},
            required=False
        )

        gltf2_asset.generator += " and Asobo Studio MSFS2024 Blender I/O v" + get_version_string() + " with Blender v" + get_blender_version_string()
        return

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
        
        if msfs_parameters.remove_lod_prefix:
            MSFS2024_NodeUtils.removeLodPrefix(gltf2_object)

        AsoboUniqueId.export(gltf2_object, blender_object)
        MSFS2024_LightExtension.export(gltf2_object, blender_object)
        AsoboSoftBodyMesh.export(gltf2_object, blender_object)
        return
    
    def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return

        gltf2_node.extensions = {}
        AsoboUniqueId.export(gltf2_node, blender_bone)
        AsoboFacialAnimation.export(gltf2_node, blender_bone)    

    def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, materials, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
            
        # Remove uniform white vertex color attribute since no vertex color in shaders results in a default white value.
        MSFS2024_MeshUtils.remove_color_attribute(gltf2_mesh, blender_mesh)

    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
        AsoboGizmoObject.export(gltf2_scene.nodes, blender_scene, export_settings)

        # Reset transforms of scene root nodes
        if msfs_parameters.reset_node_origin:
            MSFS2024_NodeUtils.resetRootPositions(gltf2_scene.nodes)
                    
    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
        MSFS2024_MaterialExtension.export(gltf2_material, blender_material, export_settings)
    
    def gather_animation_hook(self, gltf2_animation, blender_action, blender_object, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
        AsoboFacialAnimation.export(gltf2_animation, blender_action)
    
    #region Gather Material Animations
    gathered_material_actions = set()
    material_animations = {}
    place_holder_action_names = {}
    actionstoclean_objects_map = {}
    
    if bpy.app.version < (3, 6, 0):
        def gather_actions_hook(self, blender_object, blender_actions, blender_tracks, action_on_type, export_settings):
            msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
            if not msfs_parameters.enable_msfs_extension:
                return
            place_holder_action_name, material_action_name = AsoboPropertyAnimation.add_placeholder_channel(blender_object, export_settings)
            if place_holder_action_name is None or material_action_name is None:
                return
                
            if place_holder_action_name not in blender_tracks:
                blender_actions.append(bpy.data.actions[place_holder_action_name])
                blender_tracks[place_holder_action_name] = place_holder_action_name
                action_on_type[place_holder_action_name] = "OBJECT"

            self.place_holder_action_names[place_holder_action_name] = material_action_name
            self.actionstoclean_objects_map[place_holder_action_name] = blender_object

            # Gather material animations for the given object
            self.material_animations.update(AsoboPropertyAnimation.gather_material_animations(blender_object, self.gathered_material_actions, export_settings))             
    else:
        def gather_actions_hook(self, blender_object, gatheractionshookparams, export_settings):
            msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
            if not msfs_parameters.enable_msfs_extension:
                return
            place_holder_action_name, material_action_name = AsoboPropertyAnimation.add_placeholder_channel(blender_object, export_settings)
            if place_holder_action_name is None or material_action_name is None:
                return

            self.place_holder_action_names[place_holder_action_name] = material_action_name
            self.actionstoclean_objects_map[place_holder_action_name] = blender_object

            if place_holder_action_name not in gatheractionshookparams.blender_tracks:
                gatheractionshookparams.blender_actions.append(bpy.data.actions[place_holder_action_name])
                gatheractionshookparams.blender_tracks[place_holder_action_name] = place_holder_action_name
                gatheractionshookparams.action_on_type[place_holder_action_name] = "OBJECT"

            # Gather material animations for the given object
            self.material_animations.update(AsoboPropertyAnimation.gather_material_animations(blender_object, self.gathered_material_actions, export_settings))

        def pre_gather_tracks_hook(self, blender_object, export_settings):
            msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
            if not msfs_parameters.enable_msfs_extension:
                return
            # Add placeholder animation to the object if it does not exists
            place_holder_action_name, material_action_name = AsoboPropertyAnimation.add_placeholder_channel(blender_object, export_settings)
            if place_holder_action_name is None or material_action_name is None:
                return
            self.place_holder_action_names[place_holder_action_name] = material_action_name
            self.actionstoclean_objects_map[place_holder_action_name] = blender_object

        def gather_tracks_hook(self, blender_object, gathertrackhookparams, export_settings):
            msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
            if not msfs_parameters.enable_msfs_extension:
                return
            # Gather material animations for the given object
            self.material_animations.update(AsoboPropertyAnimation.gather_material_animations(blender_object, self.gathered_material_actions, export_settings))
    
    def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
        AsoboPropertyAnimation.finalize_material_animations(gltf2_plan, self.material_animations, self.place_holder_action_names)
        AsoboPropertyAnimation.clean_placeholder_actions(self.actionstoclean_objects_map)
    
    def gather_gltf_hook(self, active_scene_idx, scenes, animations, export_settings):
        msfs_parameters = bpy.context.scene.msfs_multi_exporter_settings
        if not msfs_parameters.enable_msfs_extension:
            return
        for animation in animations:
            if animation.name not in self.place_holder_action_names:
                continue
            material_action_name = self.place_holder_action_names[animation.name]
            material_animation = self.material_animations[material_action_name]
            AsoboPropertyAnimation.finalize_material_animation(animation, material_animation)
    #endregion