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
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

from .....blender.msfs_lights import MSFS2024LightPropertiesEnum

class AsoboStreetLight:
    bl_options = {"UNDO"}

    ExtensionName = "ASOBO_street_light"

    ExtensionParameters = [
        MSFS2024LightPropertiesEnum.lightIntensity,
        MSFS2024LightPropertiesEnum.lightDayNightCycle,
        MSFS2024LightPropertiesEnum.lightConeAngle,
        MSFS2024LightPropertiesEnum.hasLightSymmetry,
        MSFS2024LightPropertiesEnum.lightFlashFrequency,
        MSFS2024LightPropertiesEnum.lightFlashDuration,
        MSFS2024LightPropertiesEnum.lightFlashPhase,
        MSFS2024LightPropertiesEnum.lightRotationSpeed,
        MSFS2024LightPropertiesEnum.lightRotationPhase,
        MSFS2024LightPropertiesEnum.lightRotationPhase,
        MSFS2024LightPropertiesEnum.lightRandomPhase
    ]
    
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(vnode, gltf_node):
        from ...msfs_light_extensions import MSFS2024_LightExtension
        if gltf_node is None and not gltf_node.extensions:
            return

        extension = gltf_node.extensions.get(AsoboStreetLight.ExtensionName)
        if not extension:
            return

        bpy.ops.msfs2024.add_light(name = gltf_node.name, msfs_light_type="streetLight")
        blender_node = bpy.context.active_object

        if blender_node.type != "LIGHT":
            return

        # Set transform
        trans, rot, scale = vnode.trs()
        blender_node.location = trans
        blender_node.rotation_mode = 'QUATERNION'
        blender_node.rotation_quaternion = rot
        blender_node.scale = scale

        # Set MSFS2024 Parameters
        blender_light = blender_node.data
        properties = blender_light.msfs_light_properties

        for extensionParameter in AsoboStreetLight.ExtensionParameters:
            MSFS2024_LightExtension.getExtensionParameter(
                extension=extension,
                prop=properties,
                attribute=extensionParameter
            )

    @staticmethod
    def removeLightObject(vnode, gltf2_node, blender_node):
        if not gltf2_node:
            return
            
        if gltf2_node.extensions:
            extension = gltf2_node.extensions.get(AsoboStreetLight.ExtensionName)
            if extension:
                bpy.data.objects.remove(blender_node)
                vnode.blender_object = bpy.data.objects[gltf2_node.name]

    @staticmethod
    def export(gltf2_object, blender_object):
        from ...msfs_light_extensions import MSFS2024_LightExtension

        # First, clear all KHR_lights_punctual extensions from children.
        for child in gltf2_object.children:
            if type(child.extensions) is dict and ("KHR_lights_punctual" in child.extensions):
                child.extensions.pop("KHR_lights_punctual")
                
        if type(gltf2_object.extensions) is dict and ("KHR_lights_punctual" in gltf2_object.extensions):
            gltf2_object.extensions.pop("KHR_lights_punctual")

        extension = {}

        blender_light = blender_object.data
        if getattr(blender_light, MSFS2024LightPropertiesEnum.lightType.attributeName()) != "streetLight":
            return

        msfs_light_properties = blender_light.msfs_light_properties

        extension[MSFS2024LightPropertiesEnum.lightColor.extensionName()] = list(getattr(msfs_light_properties, MSFS2024LightPropertiesEnum.lightColor.attributeName()))
        
        for extensionParameter in AsoboStreetLight.ExtensionParameters:
            MSFS2024_LightExtension.setExtensionParameter(
                extension=extension,
                prop=msfs_light_properties,
                attribute=extensionParameter
            )

        gltf2_object.extensions[AsoboStreetLight.ExtensionName] = Extension(
            name=AsoboStreetLight.ExtensionName,
            extension=extension,
            required=False
        )