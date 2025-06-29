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

from enum import Enum

from .....blender.utils.msfs_material_utils import MSFS2024_MaterialProperties, MSFS2024_MaterialTypes


class AsoboMaterialCode:

    ExtensionName = "ASOBO_material_code"

    class MaterialCode(Enum):
        Porthole = "Porthole"
        GeoDecalFrosted = "GeoDecalFrosted"
        Propeller = "Propeller"
        Tree = "Tree"
        Vegetation = "Vegetation"

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        extras = gltf2_material.extras
        if extras is None:
            return

        assert isinstance(extras, dict)
        extra = extras.get(AsoboMaterialCode.ExtensionName)
        if extra is None:
            return

        match extra:
            case AsoboMaterialCode.MaterialCode.Porthole.value:
                setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.porthole.value)
            case AsoboMaterialCode.MaterialCode.GeoDecalFrosted.value:
                setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.geoDecalFrosted.value)
            case AsoboMaterialCode.MaterialCode.Propeller.value:
                setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.propeller.value)
            case AsoboMaterialCode.MaterialCode.Tree.value:
                setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.tree.value)
            case AsoboMaterialCode.MaterialCode.Vegetation.value:
                setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.vegetation.value)
            

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = ""
        
        match getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()):
            case MSFS2024_MaterialTypes.porthole.value:
                result = AsoboMaterialCode.MaterialCode.Porthole.value
            case MSFS2024_MaterialTypes.geoDecalFrosted.value:
                result = AsoboMaterialCode.MaterialCode.GeoDecalFrosted.value
            case MSFS2024_MaterialTypes.propeller.value:
                result = AsoboMaterialCode.MaterialCode.Propeller.value
            case MSFS2024_MaterialTypes.tree.value:
                result = AsoboMaterialCode.MaterialCode.Tree.value
            case MSFS2024_MaterialTypes.vegetation.value:
                result = AsoboMaterialCode.MaterialCode.Vegetation.value

        if gltf2_material.extras is None:
            gltf2_material.extras = {}
        
        if result != "":
            gltf2_material.extras[AsoboMaterialCode.ExtensionName] = result