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

class MSFS2024ImageFlagsEnum(Enum):
    """
        Enum describing the parameters of image contains Tuples of:
        ( 
            The name that appears in the UI, 
            Default Value, 
            attribute name of the property, 
            name that appear in the flags when it's exported/imported
        )
    """

    ## Parameters
    QUALITYHIGH = "Quality High", False, "msfs_image_quality_high", "+QUALITYHIGH"
    ALPHAPRESERVATION = "Alpha Preservation", False, "msfs_image_alpha_preserv", "+ALPHAPRESERVATION"
    NOREDUCTION = "No Reduction", False, "msfs_image_no_reduction", "+NOREDUCE"
    NOMIPMAP = "No Mipmap", False, "msfs_image_no_mipmap", "+NOMIPMAP",
    PRECOMPUTEDINVAVG = "PreComputed Inverse Average", False, "msfs_image_prec_inv_avg", "+PRECOMPUTEDINVAVG"
    ANISOTROPIC = "ANISOTROPIC", None, "msfs_image_anisotropic", "+ANISOTROPIC="

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

    def flagName(self):
        assert type(self.value) is tuple and len(self.value) > 3
        if type(self.value) is tuple and len(self.value) > 3:
            return self.value[3]
        return None

class MSFS2024ImageFlags(bpy.types.PropertyGroup):
    msfs_image_quality_high: bpy.props.BoolProperty(
        name = MSFS2024ImageFlagsEnum.QUALITYHIGH.name(),
        default = MSFS2024ImageFlagsEnum.QUALITYHIGH.defaultValue()
    )

    msfs_image_alpha_preserv: bpy.props.BoolProperty(
        name = MSFS2024ImageFlagsEnum.ALPHAPRESERVATION.name(),
        default = MSFS2024ImageFlagsEnum.ALPHAPRESERVATION.defaultValue()
    )

    msfs_image_no_reduction: bpy.props.BoolProperty(
        name = MSFS2024ImageFlagsEnum.NOREDUCTION.name(),
        default = MSFS2024ImageFlagsEnum.NOREDUCTION.defaultValue()
    )

    msfs_image_no_mipmap: bpy.props.BoolProperty(
        name = MSFS2024ImageFlagsEnum.NOMIPMAP.name(),
        default = MSFS2024ImageFlagsEnum.NOMIPMAP.defaultValue()
    )

    msfs_image_prec_inv_avg: bpy.props.BoolProperty(
        name = MSFS2024ImageFlagsEnum.PRECOMPUTEDINVAVG.name(),
        default = MSFS2024ImageFlagsEnum.PRECOMPUTEDINVAVG.defaultValue()
    )

    msfs_image_ANISOTROPIC: bpy.props.EnumProperty(
        name = MSFS2024ImageFlagsEnum.ANISOTROPIC.name(),
        items = (
            ("NONE", "Disabled", ""),
            ("0", "x0 (Standard)", ""),
            ("2", "x2 (High)", ""),
            ("4", "x4 (Very High)", ""),
            ("8", "x8 (Extreme)", ""),
            ("16", "x16 (Insane)", "")
        )
    )

    def to_string(self):
        result = ""
        result += MSFS2024ImageFlagsEnum.QUALITYHIGH.flagName() if self.msfs_image_quality_high else ""
        result += MSFS2024ImageFlagsEnum.ALPHAPRESERVATION.flagName() if self.msfs_image_alpha_preserv else ""
        result += MSFS2024ImageFlagsEnum.NOREDUCTION.flagName() if self.msfs_image_no_reduction else ""
        result += MSFS2024ImageFlagsEnum.NOMIPMAP.flagName() if self.msfs_image_no_mipmap else ""
        result += MSFS2024ImageFlagsEnum.PRECOMPUTEDINVAVG.flagName() if self.msfs_image_prec_inv_avg else ""
        result += MSFS2024ImageFlagsEnum.ANISOTROPIC.flagName() +  self.msfs_image_ANISOTROPIC if self.msfs_image_ANISOTROPIC != "NONE" else ""
        return result

class MSFS2024_OT_GenerateXML(bpy.types.Operator): # TODO
    bl_idname = "msfs2024.generate_texture_xml"
    bl_label = "Generate Texture XML"

    def execute(self, context):
        # TODO
        image = context.edit_image
        if image is None:
            self.report({"ERROR"}, f"Something went wrong image is None.")
            return {"CANCELLED"}

        if image.users < 1:
            self.report({"INFO"}, f"Image {image.name} is not used in scene.")
            return {"CANCELLED"}

        map_users = bpy.data.user_map(subset=[image])
        set_users = [user for user in map_users.values()]
        users = [user.pop() for user in set_users]
        used_materials = [user for user in users if type(user) is bpy.types.Material]
        
        return {"FINISHED"}

class MSFS2024_PT_ImageProperties(bpy.types.Panel):
    bl_label = "MSFS2024 Image Flags"
    bl_idname = "IMAGE_PT_msfs2024_image_properties"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "MSFS2024"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.edit_image is not None
    
    def draw(self, context):
        image = context.edit_image
        flags = image.msfs_flags

        layout = self.layout
        box = layout.box()

        row = box.row()
        row.prop(flags, MSFS2024ImageFlagsEnum.QUALITYHIGH.attributeName())
        row = box.row()
        row.prop(flags, MSFS2024ImageFlagsEnum.ALPHAPRESERVATION.attributeName())
        row = box.row()
        row.prop(flags, MSFS2024ImageFlagsEnum.NOREDUCTION.attributeName())
        row = box.row()
        row.prop(flags, MSFS2024ImageFlagsEnum.NOMIPMAP.attributeName())
        row = box.row()
        row.prop(flags, MSFS2024ImageFlagsEnum.PRECOMPUTEDINVAVG.attributeName())
        row = box.row()
        row.prop(flags, MSFS2024ImageFlagsEnum.ANISOTROPIC.attributeName())

        row = layout.row()
        # row.operator(MSFS2024_OT_GenerateXML.bl_idname)
        return

def register():
    bpy.types.Image.msfs_flags = bpy.props.PointerProperty(name="Flags", type=MSFS2024ImageFlags)
