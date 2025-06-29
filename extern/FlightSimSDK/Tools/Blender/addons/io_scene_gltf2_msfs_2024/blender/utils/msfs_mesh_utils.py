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

class MSFS2024_MeshUtils:

    @staticmethod
    def add_default_vcolor(mesh):
        """
        Add a white color attribute.
        """
        if mesh.data.color_attributes:
            return

        mesh.data.color_attributes.new(
            name="Color",
            type='FLOAT_COLOR',
            domain='CORNER',
        )
        return