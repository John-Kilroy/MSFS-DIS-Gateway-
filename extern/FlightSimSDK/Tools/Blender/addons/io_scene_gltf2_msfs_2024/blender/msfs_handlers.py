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
import addon_utils

from bpy.app.handlers import persistent

from .utils.msfs_scene_utils import MSFS2024_SceneUtils
from .utils.msfs_mesh_utils import  MSFS2024_MeshUtils


initial_objects = set()

@persistent
def new_object_handler(scene):
    """
    Add a default vertex color on new object. 
    When there is no color attribute, shader vertex color node outputs
    a black color. Since there is no way to detect the presence of a color attribute 
    in shaders, we assign a default white color every time an object is created.
    """
    global initial_objects
    current_objects = set(bpy.data.objects)

    new_objects = current_objects - initial_objects
    
    for obj in new_objects:
        if obj.type == 'MESH' :
            MSFS2024_MeshUtils.add_default_vcolor(obj)
    
    initial_objects = current_objects

@persistent
def load_handler(dummy):
    #region Presets compatibility
    presets = bpy.context.scene.msfs_multi_exporter_presets
    for preset in presets:
        if preset.preset_name == "":
            preset.preset_name = preset.name
            preset.name = str(uuid.uuid4())
    #endregion

    #region Object LODS compatibility
    lod_groups = bpy.context.scene.msfs_multi_exporter_lod_groups
    for lod_group in lod_groups:
        if lod_group.group_name != "":
            lod_group.name = lod_group.group_name
    #endregion

    addon_name = 'io_scene_gltf2_msfs'
    (loaded_default, loaded_state) = addon_utils.check(addon_name)
    # We don't want to convert materials or scene if MSFS2020 is activated
    if not loaded_default and not loaded_state:
        MSFS2024_SceneUtils.convertMaterialsToMSFS2024()

bpy.app.handlers.load_post.append(load_handler)
bpy.app.handlers.load_post.append(new_object_handler)
bpy.app.handlers.depsgraph_update_post.append(new_object_handler)