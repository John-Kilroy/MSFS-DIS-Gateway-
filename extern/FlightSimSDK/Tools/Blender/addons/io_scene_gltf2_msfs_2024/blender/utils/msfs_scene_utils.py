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

from .msfs_material_nodes_utils import MSFS2024_GroupNodes, MSFS2024_MaterialProperties
from ..material.msfs_material_properties_update import MSFS2024_MaterialPropUpdate

class MSFS2024_SceneUtils:
    def convertMaterialsToMSFS2024():
        #region Purge node groups
        groups = bpy.data.node_groups
        groupNames = [x.value for x in list(MSFS2024_GroupNodes)]
        for group in groups:
            if group.name in groupNames:
                bpy.data.node_groups.remove(group)
        #endregion

        #region Update shader materials
        for material in bpy.data.materials:
            if hasattr(material, MSFS2024_MaterialProperties.materialType.attributeName()):
                MSFS2024_MaterialPropUpdate.update_msfs_material_type(
                    material, 
                    bpy.context, 
                    rebuild_native_mat=False
                )
        #endregion
        return

    def convertLightsToMSFS2024():
        lightObjects = list(filter(lambda object: object.type == "LIGHT", bpy.data.objects))
        for lightObject in lightObjects:
            lightData = lightObject.data
            bpy.ops.msfs2024.add_light(name=lightObject.name, msfs_light_type="streetLight")

            newLightObject = bpy.context.object
            newLightObject.location = lightObject.location
            newLightObject.rotation_euler = lightObject.rotation_euler
            newLightObject.scale = lightObject.scale

            newLight = newLightObject.data
            newLight.type = lightData.type
            newLight.diffuse_factor = lightData.diffuse_factor
            newLight.specular_factor = lightData.specular_factor
            newLight.volume_factor = lightData.volume_factor
            if hasattr(lightData, 'shadow_soft_size'):
                newLight.shadow_soft_size = lightData.shadow_soft_size

            newLightProp = newLight.msfs_light_properties
            newLightProp.msfs_light_color = lightData.color
            newLightProp.msfs_light_intensity = lightData.energy

            if hasattr(lightObject, 'angle'):
                newLightProp.msfs_light_cone_angle = lightData.angle

            newLightProp.msfs_light_has_symmetry = lightObject.msfs_light_has_symmetry
            newLightProp.msfs_light_flash_frequency = lightObject.msfs_light_flash_frequency
            newLightProp.msfs_light_flash_duration = lightObject.msfs_light_flash_duration
            newLightProp.msfs_light_flash_phase = lightObject.msfs_light_flash_phase
            newLightProp.msfs_light_rotation_speed = lightObject.msfs_light_rotation_speed
            newLightProp.msfs_light_day_night_cycle = lightObject.msfs_light_day_night_cycle

            bpy.data.objects.remove(lightObject)
        return

    def convertSceneToMSFS2024():
        MSFS2024_SceneUtils.convertMaterialsToMSFS2024()
        MSFS2024_SceneUtils.convertLightsToMSFS2024()
        return True
