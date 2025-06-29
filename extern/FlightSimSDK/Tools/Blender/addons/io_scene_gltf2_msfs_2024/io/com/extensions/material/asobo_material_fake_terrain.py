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

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

from .....blender.utils.msfs_material_utils import (MSFS2024_MaterialProperties,
                                                  MSFS2024_MaterialTypes)


class AsoboMaterialFakeTerrainExtension:

    ExtensionName = "ASOBO_material_fake_terrain"

    @staticmethod
    def from_dict(blender_material, gltf2_material, import_settings):
        extensions = gltf2_material.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMaterialFakeTerrainExtension.ExtensionName)
        if extension is None:
            return

        setattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName(), MSFS2024_MaterialTypes.fakeTerrain.value)

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        
        if getattr(blender_material, MSFS2024_MaterialProperties.materialType.attributeName()) == MSFS2024_MaterialTypes.fakeTerrain.value:
            result["enabled"] = True

            gltf2_material.extensions[AsoboMaterialFakeTerrainExtension.ExtensionName] = Extension(
                name = AsoboMaterialFakeTerrainExtension.ExtensionName,
                extension = result,
                required = False,
            )

