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
import os
import re
import uuid
import xml.dom.minidom
import xml.etree.ElementTree as etree

import bpy

import json as json

from shutil import copyfile, _samefile

from .textureLib.msfs_texturelib import export_texturelib_with_gltf
from ...sdk import p4 as p4


#region Scene Properties
class MSFS2024MultiExporterProperties:
    bpy.types.Scene.msfs_multi_exporter_current_tab = bpy.props.EnumProperty(
        items=(
            ("OBJECTS", "Objects", ""),
            ("PRESETS", " Presets", ""),
            ("SETTINGS", "Settings", ""),
        )
    )
#endregion

#region Operators
class MSFS2024_OT_MultiExportGLTF2(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_gltf"
    bl_label = "Multi-Export 2024 glTF 2.0"

    #region Export
    def export_blender_under_3_3(self, context, file_path, settings):
        
        return bpy.ops.export_scene.gltf(
                    filepath = file_path,
                    check_existing = True,
                    export_format = 'GLTF_SEPARATE',
                    export_copyright = settings.export_copyright,
                    export_image_format = ('AUTO' if settings.enable_msfs_extension else settings.export_image_format),
                    export_texture_dir = ('' if settings.enable_msfs_extension else settings.export_texture_dir),
                    export_keep_originals = (True if settings.enable_msfs_extension else settings.export_keep_originals),
                    export_texcoords = settings.export_texcoords,
                    export_normals = settings.export_normals,
                    export_draco_mesh_compression_enable = settings.export_draco_mesh_compression_enable,
                    export_draco_mesh_compression_level = settings.export_draco_mesh_compression_level,
                    export_draco_position_quantization = settings.export_draco_position_quantization,
                    export_draco_normal_quantization = settings.export_draco_normal_quantization,
                    export_draco_texcoord_quantization = settings.export_draco_texcoord_quantization,
                    export_draco_color_quantization = settings.export_draco_color_quantization,
                    export_draco_generic_quantization = settings.export_draco_generic_quantization,
                    export_tangents = settings.export_tangents,
                    export_materials = settings.export_materials,
                    export_colors = settings.export_colors,
                    use_mesh_edges = settings.use_mesh_edges,
                    use_mesh_vertices = settings.use_mesh_vertices,
                    export_cameras = settings.export_cameras,
                    use_selection = settings.use_selection,
                    use_visible = settings.use_visible,
                    use_renderable = settings.use_renderable,
                    use_active_collection = settings.use_active_collection,
                    export_yup = settings.export_yup,
                    export_apply = settings.export_apply,
                    export_animations = settings.export_animations,
                    export_frame_range = settings.export_frame_range,
                    export_frame_step = settings.export_frame_step,
                    export_force_sampling = settings.export_force_sampling,
                    export_def_bones = settings.export_def_bones,
                    optimize_animation_size = settings.export_optimize_animation_size,
                    export_current_frame = settings.export_current_frame,
                    export_skins = settings.export_skins,
                    export_all_influences = settings.export_all_influences,
                    export_morph = settings.export_morph,
                    export_morph_normal = settings.export_morph_normal,
                    export_morph_tangent = settings.export_morph_tangent,
                    export_lights = settings.export_lights,
                    will_save_settings = settings.will_save_settings
            )  

    def export_blender_3_3(self, context, file_path, settings):
        return bpy.ops.export_scene.gltf(
                    filepath = file_path,
                    check_existing = True,
                    export_format = 'GLTF_SEPARATE',
                    export_copyright = settings.export_copyright,
                    export_image_format = ('AUTO' if settings.enable_msfs_extension else settings.export_image_format),
                    export_texture_dir = ('' if settings.enable_msfs_extension else settings.export_texture_dir),
                    export_keep_originals = (True if settings.enable_msfs_extension else settings.export_keep_originals),
                    export_texcoords = settings.export_texcoords,
                    export_normals = settings.export_normals,
                    export_draco_mesh_compression_enable = settings.export_draco_mesh_compression_enable,
                    export_draco_mesh_compression_level = settings.export_draco_mesh_compression_level,
                    export_draco_position_quantization = settings.export_draco_position_quantization,
                    export_draco_normal_quantization = settings.export_draco_normal_quantization,
                    export_draco_texcoord_quantization = settings.export_draco_texcoord_quantization,
                    export_draco_color_quantization = settings.export_draco_color_quantization,
                    export_draco_generic_quantization = settings.export_draco_generic_quantization,
                    export_tangents = settings.export_tangents,
                    export_materials = settings.export_materials,
                    export_original_specular = False, ## No need to add option for MSFS uses PBR materials with comp texture for Roughness/Metallic/Occlusion
                    export_colors = settings.export_colors,
                    use_mesh_edges = settings.use_mesh_edges,
                    use_mesh_vertices = settings.use_mesh_vertices,
                    export_cameras = settings.export_cameras,
                    use_selection = settings.use_selection,
                    use_visible = settings.use_visible,
                    use_renderable = settings.use_renderable,
                    use_active_collection = settings.use_active_collection,
                    use_active_scene = settings.use_active_scene,
                    export_yup = settings.export_yup,
                    export_apply = settings.export_apply,
                    export_animations = settings.export_animations,
                    export_frame_range = settings.export_frame_range,
                    export_frame_step = settings.export_frame_step,
                    export_force_sampling = settings.export_force_sampling,
                    export_nla_strips_merged_animation_name = settings.export_nla_strips_merged_animation_name,
                    export_def_bones = settings.export_def_bones,
                    export_optimize_animation_size = settings.export_optimize_animation_size,
                    export_anim_single_armature = settings.export_anim_single_armature,
                    export_current_frame = settings.export_current_frame,
                    export_skins = settings.export_skins,
                    export_all_influences = settings.export_all_influences,
                    export_morph = settings.export_morph,
                    export_morph_normal = settings.export_morph_normal,
                    export_morph_tangent = settings.export_morph_tangent,
                    export_lights = settings.export_lights,
                    will_save_settings = settings.will_save_settings
                )

    def export_blender_3_6(self, context, file_path, settings):
        return bpy.ops.export_scene.gltf(
                    filepath = file_path,
                    check_existing = True,
                    export_format = 'GLTF_SEPARATE',
                    export_copyright = settings.export_copyright,
                    export_image_format = ('AUTO' if settings.enable_msfs_extension else settings.export_image_format),
                    export_jpeg_quality = (75 if settings.enable_msfs_extension else settings.export_jpeg_quality),
                    export_texture_dir = ('' if settings.enable_msfs_extension else settings.export_texture_dir),
                    export_keep_originals = (True if settings.enable_msfs_extension else settings.export_keep_originals),
                    export_texcoords = settings.export_texcoords,
                    export_normals = settings.export_normals,
                    export_draco_mesh_compression_enable = settings.export_draco_mesh_compression_enable,
                    export_draco_mesh_compression_level = settings.export_draco_mesh_compression_level,
                    export_draco_position_quantization = settings.export_draco_position_quantization,
                    export_draco_normal_quantization = settings.export_draco_normal_quantization,
                    export_draco_texcoord_quantization = settings.export_draco_texcoord_quantization,
                    export_draco_color_quantization = settings.export_draco_color_quantization,
                    export_draco_generic_quantization = settings.export_draco_generic_quantization,
                    export_tangents = settings.export_tangents,
                    export_materials = settings.export_materials,
                    export_original_specular = False, ## No need to add option for MSFS uses PBR materials with comp texture for Roughness/Metallic/Occlusion
                    export_colors = settings.export_colors,
                    export_attributes = settings.export_attributes,
                    use_mesh_edges = settings.use_mesh_edges,
                    use_mesh_vertices = settings.use_mesh_vertices,
                    export_cameras = settings.export_cameras,
                    use_selection = settings.use_selection,
                    use_visible = settings.use_visible,
                    use_renderable = settings.use_renderable,
                    use_active_collection = settings.use_active_collection,
                    use_active_scene = settings.use_active_scene,
                    export_yup = settings.export_yup,
                    export_apply = settings.export_apply,
                    export_animations = settings.export_animations,
                    export_frame_range = settings.export_frame_range,
                    export_frame_step = settings.export_frame_step,
                    export_force_sampling = settings.export_force_sampling,
                    export_animation_mode = settings.export_animation_mode,
                    export_nla_strips_merged_animation_name = settings.export_nla_strips_merged_animation_name,
                    export_def_bones = settings.export_def_bones,
                    export_optimize_animation_size = settings.export_optimize_animation_size,
                    export_optimize_animation_keep_anim_armature = settings.export_optimize_animation_keep_anim_armature,
                    export_optimize_animation_keep_anim_object = settings.export_optimize_animation_keep_anim_object,
                    export_negative_frame = settings.export_negative_frame,
                    export_anim_slide_to_zero = settings.export_anim_slide_to_zero,
                    export_reset_pose_bones = settings.export_reset_pose_bones,
                    export_bake_animation = settings.export_bake_animation,
                    export_anim_single_armature = settings.export_anim_single_armature,
                    export_current_frame = settings.export_current_frame,
                    export_rest_position_armature = settings.export_rest_position_armature,
                    export_anim_scene_split_object = settings.export_anim_scene_split_object,
                    export_skins = settings.export_skins,
                    export_all_influences = settings.export_all_influences,
                    export_morph = settings.export_morph,
                    export_morph_normal = settings.export_morph_normal,
                    export_morph_tangent = settings.export_morph_tangent,
                    export_morph_animation = settings.export_morph_animation,
                    export_lights = settings.export_lights,
                    will_save_settings = settings.will_save_settings
                )

    def export(self, context, file_path):
        settings = context.scene.msfs_multi_exporter_settings

        gltf = None
        if (bpy.app.version < (3, 3, 0)):
            gltf = self.export_blender_under_3_3(context, file_path, settings)
        elif (bpy.app.version < (3, 6, 0)):
            gltf = self.export_blender_3_3(context, file_path, settings)
        else:
            gltf = self.export_blender_3_6(context, file_path, settings)
            
        if gltf is None:
            print("[ASOBO] Export failed.")
    #endregion

    #region Common
    def select_object(self, context, blender_object, recursive = True):
        if blender_object not in list(context.window.view_layer.objects):
            return

        blender_object.select_set(True)
        context.selected_objects.append(blender_object)

        if not recursive:
            return

        for child in blender_object.children:
            self.select_object(context, child, recursive)
    
    def remove_object(self, context, blender_object, remove_hierarchy = False):
        self.clear_selection(context)
        self.select_object(context, blender_object, recursive=remove_hierarchy)
        bpy.ops.object.delete()
        return

    def clear_selection(self, context):
        use_ops = context.area == 'VIEW_3D'
        if use_ops:
            bpy.ops.object.select_all(action='DESELECT')
        else:
            for obj in context.selected_objects:
                obj.select_set(False)

    def hide_objects(self, context, objects, hide = True):
        for object in objects:
            object.hide_set(hide)

    def hide_unselected_object(self, context):
        use_ops = context.area == 'VIEW_3D'
        if use_ops:
            bpy.ops.object.hide_view_set(unselected=True)
        else:
            for obj in context.window.view_layer.objects:
                if obj not in context.selected_objects:
                    obj.hide_set(True)
        return
    
    def reveal_hidden_objects(self, context):
        use_ops = context.area == 'VIEW_3D'
        if use_ops:
            bpy.ops.object.hide_view_clear()
        else:
            for obj in context.window.view_layer.objects:
                obj.hide_set(False)
    
    def merge_selected_objects(self, context):
        selected_objects = context.selected_objects

        # Duplicate selected objects
        duplicated_objects = []
        for selected_object in selected_objects:
            self.clear_selection(context)
            self.select_object(context, selected_object)
            
            bpy.ops.object.duplicate()
            duplicated_object = context.selected_objects[0]
            duplicated_objects.append(duplicated_object)

        # Get only duplicated meshs (lights and collisions should not get merged)
        duplicated_objects_to_merge = []
        for duplicated_object in duplicated_objects:
            if duplicated_object.type == "MESH":
                duplicated_objects_to_merge.append(duplicated_object)
        
        # Select objects ready to merge
        self.clear_selection(context)
        for duplicated_object_to_merge in duplicated_objects_to_merge:
            self.select_object(context, duplicated_object_to_merge)
        
        # Merge
        context.view_layer.objects.active = duplicated_objects_to_merge[0]
        bpy.ops.object.join()
        merged_object = context.active_object
        if merged_object.data is not None:
            merged_object.data.name = merged_object.name

        # Attach other objects to merged root
        for duplicated_object in duplicated_objects:
            if duplicated_object in duplicated_objects_to_merge:
                continue
            duplicated_object.parent = merged_object
            
        return merged_object

    def checkout_gltf_path(self, context, gltfPath, binPath):
        if p4.useP4():
            p4.P4edit(gltfPath)
            p4.P4edit(binPath)

    
    def clean_path(self, context, path):
        if path == '//\\':
            path = path.rsplit('\\')[0]
        return path
    #endregion

    #region LODs
    def generate_xml(self, context, lod_group, path):
        found_guid = None
        xml_path = bpy.path.abspath(os.path.join(path, lod_group.name + ".xml"))

        if os.path.exists(xml_path):
            tree = etree.parse(xml_path)
            found_guid = tree.getroot().attrib.get("guid")

        if lod_group.overwrite_guid or found_guid is None:
            root = etree.Element(
                "ModelInfo",
                guid="{" + str(uuid.uuid4()) + "}",
                version="1.1",
            )
        else:
            root = etree.Element("ModelInfo", guid=found_guid, version="1.1")
        
        lods = etree.SubElement(root, "LODS")

        lod_files = {}

        for lod in lod_group.lods:
            if lod.enabled:
                lod_files[lod.file_name] = lod.lod_value

        lod_files = sorted(lod_files.items())
        last_lod = list(lod_files)[-1:]

        if lod_group.autogenerate_lods:
            lods.attrib["autoGenerate"] = "true"
        else:
            for file_name, lod_value in lod_files:
                lod_element = etree.SubElement(lods, "LOD")

                if file_name != last_lod[0]:
                    lod_element.set("minSize", str(lod_value))

                lod_element.set("ModelFile", os.path.splitext(file_name)[0] + ".gltf")

        if lod_files:
            # Format XML
            dom = xml.dom.minidom.parseString(etree.tostring(root))
            xml_string = dom.toprettyxml(encoding="utf-8")
            
            # Checkout File
            if p4.useP4():
                p4.P4edit(xml_path)
                
            with open(xml_path,"wb") as f:
                f.write(xml_string)
                f.close()
        return

    def select_objects_lod(self, context, lod, sort_by_collection):
        if sort_by_collection:
            for obj in lod.collection.all_objects:
                obj.select_set(True)
        else:
            self.select_object(context, lod.objectLOD)
        return

    def get_autoload_path(self, context, path):
        # LOD AutoGeneration : force file name to end with _LOD0.gltf
        pattern = re.compile(r"_LOD[0-9]+\.")
        if pattern.search(path):
            path = pattern.sub("_LOD0.", path)
        else:
            ext_index = path.index(".gltf")
            path = path[:ext_index] + "_LOD0" + path[ext_index:]
        return path
    
    def export_lod(self, context, lod, lod_group):        
        merged_node = None
        limit_visible_objects = context.scene.msfs_multi_exporter_settings.use_visible
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections

        self.clear_selection(context)

        if not limit_visible_objects:
            self.reveal_hidden_objects(context)

        self.select_objects_lod(context, lod, sort_by_collection)
        
        if not limit_visible_objects:
            self.hide_unselected_bject(context)

        if context.scene.msfs_multi_exporter_settings.merge_nodes:
            merged_node = self.mergeSelectedObjects(context)
            self.clear_selection(context)
            self.select_object(context, merged_node)

        export_folder_path = bpy.path.abspath(lod_group.folder_path)
        if export_folder_path != "":
            exportPath = bpy.path.ensure_ext(os.path.join(export_folder_path, os.path.splitext(lod.file_name)[0]), ".gltf")
            exportPathBin = bpy.path.ensure_ext(os.path.join(export_folder_path, os.path.splitext(lod.file_name)[0]), ".bin")

            if lod_group.autogenerate_lods and "_LOD0." not in lod.file_name:
                exportPath = self.get_autoload_path(context, exportPath)

            self.checkout_gltf_path(context, exportPath, exportPathBin)
            self.export(context, exportPath)

            # Remove merged node from scene
            if merged_node is not None:
                self.remove_object(context, merged_node, True)
                
            return True, exportPath
        else:
            self.report({'ERROR'}, f"[EXPORT][ERROR] Object : {lod.file_name} does not have an export path set.")

        return False, ""

    def export_lod_group(self, context, lod_group):
        export_folder_path = self.clean_path(context, lod_group.folder_path)
        exported_paths = []

        # Generate XML if needed
        if lod_group.generate_xml:
            self.generate_xml(context, lod_group, export_folder_path)

        # Export glTF
        for lod in lod_group.lods:
            if not lod.enabled:
                continue
            exported, exported_path = self.export_lod(context, lod, lod_group)
            if exported:
                exported_paths.append(exported_path)

        return exported_paths
                    
    def export_lods(self, context):
        lod_groups = context.scene.msfs_multi_exporter_lod_groups

        exported_paths = []
        for lod_group in lod_groups:
            exportedLodGroupPaths = self.export_lod_group(context, lod_group)
            exported_paths.extend(exportedLodGroupPaths)

        return exported_paths
    #endregion

    #region Presets
    def select_objects_from_collection(self, context, layers):
        layer_objects = []
        for layer in layers:
            if not layer.enabled:
                continue
            layer_objects.extend(layer.collection.all_objects)

        for obj in layer_objects:
            self.select_object(context, obj, recursive=False)
    
    def export_preset(self, context, preset):
        merged_node = None
        limit_visible_objects = context.scene.msfs_multi_exporter_settings.use_visible
        self.clear_selection(context)

        if not limit_visible_objects:
            self.reveal_hidden_objects(context)

        self.select_objects_from_collection(context, preset.layers)
        
        if not limit_visible_objects:
            self.hide_unselected_object(context)

        if context.scene.msfs_multi_exporter_settings.merge_nodes:
            merged_node = self.merge_selected_objects(context)
            self.clear_selection(context)
            self.select_object(context, merged_node)

        if preset.folder_path != "":
            export_folder_path = self.clean_path(context, preset.folder_path)
            export_folder_path = bpy.path.abspath(export_folder_path)

            exportPath = bpy.path.ensure_ext(os.path.join(export_folder_path, preset.preset_name), ".gltf")
            exportPathBin = bpy.path.ensure_ext(os.path.join(export_folder_path, preset.preset_name), ".bin")

            self.checkout_gltf_path(context, exportPath, exportPathBin)
            self.export(context, exportPath)

            # Remove merged node from scene
            if merged_node is not None:
                self.remove_object(context, merged_node, True)

            return True, exportPath

        self.report({'ERROR'}, f"[EXPORT][ERROR] Preset : {preset.preset_name} does not have an export path set.")
        return False, ""
        
    def export_presets(self, context):
        presets = context.scene.msfs_multi_exporter_presets
        exportedPaths = []
        for preset in presets:
            if not preset.enabled:
                continue
            exported, exportpath = self.export_preset(context, preset)
            if exported:
                exportedPaths.append(exportpath)
        return exportedPaths
    #endregion

    #region Textures
    def export_gltf_textures(self, context, gltf_path, texture_dir):
        if not os.path.exists(gltf_path):
            return
        
        gltf_dir_path = os.path.dirname(gltf_path)

        if not os.path.isabs(texture_dir):
            texture_dir = os.path.join(gltf_dir_path, texture_dir)
            texture_dir = os.path.abspath(texture_dir)

        if not os.path.exists(texture_dir):
            try:
                os.mkdir(texture_dir)
            except:
                self.report({'ERROR'}, f"[TEXTURE] Folder {texture_dir} could not be created")
                return
        
        json_file_object = None
        try:
            with open(gltf_path, 'r') as file:
                json_file_object = json.load(file)
        except IOError:
            self.report({'ERROR'}, f"[TEXTURE] File '{gltf_path}' could not be opened. File access denied")
            self.report({'ERROR'}, f"[TEXTURE] Textures will not be written")
            return
        
        if json_file_object is None:
            return
        
        gltf_images = json_file_object.get("images")
        if gltf_images is None:
            return

        for gltf_image in gltf_images:
            image_path = gltf_image.get("uri")
            if image_path is None:
                continue

            image_path = os.path.join(gltf_dir_path, image_path)
            image_path = image_path.replace('/','\\')
            image_path = os.path.abspath(image_path)

            # Check if there is a whitespace and replace it in path
            if '%20' in image_path:
                image_path = image_path.replace('%20', ' ')

            if not os.path.exists(image_path):
                print(f"[TEXTURE] File '{image_path}' do not exists")
                continue

            image_name = os.path.basename(image_path)

            new_image_path = os.path.join(texture_dir, image_name)
            new_image_path = os.path.abspath(new_image_path)

            # Change texture path in gltf
            if len(os.path.commonprefix([new_image_path, gltf_path])) != 0:
                gltf_image['uri'] = os.path.relpath(path=new_image_path, start=gltf_dir_path)

            # Copy image if the image not already exists in the folder
            if _samefile(image_path, new_image_path):
                continue

            copyfile(image_path, new_image_path)
            print(f"[TEXTURE][{image_name}] Texture copied from '{image_path}' to '{new_image_path}'")

        # Serializing json
        json_object = json.dumps(json_file_object, indent=4)

        # Write in file
        try:
            file = open(gltf_path, 'w+')
            if file:
                file.write(json_object)
            file.close()
        except IOError:
            self.report({'ERROR'}, f"[TEXTURE] File '{gltf_path}' could not be written. File access denied")
            return

        return

    def export_textures(self, context, gltf_paths, texture_dir):
        for gltf_path in gltf_paths:
            self.export_gltf_textures(context, gltf_path, texture_dir)
        return
    #endregion

    def execute(self, context):
        gltf_paths = []
        visible_objects = context.visible_objects

        #region Objects
        if context.scene.msfs_multi_exporter_current_tab == "OBJECTS":
            exportedPaths = self.export_lods(context)
            gltf_paths.extend(exportedPaths)
        #endregion

        #region Presets
        elif context.scene.msfs_multi_exporter_current_tab == "PRESETS":
            exportedPaths = self.export_presets(context)
            gltf_paths.extend(exportedPaths)
        #endregion

        # Restore Visible Objects
        self.hide_objects(context, context.window.view_layer.objects, True)
        self.hide_objects(context, visible_objects, False)

        if len(gltf_paths) < 1:
            self.report({"ERROR"}, "An error occurred during export, no glTF files were exported.")
            return {"CANCELLED"}

        #region Textures
        settings = context.scene.msfs_multi_exporter_settings
        texture_dir = settings.export_texture_dir

        if (not settings.export_keep_originals):
            self.export_textures(
                context, 
                gltf_paths, 
                texture_dir
            )

        if (settings.generate_texturelib):
            export_texturelib_with_gltf(
                gltf_paths, 
                settings.export_keep_originals, 
                texture_dir
            )
        #endregion
        return {"FINISHED"}

class MSFS2024_OT_ChangeTab(bpy.types.Operator):
    bl_idname = "msfs2024.multi_export_change_tab"
    bl_label = "Change tab"

    current_tab: bpy.types.Scene.msfs_multi_exporter_current_tab

    def execute(self, context):
        context.scene.msfs_multi_exporter_current_tab = self.current_tab
        return {"FINISHED"}
#endregion

#region Panels
class MSFS2024_PT_MultiExporter(bpy.types.Panel):
    bl_label = "Multi-Export glTF 2.0"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Microsoft Flight Simulator 2024 Tools"

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_settings

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        current_tab = context.scene.msfs_multi_exporter_current_tab
        
        row = layout.row(align=True)
        row.operator(MSFS2024_OT_ChangeTab.bl_idname, text="Objects", depress=(current_tab == "OBJECTS")).current_tab = "OBJECTS"
        row.operator(MSFS2024_OT_ChangeTab.bl_idname, text="Presets", depress=(current_tab == "PRESETS")).current_tab = "PRESETS"
        row.operator(MSFS2024_OT_ChangeTab.bl_idname, text="Settings", depress=(current_tab == "SETTINGS")).current_tab = "SETTINGS"


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(MSFS2024_PT_MultiExporter)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    try:
        bpy.utils.unregister_class(MSFS2024_PT_MultiExporter)
    except Exception:
        pass
#endregion
