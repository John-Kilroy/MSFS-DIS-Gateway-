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
import os
import re

from .msfs_multi_export import MSFS2024_OT_MultiExportGLTF2

#region Properties
class MultiExporterLOD(bpy.types.PropertyGroup):

    def update_lod_enabled(self, context):
        if not self.enabled:
            return

        for lod_group in context.scene.msfs_multi_exporter_lod_groups:
            if not lod_group.autogenerate_lods:
                continue

            for lod in lod_group.lods:
                if lod != self:
                    lod.enabled = False

    objectLOD: bpy.props.PointerProperty(
        name = "Object", 
        type = bpy.types.Object
    )

    collection: bpy.props.PointerProperty(
        name = "Collection", 
        type=bpy.types.Collection
    )

    enabled: bpy.props.BoolProperty(
        name = "Enabled", 
        default = False, 
        update = update_lod_enabled, 
        description = "Enable/Disable to export"
    )

    lod_value: bpy.props.FloatProperty(
        name = "LOD Value", 
        default = 0, 
        min = 0, 
        max = 999,
        precision = 4
    )

    file_name: bpy.props.StringProperty(
        name = "File name", 
        default = "", 
        description = "File name of the exported model"
    )

    group_name: bpy.props.StringProperty(
        name = "Group Name", 
        default = ""
    )

class MultiExporterLODGroup(bpy.types.PropertyGroup):

    def update_autogenerate_lod(self, context):
        first_lod_encountered = False
        for lod in self.lods:
            if not lod.enabled:
                continue
            if first_lod_encountered:
                lod.enabled = False
            else:
                first_lod_encountered = True

    def update_relative_path(self, context):
        if not os.path.isabs(self.folder_path) and self.folder_path == "//":
            self.folder_path = self.folder_path + '\\'

    def update_group_lod_enabled(self, context):
        for lod in self.lods:
            lod.enabled = self.enabled

    # We will need to keep this for retro-compatibility
    group_name: bpy.props.StringProperty(
        name = "Group Name", 
        default = ""
    )

    expanded: bpy.props.BoolProperty(
        name = "Expanded", 
        default = True
    )

    lods: bpy.props.CollectionProperty(type=MultiExporterLOD)

    folder_path: bpy.props.StringProperty(
        name = "Export Folder Path", 
        default = "", 
        subtype = "DIR_PATH", 
        description = "Path to the directory where you want your model to be exported", 
        update = update_relative_path
    )

    generate_xml: bpy.props.BoolProperty(
        name = "Generate XML", 
        default = False
    )

    overwrite_guid: bpy.props.BoolProperty(
        name = "Overwrite GUID", 
        default = False,
        description = "If an XML file already exists in the location to export to, the GUID will be overwritten"
    )

    autogenerate_lods: bpy.props.BoolProperty(
        name = "Autogenerate LODs", 
        default = False, 
        description = (
            "If enabled, only the first LOD will be exported. \
            When the Microsoft Flight Simulator 2024's BuildPackage process will be used, \
            LODs will be generated automatically, using Simplygon"
        ), 
        update = update_autogenerate_lod
    )

    enabled: bpy.props.BoolProperty(
        name = "Enabled", 
        default = False, 
        update = update_group_lod_enabled, 
        description = "Enable/Disable all LODs to export"
    )
#endregion

#region Operators
class MSFS2024_OT_ReloadLODGroups(bpy.types.Operator):
    bl_idname = "msfs2024.reload_lod_groups"
    bl_label = "Reload LOD groups"

    def object_exists(self, context, object):
        return object in list(context.window.view_layer.objects)

    def object_is_root(self, context, object):
        if object.parent is None:
            return True
        return False

    def collection_exists(self, context, collection):
        return collection in list(context.window.view_layer.layer_collection.children)

    def get_group_name_from_lod_name(self, context, name):
        matches = re.findall("^x[0-9]_|_LOD[0-9]+", name)
        # If an object starts with xN_ or ends with _LODN, treat as an LOD
        if matches:
            # Get base object group name from object
            for match in matches:
                filtered_string = name.replace(match, "")
            return filtered_string
        else:
            # If prefix or suffix isn't found, use the object name as the group
            return name

    def remove_deleted_lods(self, context):
        lod_groups = context.scene.msfs_multi_exporter_lod_groups
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections
        for lod_group_key, lod_group in lod_groups.items():
            lods = lod_group.lods
            for lod_key, lod in lods.items():
                if sort_by_collection:
                    if (self.collection_exists(context, lod.collection)):
                        continue
                else:
                    if self.object_exists(context, lod.objectLOD) \
                       and self.object_is_root(context, lod.objectLOD) \
                       and lod_key == lod.objectLOD.name:
                        continue

                lod_index = lods.find(lod_key)
                lods.remove(lod_index)

            if len(lod_group.lods) == 0:
                lod_group_index = lod_groups.find(lod_group_key)
                lod_groups.remove(lod_group_index)

    def get_new_group_lods(self, context):
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections
        found_lod_groups = {}

        if sort_by_collection:
            for collection in bpy.data.collections:
                lod_group_name = self.get_group_name_from_lod_name(context, collection.name)
                if lod_group_name not in found_lod_groups:
                    found_lod_groups[lod_group_name] = []
                found_lod_groups[lod_group_name].append(collection)
        else:
            for obj in context.window.view_layer.objects:
                if obj.parent is not None:
                    continue

                lod_group_name = self.get_group_name_from_lod_name(context, obj.name)
                if lod_group_name not in found_lod_groups:
                    found_lod_groups[lod_group_name] = []

                found_lod_groups[lod_group_name].append(obj)
            
        return found_lod_groups

    def reload_lod_groups(self, context):
        lod_groups = context.scene.msfs_multi_exporter_lod_groups
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections

        # Remove deleted LODs
        self.remove_deleted_lods(context)

        # Get new lod groups
        found_lod_groups = self.get_new_group_lods(context)

        # Add to object groups
        for lod_group_name, lods in found_lod_groups.items():
            if lod_group_name not in lod_groups:
                # Create LOD group
                lod_group = lod_groups.add()
                lod_group.name = lod_group_name

            lod_group = lod_groups[lod_group_name]

            if sort_by_collection:
                for collection in lods:
                    if collection in [lod.collection for lod in lod_group.lods]:
                        continue

                    lod = lod_group.lods.add()
                    lod.collection = collection
                    lod.file_name = collection.name
                    lod.name = collection.name
                    lod.group_name = lod_group.name
            else:
                for rootObject in lods:
                    if rootObject in [lod.objectLOD for lod in lod_group.lods]:
                        continue

                    lod = lod_group.lods.add()
                    lod.objectLOD = rootObject
                    lod.file_name = rootObject.name
                    lod.name = rootObject.name
                    lod.group_name = lod_group.name

    def execute(self, context):
        self.reload_lod_groups(context)
        return {"FINISHED"}
#endregion

#region Panel
class MSFS2024_PT_MultiExporterObjectsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS2024_PT_MultiExporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "OBJECTS"

    def draw_lod(self, context, lod, autogenerate_lods, box):
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections
        row = box.row()

        if sort_by_collection:
            row.prop(lod, "enabled", text = lod.collection.name if lod.collection is not None else "")
        else:
            row.prop(lod, "enabled", text = lod.objectLOD.name if lod.objectLOD is not None else "")

        row.prop(lod, "file_name", text="")

        if not autogenerate_lods:
            row.prop(lod, "lod_value", text="LOD Value")
        return

    def draw_lod_group(self, context, lod_group):
        if len(lod_group.lods) == 0:
            return
        
        layout = self.layout
        row = layout.row()

        box = row.box()
        row = box.row()
        
        col = row.column()
        col.prop(lod_group, "enabled", text="")
        col = row.column()
        col.prop(lod_group, "expanded", icon="DOWNARROW_HLT" if lod_group.expanded else "RIGHTARROW", text="")
        col = row.column()
        col.prop(lod_group, "name", emboss = False, text="")

        if lod_group.expanded:
            row = box.row()
            row.prop(lod_group, "folder_path", text="Export Folder Path")

            row = box.row()
            row.prop(lod_group, "generate_xml", text="Generate XML")

            if lod_group.generate_xml:
                row.prop(lod_group, "overwrite_guid", text="Overwrite GUID")
                row.prop(lod_group, "autogenerate_lods", text="Enable Auto LOD")
            
            for lod in lod_group.lods:
                self.draw_lod(context, lod, lod_group.autogenerate_lods, box)
        return

    def get_number_lods(self, context):
        lod_groups = context.scene.msfs_multi_exporter_lod_groups

        total_lods = 0
        for lod_group in lod_groups:
            total_lods += len(lod_group.lods)

        return total_lods

    def draw(self, context):
        layout = self.layout

        layout.operator(MSFS2024_OT_ReloadLODGroups.bl_idname, text = "Reload LODs")
        layout.prop(context.scene, "multi_exporter_grouped_by_collections")

        lod_groups = context.scene.msfs_multi_exporter_lod_groups

        total_lods = self.get_number_lods(context)

        if total_lods == 0:
            box = layout.box()
            box.label(text="No LODs found in scene")
        else:
            for lod_group in lod_groups:
                self.draw_lod_group(context, lod_group)

        row = layout.row(align=True)
        row.operator(MSFS2024_OT_MultiExportGLTF2.bl_idname, text="Export")
#endregion

#####################################################################
def update_grouped_by(self, context):
    context.scene.msfs_multi_exporter_lod_groups.clear()
    bpy.ops.msfs2024.reload_lod_groups()
    return

def register():
    bpy.types.Scene.msfs_multi_exporter_lod_groups = bpy.props.CollectionProperty(type=MultiExporterLODGroup)
    
    bpy.types.Scene.multi_exporter_grouped_by_collections = bpy.props.BoolProperty(
        name = "Grouped by collections",
        default = False,
        update = update_grouped_by
    )
