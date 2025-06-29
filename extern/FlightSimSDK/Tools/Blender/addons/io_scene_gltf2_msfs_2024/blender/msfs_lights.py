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

from enum import Enum

class MSFS2024LightPropertiesEnum(Enum):
    """
        Enum describing the parameters of lights contains Tuples of:
        ( 
            The name that appears in the UI, 
            Default Value, 
            attribute name of the property, 
            name that appear in the extension when it's exported/imported
        )
    """

    ## Parameters
    lightType = "Light Type", "NONE", "msfs_light_type", None
    lightColor = "Color", [1.0, 1.0, 1.0], "msfs_light_color", "color"
    lightIntensity = "Intensity (cd)", 1000.0, "msfs_light_intensity", "intensity"
    hasLightSymmetry = "Has symmetry", False, "msfs_light_has_symmetry", "has_symmetry"
    lightDayNightCycle = "Day/Night Cycle", False, "msfs_light_day_night_cycle", "day_night_cycle"
    lightFlashFrequency = "Frequency (1/min)", 0.0, "msfs_light_flash_frequency", "flash_frequency"
    lightFlashDuration = "Duration (s)", 0.2, "msfs_light_flash_duration", "flash_duration"
    lightFlashPhase = "Phase (s)", 0.0, "msfs_light_flash_phase", "flash_phase"
    lightRotationSpeed = "Rotation Speed (RPM)", 0.0, "msfs_light_rotation_speed", "rotation_speed"
    lightRotationPhase = "Rotation Phase", 0.0, "msfs_light_rotation_phase", "rotation_phase"
    lightRandomPhase = "Random Phase", True, "msfs_light_random_phase", "random_phase"
    lightConeAngle = "Cone Angle", 90.0, "msfs_light_cone_angle", "cone_angle"
    lightShape = "Shape", "point", "msfs_light_shape_type", "shape_type"
    lightSourceRadius = "Source Radius (cm)", 50.0, "msfs_light_source_radius", "source_radius"
    lightInnerAngle = "Inner Angle", 160.0, "msfs_light_inner_angle", "inner_cone_angle"
    lightOuterAngle = "Outer Angle", 160.0, "msfs_light_outer_angle", "outer_cone_angle"
    lightChannelExterior = "Exterior", True, "msfs_light_channel_exterior", "channel_exterior"
    lightChannelInterior = "Interior", True, "msfs_light_channel_interior", "channel_interior"

    def name(self):
        assert type(self.value) is tuple and len(self.value) > 0
        if type(self.value) is tuple and len(self.value) > 0:
            return self.value[0]
        return None

    def defaultValue(self):
        assert type(self.value) is tuple and len(self.value) > 1
        if type(self.value) is tuple and len(self.value) > 1:
            return self.value[1]
        return None

    def attributeName(self):
        assert type(self.value) is tuple and len(self.value) > 2
        if type(self.value) is tuple and len(self.value) > 2:
            return self.value[2]
        return None

    def extensionName(self):
        assert type(self.value) is tuple and len(self.value) > 3
        if type(self.value) is tuple and len(self.value) > 3:
            return self.value[3]
        return None

class MSFS2024LightProperties(bpy.types.PropertyGroup):

    bpy.types.Light.msfs_light_type = bpy.props.EnumProperty(
        name = "Type",
        description = "Type of light to add",
        items = (("NONE", "Disabled", ""),
                ("streetLight", "MSFS2024 Street Light", ""),
                ("advancedLight", "MSFS2024 Advanced Light", ""),
                ("skyPortalLight", "MSFS2024 Sky Portal Light", "")
        )
    )

    def get_active_light_data(self, context):
        active_object = context.active_object
        if active_object.type != "LIGHT":
            return None
        active_light = active_object.data
        if not active_light:
            return None
        return active_light

    def update_light_color(self, context):
        active_light = self.get_active_light_data(context)
        if active_light is not None:
            active_light.color = getattr(
                active_light.msfs_light_properties, 
                MSFS2024LightPropertiesEnum.lightColor.attributeName()
            )

    def update_light_intensity(self, context):
        active_light = self.get_active_light_data(context)
        if active_light is not None:
            active_light.energy = getattr(
                active_light.msfs_light_properties, 
                MSFS2024LightPropertiesEnum.lightIntensity.attributeName()
            )

    msfs_light_color: bpy.props.FloatVectorProperty(
        name = MSFS2024LightPropertiesEnum.lightColor.name(),
        default = MSFS2024LightPropertiesEnum.lightColor.defaultValue(),
        subtype = "COLOR",
        size = 3,
        update = update_light_color
    )

    msfs_light_intensity: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightIntensity.name(), 
        default = MSFS2024LightPropertiesEnum.lightIntensity.defaultValue(),
        update = update_light_intensity
    )

    msfs_light_has_symmetry: bpy.props.BoolProperty(
        name = MSFS2024LightPropertiesEnum.hasLightSymmetry.name(), 
        default = MSFS2024LightPropertiesEnum.hasLightSymmetry.defaultValue()
    )

    msfs_light_flash_frequency: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightFlashFrequency.name(), 
        default = MSFS2024LightPropertiesEnum.lightFlashFrequency.defaultValue(),
        min = 0.0
    )

    msfs_light_flash_duration: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightFlashDuration.name(),
        default = MSFS2024LightPropertiesEnum.lightFlashDuration.defaultValue(),
        min = 0.0 
    )

    msfs_light_flash_phase: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightFlashPhase.name(),
        default = MSFS2024LightPropertiesEnum.lightFlashPhase.defaultValue()
    )

    msfs_light_rotation_speed: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightRotationSpeed.name(),
        default = MSFS2024LightPropertiesEnum.lightRotationSpeed.defaultValue()
    )

    msfs_light_rotation_phase: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightRotationPhase.name(),
        default = MSFS2024LightPropertiesEnum.lightRotationPhase.defaultValue()
    )

    msfs_light_random_phase: bpy.props.BoolProperty(
        name = MSFS2024LightPropertiesEnum.lightRandomPhase.name(), 
        default = MSFS2024LightPropertiesEnum.lightRandomPhase.defaultValue()
    )

    msfs_light_day_night_cycle: bpy.props.BoolProperty(
        name = MSFS2024LightPropertiesEnum.lightDayNightCycle.name(), 
        default = MSFS2024LightPropertiesEnum.lightDayNightCycle.defaultValue(), 
        description = "Set this value to 'true' if you want the light to be visible at night only."
    )

    msfs_light_cone_angle: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightConeAngle.name(),
        default = MSFS2024LightPropertiesEnum.lightConeAngle.defaultValue(),
        description = "This value sets the cone angle of the light."
    )

    msfs_light_shape_type: bpy.props.EnumProperty(
        name = MSFS2024LightPropertiesEnum.lightShape.name(),
        description = "Shape of the light",
        items = (("point", "Point", ""),
                ("sphere", "Sphere", ""),
                ("disc", "Disc", "")
        ),
        default = MSFS2024LightPropertiesEnum.lightShape.defaultValue()
    )

    msfs_light_source_radius: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightSourceRadius.name(), 
        default = MSFS2024LightPropertiesEnum.lightSourceRadius.defaultValue(),
        min = 1.0, 
    )

    msfs_light_inner_angle: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightInnerAngle.name(),
        default = MSFS2024LightPropertiesEnum.lightInnerAngle.defaultValue(),
        min = 0.0
    )

    msfs_light_outer_angle: bpy.props.FloatProperty(
        name = MSFS2024LightPropertiesEnum.lightOuterAngle.name(),
        default = MSFS2024LightPropertiesEnum.lightOuterAngle.defaultValue(),
        min = 0.0
    )

    msfs_light_channel_exterior: bpy.props.BoolProperty(
        name = MSFS2024LightPropertiesEnum.lightChannelExterior.name(),
        default = MSFS2024LightPropertiesEnum.lightChannelExterior.defaultValue()
    )

    msfs_light_channel_interior: bpy.props.BoolProperty(
        name = MSFS2024LightPropertiesEnum.lightChannelInterior.name(),
        default = MSFS2024LightPropertiesEnum.lightChannelInterior.defaultValue()
    )

class MSFS2024AddLight(bpy.types.Operator):
    bl_idname = "msfs2024.add_light"
    bl_label = "Add MSFS2024 Light"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(default="Light")
    msfs_light_type: bpy.types.Light.msfs_light_type

    def add_light(self, context):
        bpy.ops.object.light_add(type='POINT')
        blender_object = context.active_object
        blender_object.name = self.name
        blender_light = blender_object.data
        blender_light.name = self.name
        blender_light.msfs_light_type = self.msfs_light_type
        blender_light.msfs_light_properties.msfs_light_intensity = MSFS2024LightPropertiesEnum.lightIntensity.defaultValue()

        if blender_light.msfs_light_type == "skyPortalLight":
            blender_light.msfs_light_properties.msfs_light_shape_type = "disc"
        return

    def execute(self, context):
        self.add_light(context)
        return {"FINISHED"}

class MSFS2024LightsAddMenu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_msfs_lights2024_add_menu"
    bl_label = "Microsoft Flight Simulator 2024 Lights"

    def draw(self, context):
        add_fast_light_op = self.layout.operator(MSFS2024AddLight.bl_idname, text="Fast Light", icon="LIGHT_POINT")
        add_fast_light_op.msfs_light_type = "streetLight"
        add_fast_light_op.name = "MSFS2024 Street Light"
        add_advanced_light_op = self.layout.operator(MSFS2024AddLight.bl_idname, text="Advanced Light", icon="LIGHT_POINT")
        add_advanced_light_op.msfs_light_type = "advancedLight"
        add_advanced_light_op.name = "MSFS2024 Advanced Light"
        add_skyportal_light_op = self.layout.operator(MSFS2024AddLight.bl_idname, text="Sky Portal Light", icon="LIGHT_POINT")
        add_skyportal_light_op.msfs_light_type = "skyPortalLight"
        add_skyportal_light_op.name = "MSFS2024 SkyPortal Light"

#####################################################
class MSFS2024_PT_LightProperties(bpy.types.Panel):
    bl_label = "MSFS2024 Light Parameters"
    bl_idname = "LIGHT_PT_msfs2024_light_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        isMSFSLight = False
        if context.active_object is not None and context.active_object.type == 'LIGHT':
            isMSFSLight = context.active_object.data.msfs_light_type != "NONE"
        return isMSFSLight

    def draw_fast_light_properties(self, context, prop, layout):
        layout.prop(prop, MSFS2024LightPropertiesEnum.lightColor.attributeName())

        box = layout.box()
        box.label(text = "Power")
        box.prop(prop, MSFS2024LightPropertiesEnum.lightIntensity.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightDayNightCycle.attributeName())

        box = layout.box()
        box.label(text = "Distribution")
        box.prop(prop, MSFS2024LightPropertiesEnum.lightConeAngle.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.hasLightSymmetry.attributeName())

        box = layout.box()
        box.label(text = "Animation")
        box.prop(prop, MSFS2024LightPropertiesEnum.lightFlashFrequency.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightFlashDuration.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightFlashPhase.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightRotationPhase.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightRotationPhase.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightRandomPhase.attributeName())
        return
    
    def draw_advanced_light_properties(self, context, prop, layout):
        layout.prop(prop, MSFS2024LightPropertiesEnum.lightColor.attributeName())

        box = layout.box()
        box.label(text = "Power")
        box.prop(prop, MSFS2024LightPropertiesEnum.lightIntensity.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightDayNightCycle.attributeName())

        box = layout.box()
        box.label(text = "Shape")
        box.prop(prop, MSFS2024LightPropertiesEnum.lightShape.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightSourceRadius.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightInnerAngle.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightOuterAngle.attributeName())

        box = layout.box()
        box.label(text = "Channels")
        box.prop(prop, MSFS2024LightPropertiesEnum.lightChannelExterior.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightChannelInterior.attributeName())
        return

    def draw_skyportal_light_properties(self, context, prop, layout):
        box = layout.box()
        box.label(text = "Shape")
        row = box.row()
        row.prop(prop, MSFS2024LightPropertiesEnum.lightShape.attributeName())
        row.enabled = False
        box.prop(prop, MSFS2024LightPropertiesEnum.lightSourceRadius.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightInnerAngle.attributeName())
        box.prop(prop, MSFS2024LightPropertiesEnum.lightOuterAngle.attributeName())
        return

    def draw(self, context):
        layout = self.layout
        active_object = context.object

        if active_object.type != 'LIGHT':
            return

        blender_light = active_object.data
        if blender_light is None:
            return

        prop = blender_light.msfs_light_properties
        if blender_light.msfs_light_type == "streetLight":
            self.draw_fast_light_properties(context, prop, layout)
        elif blender_light.msfs_light_type == "advancedLight":
            self.draw_advanced_light_properties(context, prop, layout)
        elif blender_light.msfs_light_type == "skyPortalLight":
            self.draw_skyportal_light_properties(context, prop, layout)
    
#####################################################
def draw_menu(self, context):
    self.layout.menu(menu=MSFS2024LightsAddMenu.bl_idname, icon="OUTLINER_DATA_LIGHT")

def register():
    bpy.types.VIEW3D_MT_add.append(draw_menu)
    
    bpy.types.Light.msfs_light_properties = bpy.props.PointerProperty(type=MSFS2024LightProperties)

def unregister():
    bpy.types.VIEW3D_MT_add.remove(draw_menu)