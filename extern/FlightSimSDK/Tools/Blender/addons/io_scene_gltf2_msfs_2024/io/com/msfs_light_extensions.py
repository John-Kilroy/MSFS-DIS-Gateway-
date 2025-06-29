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
import math

from mathutils import Quaternion

from .extensions.light.asobo_street_light import AsoboStreetLight
from .extensions.light.asobo_advanced_light import AsoboAdvancedLight
from .extensions.light.asobo_skyportal_light import AsoboSkyPortalLight

class MSFS2024_LightExtension:
    bl_options = {"UNDO"}

    extensions = [
        AsoboStreetLight,
        AsoboAdvancedLight,
        AsoboSkyPortalLight
    ]

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def getExtensionParameter(extension, prop, attribute):
        if attribute.extensionName() and extension.get(attribute.extensionName()) is not None:
            setattr(
                prop, 
                attribute.attributeName(), 
                extension.get(attribute.extensionName())
            )
        
        ## Special case for retro compatibility 
        if attribute.extensionName() == "has_simmetry" and extension.get("has_simmetry") is not None:
            setattr(
                prop, 
                attribute.attributeName(), 
                extension.get("has_simmetry")
            )

    @staticmethod
    def setExtensionParameter(extension, prop, attribute):
        if not attribute.extensionName():
            return
            
        extension[attribute.extensionName()] = getattr(prop, attribute.attributeName())

    @staticmethod
    def create(vnode, gltf_node):
        for extension in MSFS2024_LightExtension.extensions:
            extension.create(vnode, gltf_node)
        
    @staticmethod
    def removeLightObject(vnode, gltf2_node, blender_node):
        for extension in MSFS2024_LightExtension.extensions:
            extension.removeLightObject(vnode, gltf2_node, blender_node)

    @staticmethod
    def export(gltf2_object, blender_object):
        if blender_object.type != "LIGHT":
            return

        # start quick dirty fix to solve rotation problem 
        currentRotationQuat = Quaternion()
        if gltf2_object.rotation:
            currentRotationQuat = Quaternion(
                (
                    gltf2_object.rotation[3], 
                    gltf2_object.rotation[0], 
                    gltf2_object.rotation[1], 
                    gltf2_object.rotation[2]
                )
            )
        
        angle = math.radians(90.0 if bpy.app.version < (3, 2, 0) else 180)
        quat_a = Quaternion((1.0, 0.0, 0.0), angle)
        rotation =  currentRotationQuat @ quat_a
        gltf2_object.rotation = [
            rotation.x, 
            rotation.y, 
            rotation.z, 
            rotation.w
        ]

        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}

        for extension in MSFS2024_LightExtension.extensions:
            extension.export(gltf2_object, blender_object)