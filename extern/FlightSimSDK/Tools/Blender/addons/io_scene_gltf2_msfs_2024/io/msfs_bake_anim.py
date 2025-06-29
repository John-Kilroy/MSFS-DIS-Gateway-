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

from ..blender.utils import msfs_animations_utils as CONSTANTS


def setMode(mode=''):
    if bpy.context.mode != mode:
        bpy.ops.object.mode_set(mode=mode)

def setupRigAnimationData(rig=None):
    if rig:
        if rig.animation_data:
            rig.animation_data.action = None
        else:
            rig.animation_data_create()

def cleanRigNlaTracks(rig=None):
    if rig:
        if rig.animation_data:
            if rig.animation_data.nla_tracks:
                for track in rig.animation_data.nla_tracks:
                    rig.animation_data.nla_tracks.remove(track)
            else:
                print(f"[WARNINIG] Rig : {rig.name} does not have NLA tracks")
        else:
            print(f"[WARNINIG] Rig : {rig.name} does not have animation data set up")

def changeAreaView(stackAreaView = [], newUIType = None, newUIMode = ''):
    # Create a temporary context with an active Dope Sheet Editor
    old_area = bpy.context.area.ui_type
    stackAreaView.append(old_area)
    bpy.context.area.ui_type = newUIType
    if newUIMode != '':
        bpy.context.space_data.ui_mode = newUIMode

    return stackAreaView

def purge_orphans():
    # Delete unreferenced data blocks.
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )

def find_shape_key_driver(mesh, shape_key=''):
    # Find the driver controlling a shape key by comparing the data_path, if any.
    for driver in mesh.data.shape_keys.animation_data.drivers:
        if driver.data_path == f'key_blocks["{shape_key.name}"].value':
            print(f"Found: {shape_key.name}")
            return driver
    return None

def cleanKeyActions():
    for action in bpy.data.actions:
        if "KeyAction" in action.name:
            bpy.data.actions.remove(action)

def assign_animation_to_rig_nla(rig, animation_name):
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    setMode("OBJECT")
    cleanRigNlaTracks(rig)

    # Make the rig active and put it in pose mode.
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    setMode("POSE")

    if rig.animation_data:
        rig.animation_data.action = bpy.data.actions[animation_name]
    
    # Create a temporary context with an active Dope Sheet Editor
    stackAreaView = []
    stackAreaView = changeAreaView(stackAreaView, "DOPESHEET", "ACTION")

    # Push this action to the NLA editor.
    bpy.ops.action.push_down()

    # Rename the NLA track to the shape key name (exclude lod specifier).
    if (len(rig.animation_data.nla_tracks) > 0):
        rig.animation_data.nla_tracks[-1].name = animation_name

    # Restore the original area.
    bpy.context.area.ui_type = stackAreaView[0]
   
def loadAnimation(rig = None, armature = None, rivet_mesh = None, shape_key_name = '', min_range = 1, max_range = 100, rig_level = 0):
    if (rig is not None and armature is not None and rivet_mesh is not None):
        setMode('OBJECT')

        # Delete all animation data on the rig, and purge the unreferenced data blacks
        # Don't use clean_animation_data because we want to keep the drivers.
        setupRigAnimationData(rig)
        cleanRigNlaTracks(rig)
        purge_orphans()

        if ("drive_ssdr_joints" in rig):
            rig["drive_ssdr_joints"] = 1.0

        # Turn off the effect of the NLA editor during animation baking
        rig.animation_data.use_nla = False

        # Get the rivet mesh, and make sure it's visible.
        rivet_mesh.hide_viewport = False
        rivet_mesh.hide_set(False)

        stackAreaView = []
        stackAreaView = changeAreaView(stackAreaView, "DOPESHEET", "ACTION")

        ## Save shape keys in an array
        shape_keys = []
        if shape_key_name != '':
            outputName = f"{shape_key_name}_L{rig_level}"
            if outputName in rivet_mesh.data.shape_keys.key_blocks:
                shape_keys.append(rivet_mesh.data.shape_keys.key_blocks[outputName])
            else:
                print(f"[WARNING] Shape key : {outputName} does not exists in {rivet_mesh.name}.")
                return False
        else:
            shape_keys = reversed(rivet_mesh.data.shape_keys.key_blocks)

        for shape_key in shape_keys:
            # Name of the shape key without the suffix
            shape_key_name = shape_key.name[0:-3]

            if shape_key_name not in CONSTANTS.FACIAL_ANIMATIONS:
                print(f"[WARNING] Animation : {shape_key_name} is not defined in facial animation constants")
                continue
            
            ## Set the timeline to min range
            bpy.context.scene.frame_current = min_range

            # Make sure we're in object mode and the rivet mesh is active.
            bpy.context.view_layer.objects.active = rivet_mesh
            rivet_mesh.select_set(True)
            setMode('OBJECT')

            # If there's a driver on the shape_key, mute it, so the keyframes we will add now will drive the shape key instead.
            driver = find_shape_key_driver(rivet_mesh, shape_key)
            if driver:
                driver.mute = True

            # Put keyframes on the shape key value which will be evaluated and used only if the driver is muted.
            shape_key.value = 0
            shape_key.keyframe_insert(data_path="value", frame=min_range)
            shape_key.value = 1
            shape_key.keyframe_insert(data_path="value", frame=max_range)

            # Make the rig active and put it in pose mode.
            bpy.context.view_layer.objects.active = rig
            rig.select_set(True)
            setMode('POSE')

            ## Set the timeline to min range
            bpy.context.scene.frame_current = min_range

            ## Check if there is already an existing action and remove it if there is
            if shape_key_name in bpy.data.actions:
                action = bpy.data.actions[shape_key_name]
                bpy.data.actions.remove(action)
                print(f'Action {shape_key_name} deleted')
                
            # Blender doesn't like working on invisble objects or bones.
            # Find the rig and armature. Ensure SSDR bones are visible.
            armature.layers[31] = True

            # Select all the SSDR bones relevant to this LOD (these have been added to the "ssdr_joint" selection set during build)
            bones = [b for b in armature.bones if b.layers[31]]
            
            bpy.ops.pose.select_all(action="DESELECT")
            bpy.ops.pose.transforms_clear()

            found = False
            for b in bones:
                if "faceSSDR" in b.name:
                    b.select = True
                    found = True

            if not found:
                print("[WARNING] There is no bone to bake.")
                # Restore the original area.
                bpy.context.area.ui_type = stackAreaView.pop()
                armature.layers[31] = False
                return False

            # Bake the selected joints to a new action. Use visual keying so the result of the constraints is captured.
            bpy.ops.nla.bake(
                frame_start=min_range,
                frame_end=max_range,
                step=99,
                only_selected=True,
                visual_keying=True,
                clear_constraints=False,
                clear_parents=False,
                use_current_action=True,
                clean_curves=True,
                bake_types={"POSE"},
            )

            # Rename the new action to the shape key name (exclude lod specifier).
            rig.animation_data.action.name = shape_key_name

            # Enable extension for action 
            rig.animation_data.action.msfs_facial_animation = True

            # Remove as many static channels as possible. (bones that don't move in this particular pose)
            bpy.ops.action.clean(channels=True, threshold=0.000001)

            for fc in rig.animation_data.action.fcurves:
                for kf in fc.keyframe_points:
                    kf.interpolation = 'LINEAR'

            rig.animation_data.action.msfs_facial_animation = True
            # Push this action to the NLA editor.
            bpy.ops.action.push_down()

            # Rename the NLA track to the shape key name (exclude lod specifier).
            rig.animation_data.nla_tracks[-1].name = shape_key_name
            rig.animation_data.nla_tracks[-1].is_solo = True
            rig.animation_data.nla_tracks[-1].strips[0].blend_type = 'COMBINE'

            # Delete the keyframes on the shape key as they are no longer needed.
            shape_key.keyframe_delete(data_path="value", frame=min_range)
            shape_key.keyframe_delete(data_path="value", frame=max_range)

            # Unmute the driver again.
            if driver:
                driver.mute = False
                print("Driver unmuted")

        # Restore the original area.
        bpy.context.area.ui_type = stackAreaView[0]
        armature.layers[31] = False

        rivet_mesh.hide_viewport = True
        rivet_mesh.hide_set(True)

        # Enable NLA editor again
        rig.animation_data.use_nla = True
        cleanKeyActions()
        setMode("OBJECT")

        if ("drive_ssdr_joints" in rig):
            rig["drive_ssdr_joints"] = 0.0
    else:
        print("[WARNING] Rig, Armature or RivetMesh is not set up correctly")
        return False
    
    return True

def setBonesParentConstraints(rig, enable=True):
    if rig and rig.pose:
        for bone in rig.pose.bones:
            for constraint in bone.constraints:
                constraint.enabled = enable

###################################################################################### OLD ################################################################################
def create_animation(rig, armature, rivet_mesh, min_range = 1, max_range = 100):
    bpy.ops.object.mode_set(mode="OBJECT")
    # Blender doesn't like working on invisble objects or bones.

    # Ensure SSDR bones are visible.
    armature.layers[31] = True

    # Delete all animation data on the rig, and purge the unreferenced data blacks
    # Don't use clean_animation_data because we want to keep the drivers.

    if rig.animation_data:
        rig.animation_data.action = None
    else:
        rig.animation_data_create()

    if rig.animation_data.nla_tracks:
        for track in rig.animation_data.nla_tracks:
            rig.animation_data.nla_tracks.remove(track)

    # Turn off the effect of the NLA editor during animation baking
    rig.animation_data.use_nla = False

    purge_orphans()

    # Get the rivet mesh, and make sure it's visible.
    # rivet_mesh = find_rivet_mesh()
    rivet_mesh.hide_viewport = False
    rivet_mesh.hide_set(False)

    # Create a temporary context with an active Dope Sheet Editor
    old_area = bpy.context.area.ui_type
    bpy.context.area.ui_type = "DOPESHEET"
    bpy.context.space_data.ui_mode = "ACTION"

    # Iterate in reverse over all the shape keys in the rivet mesh.
    # By reversing they end up in the same order in the NLA editor
    for shape_key in reversed(rivet_mesh.data.shape_keys.key_blocks):
        # skip Basis shape key
        if shape_key.name == "Basis":
            continue

        # Make sure we're in object mode and the rivet mesh is active.
        bpy.context.view_layer.objects.active = rivet_mesh
        rivet_mesh.select_set(True)
        bpy.ops.object.mode_set(mode="OBJECT")

        # If there's a driver on the shape_key, mute it, so the keyframes we will add now will drive the shape key instead.
        driver = find_shape_key_driver(rivet_mesh, shape_key)
        if driver:
            driver.mute = True

        # Put keyframes on the shape key value which will be evaluated and used only if the driver is muted.
        shape_key.value = 0
        shape_key.keyframe_insert(data_path="value", frame=min_range)
        shape_key.value = 1
        shape_key.keyframe_insert(data_path="value", frame=max_range)

        # Make the rig active and put it in pose mode.
        bpy.context.view_layer.objects.active = rig
        rig.select_set(True)
        bpy.ops.object.mode_set(mode="POSE")

        # Select all the SSDR bones relevant to this LOD (these have been added to the "ssdr_joint" selection set during build)
        bpy.context.object.data.layers[31] = True
        bones = [b for b in armature.bones if b.layers[31]]
        
        bpy.ops.pose.select_all(action="DESELECT")
        found = False
        for b in bones:
            if "faceSSDR" in b.name:
                b.select = True
                found = True

        if not found:
            print("There is no bone to bake.")
            # Restore the original area.
            bpy.context.area.ui_type = old_area
            return False

        # Bake the selected joints to a new action. Use visual keying so the result of the constraints is captured.
        bpy.ops.nla.bake(
            frame_start=min_range,
            frame_end=max_range,
            step=99,
            only_selected=True,
            visual_keying=True,
            clear_constraints=False,
            clear_parents=False,
            use_current_action=False,
            clean_curves=True,
            bake_types={"POSE"},
        )

        # Rename the new action to the shape key name (exclude lod specifier).
        rig.animation_data.action.name = shape_key.name[0:-3]

        # Remove as many static channels as possible. (bones that don't move in this particular pose)
        bpy.ops.action.clean(channels=True)

        # Push this action to the NLA editor.
        bpy.ops.action.push_down()

        # Rename the NLA track to the shape key name (exclude lod specifier).
        rig.animation_data.nla_tracks[-1].name = shape_key.name[0:-3]
        rig.animation_data.nla_tracks[-1].is_solo = True

        # Delete the keyframes on the shape key as they are no longer needed.
        shape_key.keyframe_delete(data_path="value", frame=min_range)
        shape_key.keyframe_delete(data_path="value", frame=max_range)
        
        # Unmute the driver again.
        if driver:
            driver.mute = False

    # Restore the original area.
    bpy.context.area.ui_type = old_area

    armature.layers[31] = False

    rivet_mesh.hide_viewport = True
    rivet_mesh.hide_set(True)

    # Enable NLA editor again
    rig.animation_data.use_nla = True

    cleanKeyActions()

    return True

def find_rivet_mesh():
    # Find the first mesh starting with "geo_headRivet_".
    for obj in bpy.data.objects:
        if obj.name.startswith("geo_headRivet_"):
            return obj
    return None


 