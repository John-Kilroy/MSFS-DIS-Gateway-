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
    def remove_color_attribute(gltf2_mesh, blender_mesh):
        if not MSFS2024_MeshUtils.is_color_attribute_uniform_white(blender_mesh):
            return
        
        for primitive in gltf2_mesh.primitives:
            newAttributes = dict()
            for attributeName, attribute in primitive.attributes.items():
                if not attributeName.startswith('COLOR'):
                    newAttributes[attributeName] = attribute
            primitive.attributes = newAttributes

    @staticmethod
    def is_color_attribute_uniform_white(blender_mesh):
        """
        Checks if the render active color attribute in the specified mesh object 
        is uniformly white.
        
        Parameters:
        - blender_mesh: The Blender mesh to check.

        Returns:
        - True if the render active color attribute is uniformly white, False otherwise.
        """
        if blender_mesh.attributes is None:
            return False

        render_color_index = blender_mesh.attributes.render_color_index

        if render_color_index == -1:
            return False

        if render_color_index >= len(blender_mesh.color_attributes):
            return False
        
        render_active_attr = blender_mesh.color_attributes[render_color_index]
        color_data = render_active_attr.data

        white_color = (1.0, 1.0, 1.0, 1.0)  
        if all(color.color[:] == white_color for color in color_data):
            return True
