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

from math import radians

import bmesh
import bpy
import gpu
import numpy as np
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix

if bpy.app.version < (3, 6, 0):
    import bgl

class MSFS2024GizmoProperties():

    def msfs_gizmo_type_update(self, context):
        empties = MSFS2024CollisionGizmoGroup.empties
        object = context.object
        if object not in empties.keys():
            return

        if object.msfs_gizmo_type != empties[object].msfs_gizmo_type:
            empties[object].msfs_gizmo_type = object.msfs_gizmo_type
            empties[object].create_custom_shape()

    bpy.types.Object.msfs_gizmo_type = bpy.props.EnumProperty(
        name = "Type",
        description = "Type of collision gizmo to add",
        items = (("NONE", "Disabled", ""),
                ("sphere", "Sphere Collision Gizmo", ""),
                ("box", "Box Collision Gizmo", ""),
                ("cylinder", "Cylinder Collision Gizmo", ""),
                ("boundingSphere", "Skin Bounding Volume Gizmo", "")
        ),
        update=msfs_gizmo_type_update
    )

class MSFS2024AddGizmo(bpy.types.Operator):
    bl_idname = "msfs2024.add_gizmo"
    bl_label = "Add MSFS2024 Collision Gizmo"
    bl_options = {"REGISTER", "UNDO"}

    msfs_gizmo_type: bpy.types.Object.msfs_gizmo_type

    def add_gizmo(self, context, parent=None):
        bpy.ops.object.empty_add()
        gizmo = context.object
        if self.msfs_gizmo_type == "sphere":
            gizmo.name = "MSFS2024 Sphere Collision"
        elif self.msfs_gizmo_type == "box":
            gizmo.name = "MSFS2024 Box Collision"
        elif self.msfs_gizmo_type == "cylinder":
            gizmo.name = "MSFS2024 Cylinder Collision"
        elif self.msfs_gizmo_type == "boundingSphere":
            gizmo.name = "MSFS2024 Skin Bounding Volume"

        gizmo.msfs_gizmo_type = self.msfs_gizmo_type
        if parent and parent.type == "MESH":
            gizmo.parent = parent

    def execute(self, context):
        self.add_gizmo(context, context.active_object)
        return {"FINISHED"}

class MSFS2024CollisionGizmo(bpy.types.Gizmo):
    bl_idname = "VIEW3D_GT_msfs2024_collision_gizmo"
    bl_label = "MSFS2024 Collision Gizmo"
    bl_options = {"UNDO"}

    def draw_line_3d(self, color, width, region, pos):
        shader = gpu.shader.from_builtin('3D_POLYLINE_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": pos})
        shader.bind()
        shader.uniform_float("color", color)
        shader.uniform_float("lineWidth", width)
        shader.uniform_float("viewportSize", (region.width, region.height))
        batch.draw(shader)

    def create_custom_shape(self):
        mesh = bpy.data.meshes.new("Gizmo Mesh")
        bm = bmesh.new()
        if self.msfs_gizmo_type == "sphere":
            bmesh.ops.create_circle(bm, segments=32, radius=1)
            bm.to_mesh(mesh)
            bmesh.ops.create_circle(bm, segments=32, radius=1, matrix=Matrix.Rotation(radians(90), 4, 'X'))
            bm.to_mesh(mesh)
            bmesh.ops.create_circle(bm, segments=32, radius=1, matrix=Matrix.Rotation(radians(90), 4, 'Y'))
            bm.to_mesh(mesh)
        elif self.msfs_gizmo_type == "box":
            bmesh.ops.create_cube(bm, size=2)
        elif self.msfs_gizmo_type == "cylinder":
            bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=1, radius2=1, depth=2) # Create cone with both ends having the same diameter - this creates a cylinder
        elif self.msfs_gizmo_type == "boundingSphere":
            bmesh.ops.create_circle(bm, segments=32, radius=1)
            bm.to_mesh(mesh)
            bmesh.ops.create_circle(bm, segments=32, radius=1, matrix=Matrix.Rotation(radians(90), 4, 'X'))
            bm.to_mesh(mesh)
            bmesh.ops.create_circle(bm, segments=32, radius=1, matrix=Matrix.Rotation(radians(90), 4, 'Y'))
            bm.to_mesh(mesh)

        bm.to_mesh(mesh)
        bm.free()

        edges = []
        for edge in mesh.edges:
            edge_verts = []
            for vert in edge.vertices:
                edge_verts.append(mesh.vertices[vert])
            edges.append(edge_verts)

        self.custom_shape_edges = edges

    def draw(self, context):
        if not self.empty:
            return

        if self.empty.hide_get():
            return

        if not self.custom_shape_edges:
            return

        if bpy.app.version < (3, 6, 0):
            bgl.glEnable(bgl.GL_BLEND)
            bgl.glEnable(bgl.GL_LINE_SMOOTH)
            bgl.glEnable(bgl.GL_DEPTH_TEST)

        # Use Blender theme colors to keep everything consistent
        draw_color = list(context.preferences.themes[0].view_3d.empty)
        draw_color.append(1) # Add alpha (there isn't any functions in the Color class to add an alpha, so we have to convert to a list)

        vertex_pos = []
        for edge in self.custom_shape_edges:
            line_start = self.apply_vert_transforms(edge[0], matrix=self.empty.matrix_world)
            line_end = self.apply_vert_transforms(edge[1], matrix=self.empty.matrix_world)
            vertex_pos.extend([line_start, line_end])

        self.draw_line_3d(draw_color, 2, context.region, vertex_pos)

        if bpy.app.version < (3, 6, 0):
            # Restore OpenGL defaults
            bgl.glLineWidth(1)
            bgl.glDisable(bgl.GL_BLEND)
            bgl.glDisable(bgl.GL_LINE_SMOOTH)

    def apply_vert_transforms(self, vert, matrix):
        vert = list(vert.co)
        vert.append(1)
        multiplied_matrix = np.array(matrix).dot(np.array(vert))
        return multiplied_matrix[:-1].tolist()

class MSFS2024CollisionGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "VIEW3D_GT_msfs2024_collision_gizmo_group"
    bl_label = "MSFS2024 Collision Gizmo Group"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {'3D', 'PERSISTENT', 'SHOW_MODAL_ALL', 'SELECT'}

    empties = {}

    @classmethod
    def poll(cls, context):
        for object in context.view_layer.objects:
            if object.type == 'EMPTY' and object.msfs_gizmo_type != "NONE":
                return True
        return False

    def setup(self, context):
        for object in context.view_layer.objects:
            if object.type != 'EMPTY':
                continue

            if object.msfs_gizmo_type == "NONE":
                continue

            if object in self.empties:
                continue

            gizmo = self.gizmos.new(MSFS2024CollisionGizmo.bl_idname)
            gizmo.msfs_gizmo_type = object.msfs_gizmo_type
            gizmo.empty = object
            gizmo.create_custom_shape()

            self.empties[object] = gizmo

    def refresh(self, context):
        # We have to get a list of gizmo empties in the scene first in order to avoid a crash due to referencing a removed object
        found_empties = []
        for object in context.view_layer.objects:
            if object.type == 'EMPTY' and object.msfs_gizmo_type != "NONE":
                found_empties.append(object)

        # Check if there are any new gizmo empties, and if so create new gizmo. We can't do this in the above loop due to the crash mentioned above
        for found_empty in found_empties:
            if found_empty not in self.empties:
                self.setup(context)
                continue

            try:
                gizmo = self.empties.pop(found_empty)
                self.gizmos.remove(gizmo)
            except KeyError as exception:
                print("There is no such key : " + exception.message)

class MSFS2024CollisionAddMenu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_msfs_collision2024_add_menu"
    bl_label = "Microsoft Flight Simulator 2024 Collisions"

    def draw(self, context):
        self.layout.operator(MSFS2024AddGizmo.bl_idname, text="Sphere Collision", icon="MESH_UVSPHERE").msfs_gizmo_type = "sphere"
        self.layout.operator(MSFS2024AddGizmo.bl_idname, text="Box Collision", icon="MESH_CUBE").msfs_gizmo_type = "box"
        self.layout.operator(MSFS2024AddGizmo.bl_idname, text="Cylinder Collision", icon="MESH_CYLINDER").msfs_gizmo_type = "cylinder"
        self.layout.operator(MSFS2024AddGizmo.bl_idname, text="Bounding Volume Sphere", icon="MESH_UVSPHERE").msfs_gizmo_type = "boundingSphere"

#####################################################
def draw_menu(self, context):
    self.layout.menu(menu=MSFS2024CollisionAddMenu.bl_idname, icon="SHADING_BBOX")

def register():
    bpy.types.VIEW3D_MT_add.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_add.remove(draw_menu)
