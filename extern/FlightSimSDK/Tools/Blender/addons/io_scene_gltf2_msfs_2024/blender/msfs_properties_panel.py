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

class MSFS2024_PT_BoneProperties(bpy.types.Panel):
    bl_label = "MSFS2024 Bone Properties"
    bl_idname = "BONE_PT_msfs2024_bone_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'
    
    @classmethod
    def poll(cls, context):
        return (context.active_bone is not None)

    def draw(self, context):
        if context.mode != 'EDIT_ARMATURE':
            layout = self.layout
            box = None
            active_bone = context.active_bone
            if hasattr(active_bone, "msfs_override_unique_id"):
                box = layout.box()
                box.prop(active_bone,"msfs_override_unique_id")
                if active_bone.msfs_override_unique_id:
                    box.prop(active_bone, "msfs_unique_id")
            if hasattr(active_bone, "msfs_facial_animation"):
                if box == None:
                    box = layout.box()
                box.prop(active_bone, "msfs_facial_animation")

class MSFS2024_PT_ObjectProperties(bpy.types.Panel):
    bl_label = "MSFS2024 Object Parameters"
    bl_idname = "OBJECT_PT_msfs2024_object_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def draw_object_properties(self, context, active_object, layout):
        box = layout.box()
        box.label(text = "MSFS2024 Object Parameters", icon='OBJECT_DATA')
        box.prop(active_object,"msfs_override_unique_id")
        if active_object.msfs_override_unique_id:
            box.prop(active_object, "msfs_unique_id")

        # box.prop(active_object, "msfs_facial_animation")
        return

    def draw_mesh_properties(self, context, active_object, layout):
        box = layout.box()
        box.label(text = "MSFS2024 Mesh Parameters", icon='MESH_DATA')
        box.prop(active_object.data, "msfs_softbody")
        return

    def draw_collision_parameters(self, context, active_object, layout):
        box = layout.box()
        box.label(text="MSFS2024 Collision Parameters", icon='EMPTY_DATA')
        box.prop(active_object, "msfs_gizmo_type")
        if active_object.msfs_gizmo_type != "NONE" and active_object.msfs_gizmo_type != "boundingSphere":
            box.prop(active_object, "msfs_collision_is_road_collider")

    def draw(self, context):
        layout = self.layout
        active_object = context.object

        self.draw_object_properties(context, active_object, layout)

        if active_object.type == 'MESH':
            self.draw_mesh_properties(context, active_object, layout)

        elif active_object.type == 'EMPTY':
            self.draw_collision_parameters(context, active_object, layout)

class MSFS2024_PT_ActionProperties(bpy.types.Panel):
    bl_label = "MSFS2024 Action Parameters"
    bl_idname = "ACTION_PT_msfs2024_action_properties"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_category = "Action"
    bl_region_type = 'UI'
    bl_context = "data"
    
    @classmethod
    def poll(cls, context):
        return context.active_action is not None and context.object.mode in ('POSE', 'OBJECT')

    def draw(self, context):
        layout = self.layout
        box = None
        active_action = context.active_action
        if hasattr(active_action, "msfs_facial_animation"):
            box = layout.box()
            box.prop(active_action, "msfs_facial_animation")

