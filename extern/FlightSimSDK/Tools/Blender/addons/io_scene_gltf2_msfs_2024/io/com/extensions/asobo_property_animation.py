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

import typing
import bpy

from io_scene_gltf2.io.com import gltf2_io_constants
from io_scene_gltf2.io.com import gltf2_io
from io_scene_gltf2.io.exp import gltf2_io_binary_data

from io_scene_gltf2.blender.exp import gltf2_blender_gather_accessors
from io_scene_gltf2.blender.com import gltf2_blender_math


from ....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties
from .material.asobo_material_uv_options import AsoboMaterialUVOptionsExtension
from .material.asobo_material_windshield import AsoboMaterialWindshieldExtension
from .material.asobo_material_dirt import AsoboMaterialDirtExtension

class AsoboChannel:
    def __init__(self, fcurve: bpy.types.FCurve, data_path: str, array_index: int, target_property: str, material_name: str, sampler : gltf2_io.AnimationSampler):
        self.fcurve = fcurve
        self.data_path = data_path
        self.array_index = array_index
        self.target_property = target_property
        self.material_name = material_name
        self.sampler = sampler

class Keyframe:
    def __init__(self, channels: typing.Tuple[bpy.types.FCurve] = [], frame: float = 0.0):
        self.seconds = frame / bpy.context.scene.render.fps
        self.frame = frame
        self.fps = bpy.context.scene.render.fps
        self.target = ""
        if len(channels) > 0:
            self.target = [c for c in channels if c is not None][0].data_path.split('.')[-1]

class AsoboMaterialAnimation:
    def __init__(self, channels: typing.List[AsoboChannel]):
        self.channels = channels
        self.name = ""

class AsoboPropertyAnimation:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_property_animation"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def has_material_action(blender_object: bpy.types.Object, export_settings) -> typing.Tuple[bool, bpy.types.Action]:
        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None:
                continue

            if material.animation_data is not None:
                if material.animation_data.action:
                    return True, material.animation_data.action.name

                if bpy.app.version > (3, 6, 0):
                    export_animations = (export_settings["gltf_animation_mode"] == 'NLA_TRACKS') or (export_settings['gltf_animation_mode'] == "ACTIONS")
                else:
                    export_animations = export_settings["gltf_nla_strips"] is True

                # Check if the animation is an NLA strip
                if export_animations:  
                    for track in material.animation_data.nla_tracks:
                        if track.mute is True:
                            continue

                        for strip in track.strips:
                            if strip.mute is True:
                                continue

                            if strip.action:
                                return True, strip.action.name

        return False, ''

    @staticmethod
    def add_placeholder_channel(blender_object: bpy.types.Object, export_settings):
        has_material_action, material_action_name = AsoboPropertyAnimation.has_material_action(blender_object, export_settings)
        if not has_material_action:
            # If we actually find a property besides the material animations, we don't need a temp fcurve
            return None, None

        # Create temp action and insert fake keyframes
        if blender_object.animation_data.action is None:
            temp_action = bpy.data.actions.new(name="placeHolderAction")
            blender_object.animation_data_create().action = temp_action
        else:
            temp_action = blender_object.animation_data.action

        if len(temp_action.fcurves) == 0:
            fcurve = temp_action.fcurves.new(data_path="scale")
            fcurve.keyframe_points.insert(bpy.context.scene.frame_start, 1)
            fcurve.keyframe_points.insert(bpy.context.scene.frame_end, 1)

        if bpy.app.version < (3, 6, 0):
            export_nla_animations = export_settings["gltf_nla_strips"] is True
        else:
            export_nla_animations = (export_settings["gltf_animation_mode"] == 'NLA_TRACKS')

        if export_nla_animations: 
            if blender_object.animation_data is None:
                blender_object.animation_data.new()
            if len(blender_object.animation_data.nla_tracks) == 0:
                track = blender_object.animation_data.nla_tracks.new()
                track.name = temp_action.name
                track.mute = False
                track.strips.new(name = temp_action.name, start = bpy.context.scene.frame_start, action = temp_action)

        return temp_action.name, material_action_name

    @staticmethod
    def clean_placeholder_actions(actionstoclean_objects_map):
        for action_name, blender_object in actionstoclean_objects_map.items():
            AsoboPropertyAnimation.clean_placeholder_action(action_name, blender_object)
            
    @staticmethod
    def clean_placeholder_action(action_name, blender_object):
        if blender_object.animation_data is not None and len(blender_object.animation_data.nla_tracks) > 0:
            if action_name in blender_object.animation_data.nla_tracks:
                track = blender_object.animation_data.nla_tracks[action_name]

                if len(track.strips) > 0 and action_name in track.strips:
                    strip = track.strips[action_name]
                    track.strips.remove(strip)

                blender_object.animation_data.nla_tracks.remove(track)

        if action_name in bpy.data.actions:
            bpy.data.actions.remove(bpy.data.actions[action_name])

    @staticmethod 
    def gather_material_animations(blender_object: bpy.types.Object, gathered_material_actions: set, export_settings) -> typing.Dict[str, AsoboMaterialAnimation]:
        material_actions_map = AsoboPropertyAnimation.gather_material_actions(blender_object, gathered_material_actions, export_settings)

        # Save gathered material action names 
        for material_actions in material_actions_map.values():
            gathered_material_actions.update({material_action.name for material_action in material_actions})

        material_animations = {}
        # Sample material actions
        for material, blender_actions in material_actions_map.items():
            for blender_action in blender_actions:
                animation = AsoboPropertyAnimation.gather_material_sampled_animation(material, blender_action, export_settings)
                animation.name = blender_action.name
                material_animations[blender_action.name] = animation

        return material_animations

    @staticmethod
    def gather_material_actions(blender_object: bpy.types.Object, gathered_material_actions: typing.List[bpy.types.Action], export_settings):
        """
        Args:
            blender_object (bpy.types.Object): _description_
            gathered_material_actions (typing.List[bpy.types.Action]): _description_
            export_settings (_type_): _description_

        Returns:
            typing.dict[bpy.types.Material, typing.List[bpy.types.Action]]: Map for all material -> actions
        """
        if bpy.app.version > (3, 6, 0):
            export_animations = (export_settings["gltf_animation_mode"] == 'NLA_TRACKS') or (export_settings['gltf_animation_mode'] == "ACTIONS")
        else:
            export_animations = export_settings["gltf_nla_strips"] is True

        if not export_animations:
            return {}

        if not (
            blender_object.type == "MESH"
            and blender_object.data is not None
            and len(blender_object.material_slots) > 0
        ):
            return {}

        material_actions_map = {}
        # Get a list of all material animation actions and NLA tracks (if used)
        for material_slot in blender_object.material_slots:
            material = material_slot.material
            
            blender_actions = []
            if material.animation_data is not None:

                # Get action if exists in material and not already gathered
                if material.animation_data.action is not None and material.animation_data.action.name not in gathered_material_actions:
                    blender_actions.append(material.animation_data.action)

                # Get action if exists in material nla tracks and not already gathered
                for nla_track in material.animation_data.nla_tracks:
                    if nla_track.mute == True or nla_track.strips is None:
                        continue

                    for strip in nla_track.strips:
                        if strip.mute == True:
                            continue

                        if strip.action is not None and strip.action.name not in gathered_material_actions:
                            blender_actions.append(strip.action)

            if len(blender_actions) > 0:
                material_actions_map[material] = blender_actions

        return material_actions_map

    @staticmethod
    def gather_material_sampled_animation(material, blender_action, export_settings):
        return AsoboPropertyAnimation.gather_animation_fcurves(material, blender_action, export_settings)
    
    @staticmethod
    def gather_animation_fcurves(material, blender_action, export_settings):
        return AsoboPropertyAnimation.gather_channels_fcurves(material, blender_action, export_settings)

    @staticmethod
    def gather_channels_fcurves(material, blender_action, export_settings):
        channels_map = {}
        for fcurve in blender_action.fcurves:
            if len(fcurve.keyframe_points) == 0:
                continue

            channel = AsoboChannel(
                fcurve = fcurve,
                data_path = material.name + '.' + fcurve.data_path,
                array_index = fcurve.array_index,
                target_property = fcurve.data_path,
                material_name = material.name,
                sampler = None
            )
            
            if fcurve.data_path not in channels_map:
                channels_map[fcurve.data_path] = []

            channels_map[fcurve.data_path].append(channel)

        channels = []
        for channels in channels_map.values():
            frames = AsoboPropertyAnimation.gather_fcurve_keyframes(channels, export_settings)
            input, output = AsoboPropertyAnimation.convert_keyframes(frames, export_settings)

            sampler = gltf2_io.AnimationSampler(
                extensions=None,
                extras=None,
                input=input,
                interpolation="LINEAR", # we'll keep linear for this ones
                output=output
            )
            channels[0].sampler = sampler

        animation = AsoboMaterialAnimation(
            channels = [channels[0] for channels in channels_map.values()]
        )

        return animation

    @staticmethod
    def gather_fcurve_keyframes(channels, export_settings):
        keyframes = []
        frame_key_map = {}
        for channel in channels:
            # Just use the keyframes as they are specified in blender
            frames = [keyframe.co[0] for keyframe in channel.fcurve.keyframe_points]

            # Some weird files have duplicate frame at same time, removed them
            frames = sorted(set(frames))

            if bpy.app.version >= (3, 6, 0):
                if export_settings['gltf_negative_frames'] == "CROP":
                    frames = [f for f in frames if f >= 0]

                if export_settings['gltf_frame_range'] is True:
                    frames = [f for f in frames if f >= bpy.context.scene.frame_start and f <= bpy.context.scene.frame_end]

            if len(frames) == 0:
                return None

            for frame in frames:
                key = Keyframe(channels, frame)
                key.value = channel.fcurve.evaluate(frame)
                if frame not in frame_key_map:
                    frame_key_map[frame] = []

                frame_key_map[frame].append(key)

        for frame, keys in frame_key_map.items():
            key = Keyframe()
            key.fps = keys[0].fps
            key.frame = frame
            key.seconds = keys[0].seconds
            key.target = keys[0].target
            key.value = [k.value for k in keys]

            keyframes.append(key)
            
        return keyframes
    
    @staticmethod
    def convert_keyframes(keyframes, export_settings):
        times = [k.seconds for k in keyframes]

        input = gltf2_blender_gather_accessors.gather_accessor(
            gltf2_io_binary_data.BinaryData.from_list(times, gltf2_io_constants.ComponentType.Float),
            gltf2_io_constants.ComponentType.Float,
            len(times),
            tuple([max(times)]),
            tuple([min(times)]),
            gltf2_io_constants.DataType.Scalar,
            export_settings)

        values = []
        for keyframe in keyframes:
            keyframe_value = gltf2_blender_math.mathutils_to_gltf(keyframe.value)
            values += keyframe_value

        # Store the keyframe data in a binary buffer
        component_type = gltf2_io_constants.ComponentType.Float
        data_type = gltf2_io_constants.DataType.vec_type_from_num(len(keyframes[0].value))

        output = gltf2_io.Accessor(
            buffer_view=gltf2_io_binary_data.BinaryData.from_list(values, component_type),
            byte_offset=None,
            component_type=component_type,
            count=len(values) // gltf2_io_constants.DataType.num_elements(data_type),
            extensions=None,
            extras=None,
            max=None,
            min=None,
            name=None,
            normalized=None,
            sparse=None,
            type=data_type
        )

        return input, output

    @staticmethod
    def finalize_material_animations(gltf2_plan, material_animations, place_holder_action_names):
        for animation in gltf2_plan.animations:
            if animation.name in place_holder_action_names:
                material_action_name = place_holder_action_names[animation.name]
                material_animation = material_animations[material_action_name]
                AsoboPropertyAnimation.finalize_material_animation(animation, material_animation, gltf2_plan)
                animation.name = material_action_name

    @staticmethod
    def finalize_material_animation(gltf2_animation, material_animation, gltf2_plan = None):
        sampler_index = len(gltf2_animation.samplers) + 1

        if not gltf2_animation.extensions:
            gltf2_animation.extensions = {}

        if (AsoboPropertyAnimation.extension_name not in gltf2_animation.extensions.keys()):
            gltf2_animation.extensions[AsoboPropertyAnimation.extension_name] = {"channels": []}

        if gltf2_plan is not None and AsoboPropertyAnimation.extension_name not in gltf2_plan.extensions_used:
            gltf2_plan.extensions_used.append(AsoboPropertyAnimation.extension_name)

        extension = gltf2_animation.extensions[AsoboPropertyAnimation.extension_name]
        for i, material_channel in enumerate(material_animation.channels):
            if (len(extension["channels"]) - 1  < i):
                extension["channels"].insert(i, {})
            channel = extension["channels"][i]

            #region Samplers
            if material_channel.sampler not in gltf2_animation.samplers:
                gltf2_animation.samplers.insert(sampler_index, material_channel.sampler)
                channel["sampler"] = sampler_index
                sampler_index += 1

            if gltf2_plan is None:
                continue
            #endregion

            #region Targets
            material_index = None
            for j, material in enumerate(gltf2_plan.materials):
                if material.name == material_channel.material_name:
                    material_index = j
                    break

            if material_index is None:
                continue

            target_property = material_channel.target_property

            if target_property == MSFS2024_MaterialProperties.baseColor.attributeName():
                channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/baseColorFactor"
            elif target_property == MSFS2024_MaterialProperties.emissiveColor.attributeName():
                channel["target"] = f"materials/{material_index}/emissiveFactor"
            elif target_property == MSFS2024_MaterialProperties.metallicScale.attributeName():
                channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/metallicFactor"
            elif target_property == MSFS2024_MaterialProperties.roughnessScale.attributeName():
                channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/roughnessFactor"

            elif target_property == MSFS2024_MaterialProperties.uvOffsetU.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialUVOptionsExtension.ExtensionName}/UVOffsetU"
            elif target_property == MSFS2024_MaterialProperties.uvOffsetV.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialUVOptionsExtension.ExtensionName}/UVOffsetV"
            elif target_property == MSFS2024_MaterialProperties.uvTilingU.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialUVOptionsExtension.ExtensionName}/UVTilingU"
            elif target_property == MSFS2024_MaterialProperties.uvTilingV.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialUVOptionsExtension.ExtensionName}/UVTilingV"
            elif target_property == MSFS2024_MaterialProperties.uvRotation.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialUVOptionsExtension.ExtensionName}/UVRotation"

            elif target_property == MSFS2024_MaterialProperties.windshieldWiper1State.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialWindshieldExtension.ExtensionName}/wiper1State"

            elif target_property == MSFS2024_MaterialProperties.wearAmount.attributeName():
                channel["target"] = f"materials/{material_index}/extensions/{AsoboMaterialDirtExtension.ExtensionName}/dirtBlendAmount"

            ## TODO - Add tireMudAnimState and tireDustAnimState
            ## f"materials/{material_index}/extensions/{AsoboMaterialTireExtension.ExtensionName}/tireMudAnimState"
            ## f"materials/{material_index}/extensions/{AsoboMaterialTireExtension.ExtensionName}/tireDustAnimState"

            #endregion
        