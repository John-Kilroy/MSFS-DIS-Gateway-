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


class TextureConfig:
    """ 
        Simple structure:
            id: int, 
            bitmap_config: BitmapConfig
            blend_texture : bpy.types.Image 
    """
    def __init__(self, gltf_texture_id=-1, bitmap_config=None, blend_texture=None) -> None:
        self.gltf_texture_id = gltf_texture_id
        self.bitmap_config = bitmap_config
        self.blend_texture = blend_texture