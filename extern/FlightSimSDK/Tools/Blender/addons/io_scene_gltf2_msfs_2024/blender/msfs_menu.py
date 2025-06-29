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
import addon_utils
from .utils.msfs_scene_utils import MSFS2024_SceneUtils

class MSFS2024_OT_ConfirmSceneConversion(bpy.types.Operator):
    bl_idname = "msfs2024.confirm_dialog"
    bl_label = "Do you really want to do that?"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_description = "This will convert all scene to be compatible with MSFS2024 (MSFS2020 addon MUST be enabled)"

    def execute(self, context):
        addon_name = 'io_scene_gltf2_msfs'
        (loaded_default, loaded_state) = addon_utils.check(addon_name)
        # We don't want to convert materials or scene if MSFS2020 is activated
        if not loaded_default and not loaded_state:
            self.report({'ERROR'}, 'You need to enable MSFS2020 addon to convert your scene correctly.')
            return {'CANCELLED'}

        if MSFS2024_SceneUtils.convertSceneToMSFS2024():
            return {'FINISHED'}
        return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="This will convert all scene to be compatible with MSFS2024")
        row = box.row()
        row.label(text="tools (Be aware that you risk losing data that is not supported")
        row = box.row()
        row.label(text="in MSFS2024, and once it's lost, there is no way to recover it")

    def draw_header(self, context):
        self.layout.label(text="WARNING")

class MSFS2024_HeaderMenu(bpy.types.Menu):
    bl_label = "MSFS2024"
    bl_idname = "VIEW3D_MT_MSFS2024"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            operator=MSFS2024_OT_ConfirmSceneConversion.bl_idname, 
            text="Convert scene to MSFS2024"
        )

def draw_menu(self, context):
    self.layout.menu(MSFS2024_HeaderMenu.bl_idname)

def register():
    bpy.types.VIEW3D_MT_editor_menus.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_menu)