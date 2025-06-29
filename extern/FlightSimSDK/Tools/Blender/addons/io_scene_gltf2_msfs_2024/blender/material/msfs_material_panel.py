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

from ..utils.msfs_material_utils import (MSFS2024_MaterialProperties,
                                         MSFS2024_MaterialUtilsUI,
                                         MSFS2024_MaterialTypes)

from .msfs_material_anisotropic import MSFS2024_Anisotropic
from .msfs_material_clearcoat import MSFS2024_Clearcoat
from .msfs_material_environment_occluder import MSFS2024_Environment_Occluder
from .msfs_material_fake_terrain import MSFS2024_Fake_Terrain
from .msfs_material_fresnel_fade import MSFS2024_Fresnel_Fade
from .msfs_material_geo_decal import MSFS2024_Geo_Decal
from .msfs_material_geo_decal_blendmasked import MSFS2024_Geo_Decal_BlendMasked
from .msfs_material_geo_decal_frosted import MSFS2024_Geo_Decal_Frosted
from .msfs_material_ghost import MSFS2024_Ghost
from .msfs_material_glass import MSFS2024_Glass
from .msfs_material_hair import MSFS2024_Hair
from .msfs_material_invisible import MSFS2024_Invisible
from .msfs_material_parallax import MSFS2024_Parallax
from .msfs_material_porthole import MSFS2024_Porthole
from .msfs_material_propeller import MSFS2024_Propeller
from .msfs_material_sail import MSFS2024_Sail
from .msfs_material_sss import MSFS2024_SSS
from .msfs_material_standard import MSFS2024_Standard
from .msfs_material_tree import MSFS2024_Tree
from .msfs_material_vegetation import MSFS2024_Vegetation
from .msfs_material_windshield import MSFS2024_Windshield


class MSFS2024_PT_Material(bpy.types.Panel):
    bl_label = "MSFS2024 Material Parameters"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw(self, context):
        layout = self.layout
        material = context.active_object.active_material

        # If there is no active material we can cut the draw
        if not material:
            return

        ## Material Types
        MSFS2024_MaterialUtilsUI.draw_prop(
            layout = layout,
            material = material,
            property = MSFS2024_MaterialProperties.materialType.attributeName()
        )

        # If we don't have any material type set we can cut the draw
        if getattr(material, MSFS2024_MaterialProperties.materialType.attributeName()) == "NONE":
            return

        match getattr(material, MSFS2024_MaterialProperties.materialType.attributeName()):
            case MSFS2024_MaterialTypes.standard.value:
                MSFS2024_Standard.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.decal.value:
                MSFS2024_Geo_Decal.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.windshield.value:
                MSFS2024_Windshield.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.porthole.value:
                MSFS2024_Porthole.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.glass.value:
                MSFS2024_Glass.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.geoDecalFrosted.value:
                MSFS2024_Geo_Decal_Frosted.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.geoDecalBlendMasked.value:
                MSFS2024_Geo_Decal_BlendMasked.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.clearcoat.value:
                MSFS2024_Clearcoat.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.parallaxWindow.value:
                MSFS2024_Parallax.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.anisotripic.value:
                MSFS2024_Anisotropic.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.hair.value:
                MSFS2024_Hair.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.subSurfaceScattering.value:
                MSFS2024_SSS.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.invisible.value:
                MSFS2024_Invisible.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.fakeTerrain.value:
                MSFS2024_Fake_Terrain.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.fresnelFade.value:
                MSFS2024_Fresnel_Fade.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.environmentOccluder.value:
                MSFS2024_Environment_Occluder.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.ghost.value:
                MSFS2024_Ghost.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.sail.value:
                MSFS2024_Sail.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.propeller.value:
                MSFS2024_Propeller.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.tree.value:
                MSFS2024_Tree.drawPanel(layout = layout, material = material)
            case MSFS2024_MaterialTypes.vegetation.value:
                MSFS2024_Vegetation.drawPanel(layout = layout, material = material)
