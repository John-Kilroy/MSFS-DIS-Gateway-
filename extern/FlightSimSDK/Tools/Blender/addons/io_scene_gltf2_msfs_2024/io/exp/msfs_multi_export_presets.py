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
import uuid
import bpy
import os
from .msfs_multi_export import MSFS2024_OT_MultiExportGLTF2


class MSFS2024MultiExporterPresetUtils:
    @staticmethod
    def update_relative_path(self, context):
        if not os.path.isabs(self.folder_path) and self.folder_path == "//":
            self.folder_path = self.folder_path + '\\'

    @staticmethod
    def update_group_path(self, context):
        MSFS2024MultiExporterPresetUtils.update_relative_path(self, context)

        groups = context.scene.msfs_multi_exporter_preset_groups
        group = groups[self.name]

        presets = context.scene.msfs_multi_exporter_presets
        for preset in presets:
            if preset.groupID == self.name:
                preset.folder_path = group.folder_path

    @staticmethod
    def update_enabled_group(self, context):
        groups = context.scene.msfs_multi_exporter_preset_groups
        group = groups[self.name]

        presets = context.scene.msfs_multi_exporter_presets
        for preset in presets:
            if preset.groupID == self.name:
                preset.enabled = group.enabled

    @staticmethod
    def update_checked_collection(self, context):
        preset = context.scene.msfs_multi_exporter_presets[self.presetID]
        for collection in self.collection.children:
            if collection.name in preset.layers:
                preset.layers[collection.name].enabled = self.enabled
            return
    

#region Groups
class MultiExporterPresetGroup(bpy.types.PropertyGroup):
    ## name : guid of the Preset Group
    group_name: bpy.props.StringProperty(
        name = "", 
        default = "", 
        description = "Name of the presets's group"
    )

    folder_path: bpy.props.StringProperty(
        name = "", 
        default = "", 
        subtype = "DIR_PATH", 
        description = "Path to the directory where you want the presets to be exported", 
        update = MSFS2024MultiExporterPresetUtils.update_group_path
    )

    enabled: bpy.props.BoolProperty(
        name = "", 
        default = False, 
        description = "Enable/Disable the group for the export", 
        update = MSFS2024MultiExporterPresetUtils.update_enabled_group
    )

    expanded: bpy.props.BoolProperty(
        name = "", 
        default = False, 
        description="Expand/Collapse group."
    )

    def draw(self, context):
        layout = self.layout
        groups = context.scene.msfs_multi_exporter_preset_groups
        presets = context.scene.msfs_multi_exporter_presets

        groupPresetsIDMap = {}

        for groupID, group in groups.items():
            groupPresetsIDMap[groupID] = []

        for presetID, preset in presets.items():
            if preset.groupID == "":
                continue
                
            groupPresetsIDMap[preset.groupID].append(presetID)

        for groupID, presetIDs in groupPresetsIDMap.items():
            group = groups[groupID]

            row = layout.row()

            groupBox = row.box()

            row = groupBox.row()
            row.prop(group, "enabled")
            row.prop(group, "expanded", icon="DOWNARROW_HLT" if group.expanded else "RIGHTARROW")
            row.prop(group, "group_name")
            row.prop(group, "folder_path")
            row.operator(MSFS2024_OT_ShowGroupPresetObjects.bl_idname, text="", icon="HIDE_OFF").groupID = groupID
            row.operator(MSFS2024_OT_AddPreset.bl_idname, text="", icon="ADD").groupID = groupID
            row.operator(MSFS2024_OT_RemovePresetGroup.bl_idname, text="", icon="REMOVE").groupID = groupID

            if group.expanded:
                for presetID in presetIDs:
                    preset = presets[presetID]
                    MultiExporterPreset.draw_preset(preset, groupBox, presetID)
 
class MSFS2024_OT_AddPresetGroup(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_add_preset_group"
    bl_label = "Add group"

    def execute(self, context):
        groups = context.scene.msfs_multi_exporter_preset_groups
        group = groups.add()
        group.name = str(uuid.uuid4())
        group.group_name = f"Group{len(groups)}"
        group.folder_path = ""

        return {"FINISHED"}

class MSFS2024_OT_RemovePresetGroup(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_remove_preset_group"
    bl_label = "Remove group"
    bl_description = "Remove the group from the group list"

    groupID: bpy.props.StringProperty(default="")

    def execute(self, context):
        groups = context.scene.msfs_multi_exporter_preset_groups
        presets = context.scene.msfs_multi_exporter_presets

        for presetID in presets.keys():
            idx = presets.find(presetID)
            if presets[idx].groupID == self.groupID:
                presets.remove(idx)

        groupIdx = groups.find(self.groupID)
        groups.remove(groupIdx)

        return {"FINISHED"}

class MSFS2024_OT_ShowGroupPresetObjects(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_show_group_preset_object"
    bl_label = "Show group's object"

    groupID: bpy.props.StringProperty(default="")

    def execute(self, context):
        bpy.ops.object.hide_view_clear()
        bpy.ops.object.select_all(action='DESELECT')
        presets = context.scene.msfs_multi_exporter_presets
        for preset in presets:
            if preset.groupID == self.groupID:
                MSFS2024_OT_ShowPresetObjects.select_preset_layers(preset)
        bpy.ops.object.hide_view_set(unselected=True)
        return {"FINISHED"}
#endregion

#region Layers
class MultiExporterPresetLayer(bpy.types.PropertyGroup):    
    collection: bpy.props.PointerProperty(
        name = "Collection", 
        type = bpy.types.Collection
    )

    enabled: bpy.props.BoolProperty(
        name = "Enabled", 
        default = False, 
        description = "Enable/Disable the collection for the preset", 
        update = MSFS2024MultiExporterPresetUtils.update_checked_collection
    )

    expanded: bpy.props.BoolProperty(
        name = "Expanded", 
        default = False
    )

    presetID: bpy.props.StringProperty(default = "")

    def __init__(self) -> None:
        presets = bpy.context.scene.msfs_multi_exporter_presets
        for preset in presets:
            for i, layer in enumerate(preset.layers):
                if not layer.collection in list(bpy.data.collections):
                    preset.layers.remove(i)

            for collection in bpy.data.collections:
                if not collection.name in preset.layers:
                    layer = preset.layers.add()
                    layer.name = collection.name
                    layer.collection = collection
                    layer.presetID = preset.name

class MSFS2024_OT_EditLayers(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_edit_layers"
    bl_label = "Edit layers"
    bl_description = "Edit layers to be enabled or disabled for the preset"

    presetID: bpy.props.StringProperty(default = "")

    @staticmethod
    def has_layer_enabled(preset, layer):
        if layer.enabled:
            return True
        
        for child in layer.collection.children:
            if child.name in preset.layers:
                childLayer = preset.layers[child.name]
                if MSFS2024_OT_EditLayers.has_layer_enabled(preset, childLayer):
                    return True

        return False

    @staticmethod
    def load_layers(preset):
        for i, layer in enumerate(preset.layers):
            if not layer.collection.name in bpy.data.collections:
                preset.layers.remove(i)
                
            elif MSFS2024_OT_EditLayers.has_layer_enabled(preset, layer):
                layer.expanded = True

        for collection in bpy.data.collections:
            if not collection.name in preset.layers:
                layer = preset.layers.add()
                layer.name = collection.name
                layer.collection = collection
                layer.presetID = preset.name

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        preset = bpy.context.scene.msfs_multi_exporter_presets[self.presetID]
        MSFS2024_OT_EditLayers.load_layers(preset)

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        preset = context.scene.msfs_multi_exporter_presets[self.presetID]
        MSFS2024_OT_EditLayers.drawTree(layout, bpy.data.scenes["Scene"].collection.children, preset)

        # TODO - update the layers with a list
        # layout.template_list("LAYERS_UL_collectionslot", "Edit Collections", preset, "layers", preset, "preset_index")
        return

    @staticmethod
    def drawChildrenTree(box, tree, preset, factor):
        for collection in tree:
            for layer in preset.layers:
                if layer.collection == collection:
                    row = box.row()

                    split = row.split(factor=factor)
                    col = split.column()
                    col.label(text="")

                    col = split.column()
                    row = col.row()
                    row.prop(layer, "enabled", text="")

                    if layer.collection.children:
                        row.prop(layer, "expanded", text="", icon="DOWNARROW_HLT" if layer.expanded else "RIGHTARROW", emboss=False)

                    row.label(text=layer.collection.name)

                    if layer.expanded:
                        MSFS2024_OT_EditLayers.drawChildrenTree(box, layer.collection.children, preset, factor = factor + 0.1)
                    
                    break
        return

    @staticmethod
    def drawTree(layout, tree, preset):
        for collection in tree:
            box = layout.box()
            for layer in preset.layers:
                if layer.collection == collection:
                    row = box.row()
                    row.prop(layer, "enabled", text="")
                    
                    if layer.collection.children:
                        row.prop(layer, "expanded", text="", icon="DOWNARROW_HLT" if layer.expanded else "RIGHTARROW", emboss=False)

                    row.label(text=layer.collection.name)

                    if layer.expanded:
                        MSFS2024_OT_EditLayers.drawChildrenTree(box, layer.collection.children, preset, factor = 0.1)
                    
                    break
#endregion

#region CollectionUIList
# class LAYERS_UL_collectionslot(bpy.types.UIList):
#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
#         # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             if data:
#                 row = layout.row()
#                 row.prop(item, "enabled", text="")
                    
#                 if item.collection.children:
#                     row.prop(item, "expanded", text="", icon="DOWNARROW_HLT" if item.expanded else "RIGHTARROW", emboss=True)

#                 row.label(text=item.collection.name)
#             else:
#                 layout.label(text="", translate=False, icon_value=icon)
#endregion

#region Presets
class MultiExporterPreset(bpy.types.PropertyGroup):
    ## name : guid of Preset
    preset_name: bpy.props.StringProperty(
        name = "", 
        default = "", 
        description = "Name of the glTF to export"
    )

    folder_path: bpy.props.StringProperty(
        name = "", 
        default = "", 
        subtype = "DIR_PATH", 
        description = "Path to the directory where you want your model to be exported", 
        update = MSFS2024MultiExporterPresetUtils.update_relative_path
    )

    enabled: bpy.props.BoolProperty(
        name = "", 
        default = False, 
        description = "Enable/Disable the preset for the export"
    )

    layers: bpy.props.CollectionProperty(type = MultiExporterPresetLayer)
    groupID: bpy.props.StringProperty(default = "")

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def draw_preset(preset, box, presetID = ""):
        row = box.row()
        if preset.groupID != "":
            split = row.split(factor=1/30)
            col = split.column()
            col.label(text="")
        else:
            split = row.split(factor=1)
        
        col = split.column()

        row = col.row()
        row.prop(preset, "enabled")
        row.prop(preset, "preset_name")
        row.prop(preset, "folder_path")

        row.operator(MSFS2024_OT_ShowPresetObjects.bl_idname, text="", icon="HIDE_OFF").presetID = presetID
        row.operator(MSFS2024_OT_EditLayers.bl_idname, text="", icon="COLLECTION_NEW").presetID = presetID
        row.operator(MSFS2024_OT_RemovePreset.bl_idname, text="", icon="REMOVE").presetID = presetID

    def draw(self, context):
        presets = context.scene.msfs_multi_exporter_presets
        layout = self.layout
        for presetID, preset in presets.items():
            if preset.groupID == "":
                row = layout.row()
                box = row.box()
                MultiExporterPreset.draw_preset(preset, box, presetID)

class MSFS2024_OT_AddPreset(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_add_preset"
    bl_label = "Add preset"

    groupID: bpy.props.StringProperty(default="")

    def execute(self, context):
        presets = context.scene.msfs_multi_exporter_presets
        preset = presets.add()
        preset.name = str(uuid.uuid4())
        preset.preset_name = f"Preset{len(presets)}"
        preset.folder_path = ""
        preset.groupID = self.groupID
        MSFS2024_OT_EditLayers.load_layers(preset)

        if self.groupID != "":
            groups = context.scene.msfs_multi_exporter_preset_groups
            groups[self.groupID].expanded = True

        return {"FINISHED"}

class MSFS2024_OT_RemovePreset(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_remove_preset"
    bl_label = "Remove preset"
    bl_description = "Remove the preset from the preset list"

    presetID: bpy.props.StringProperty(default="")

    def execute(self, context):
        presets = context.scene.msfs_multi_exporter_presets
        idx = presets.find(self.presetID)
        presets.remove(idx)

        return {"FINISHED"}

class MSFS2024_OT_ShowPresetObjects(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_show_preset_object"
    bl_label = "Show preset's object"

    presetID: bpy.props.StringProperty(default="")

    @staticmethod
    def select_preset_layers(preset):
        for layer in preset.layers:
            for obj in layer.collection.objects:
                bpy.context.view_layer.objects.active = obj
                if layer.enabled:
                    obj.select_set(True)

    def execute(self, context):
        preset = context.scene.msfs_multi_exporter_presets[self.presetID]
        bpy.ops.object.hide_view_clear()
        bpy.ops.object.select_all(action='DESELECT')
        MSFS2024_OT_ShowPresetObjects.select_preset_layers(preset)
        bpy.ops.object.hide_view_set(unselected=True)
        return {"FINISHED"}
#endregion

class MSFS2024_PT_MultiExporterPresetsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS2024_PT_MultiExporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "PRESETS"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(MSFS2024_OT_AddPreset.bl_idname, text="Add Preset").groupID = ""
        row.operator(MSFS2024_OT_AddPresetGroup.bl_idname, text="Add Group")

        MultiExporterPreset.draw(self, context)
        MultiExporterPresetGroup.draw(self, context)

        row = layout.row()
        row.operator(MSFS2024_OT_MultiExportGLTF2.bl_idname, text="Export")

def register():
    bpy.types.Scene.msfs_multi_exporter_presets = bpy.props.CollectionProperty(type=MultiExporterPreset)
    bpy.types.Scene.msfs_multi_exporter_preset_groups = bpy.props.CollectionProperty(type=MultiExporterPresetGroup)
