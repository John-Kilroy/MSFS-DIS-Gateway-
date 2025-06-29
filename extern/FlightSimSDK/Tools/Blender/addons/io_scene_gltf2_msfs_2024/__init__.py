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
import sys
import importlib
import inspect
import pkgutil
from pathlib import Path

if "bpy" in locals():#Reload entire addon
    current_package_prefix = f"{__name__}."
    for name, module in sys.modules.copy().items():
        if name.startswith(current_package_prefix):
            print(f"Reloading {name}")
            importlib.reload(module)

import bpy

bl_info = {
    "name": "Microsoft Flight Simulator 2024 glTF Extension",
    "author": "Yasmine Khodja, Luca Pierabella, Wing42, pepperoni505, ronh991, and others",
    "description": "This toolkit prepares your 3D assets to be used for Microsoft Flight Simulator 2024",
    "blender": (3, 3, 0),
    "version": (0, 3, 6),
    "location": "File > Import-Export",
    "category": "Import-Export"
    # "tracker_url": "https://github.com/AsoboStudio/glTF-Blender-IO-MSFS2024"
}

def get_version_string():
    return str(bl_info['version'][0]) + '.' + str(bl_info['version'][1]) + '.' + str(bl_info['version'][2])

#region Panels

#region Importer
class MSFS2024_PT_importer_panel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Microsoft Flight Simulator 2024 : Importer glTF 2.0"
    bl_parent_id = "GLTF_PT_import_user_extensions"
    bl_location = "File > Import > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "IMPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='TOOL_SETTINGS')

    def draw(self, context):
        props = context.scene.msfs_multi_exporter_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(props, "enable_msfs_extension", text="")
#endregion

#region Exporter
class MSFS2024_PT_exporter_panel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Microsoft Flight Simulator 2024 : Exporter glTF 2.0"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_location = "File > Export > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        settings = context.scene.msfs_multi_exporter_settings
        self.layout.label(icon='TOOL_SETTINGS')
        self.layout.prop(settings, "enable_msfs_extension", text="")

    def draw(self, context):
        return

class MSFS2024_PT_exporter_extension(bpy.types.Panel):
    bl_space_type = "FILE_BROWSER"
    bl_region_type = "TOOL_PROPS"
    bl_label = "Extensions"
    bl_parent_id = "MSFS2024_PT_exporter_panel"
    bl_location = "File > Export > glTF 2.0"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw(self, context):
        settings = context.scene.msfs_multi_exporter_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.active = settings.enable_msfs_extension

        layout.prop(settings, 'use_unique_id', text="Enable ASOBO Unique ID extension")

class MSFS2024_PT_exporter_texture(bpy.types.Panel):
    bl_space_type = "FILE_BROWSER"
    bl_region_type = "TOOL_PROPS"
    bl_label = "Textures"
    bl_parent_id = "MSFS2024_PT_exporter_panel"
    bl_location = "File > Export > glTF 2.0"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw(self, context):
        settings = context.scene.msfs_multi_exporter_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.active = settings.enable_msfs_extension

        layout.prop(settings, "generate_texturelib", text="Generate TextureLib")

class MSFS2024_PT_exporter_process(bpy.types.Panel):
    bl_space_type = "FILE_BROWSER"
    bl_region_type = "TOOL_PROPS"
    bl_label = "Export Process"
    bl_parent_id = "MSFS2024_PT_exporter_panel"
    bl_location = "File > Export > glTF 2.0"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw(self, context):
        settings = context.scene.msfs_multi_exporter_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.active = settings.enable_msfs_extension
        layout.prop(settings, "reset_node_origin")
        layout.prop(settings, "remove_lod_prefix")
        layout.prop(settings, "merge_nodes")
#endregion
#endregion


#region ######################### REGISTRATION #################################

   
modules=[]
classes = []
extension_panels = [
    MSFS2024_PT_importer_panel, 
    MSFS2024_PT_exporter_panel,
    MSFS2024_PT_exporter_extension,
    MSFS2024_PT_exporter_texture,
    # MSFS2024_PT_exporter_process
]

def recursive_module_search(path, root=""):
    for _, name, ispkg in pkgutil.iter_modules([str(path)]):
        if ispkg:
            yield from recursive_module_search(path / name, f"{root}.{name}")
        else:
            yield root, name

def update_module_list():
    global modules
    for root, name in recursive_module_search(Path(__file__).parent):
        modules.append(importlib.import_module(f".{name}", package=f"{__package__}{root}")) 
    return modules

# Refresh the list of classes
def update_class_list():
    global modules
    global classes
    
    classes = []

    for module in modules:
        for obj in module.__dict__.values():
            if inspect.isclass(obj) \
                    and module.__name__ in str(obj) \
                    and "bpy" in str(inspect.getmro(obj)[1]):
                classes.append(obj)


def register():
    global modules
    global classes

    update_module_list()
    # Refresh the list of classes whenever the addon is reloaded so we can stay up to date with the files on disk.
    update_class_list()
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass
    
    for module in modules:
        if hasattr(module, "register"):
            module.register()

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    global extension_panels
    global modules
    for panel in extension_panels:
        try:
            bpy.utils.register_class(panel)
        except Exception:
            pass

    for module in modules:
        if hasattr(module, "register_panel"):
            module.register_panel()

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister():
    global classes
    global modules
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()


def unregister_panel():
    global extension_panels
    global modules
    for panel in extension_panels:
        try:
            bpy.utils.unregister_class(panel)
        except Exception:
            pass

    for module in modules:
        if hasattr(module, "unregister_panel"):
            module.unregister_panel()

#endregion
#region ######################### IMPORT #################################
from .io.imp.msfs_import import Import


class glTF2ImportUserExtension(Import):
    def __init__(self):
        return

#endregion
#region ######################### EXPORT #################################
from .io.exp.msfs_export import Export


class glTF2ExportUserExtension(Export):
    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        return
#endregion
