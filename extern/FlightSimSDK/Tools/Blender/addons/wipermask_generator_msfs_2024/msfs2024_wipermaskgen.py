import bpy
import bmesh
import os


def remove_object(object):
    data = object.data

    bpy.data.objects.remove(object)

    if data is not None:
        bpy.data.meshes.remove(data)

##########################################################################################
def createProjectedMesh(configuration, frame_start = 0, frame_end = 0):
    name = "NewWiperMaskObject"

    # create the mesh data
    mesh_data = bpy.data.meshes.new(f"{name}_data")

    # create the mesh object using the mesh data
    mesh_obj = bpy.data.objects.new(name, mesh_data)

    # add the mesh object into the scene
    bpy.context.scene.collection.objects.link(mesh_obj)

    # create a new bmesh
    bm = bmesh.new()

    boundaries_vertices_indexes = []
    vertices = []
    j = 0
    for i in range(frame_start, frame_end):
        bpy.context.scene.frame_set(i)
        vertices.append(configuration.wiper_point_a.matrix_world.to_translation())
        j += 1
        vertices.append(configuration.wiper_point_b.matrix_world.to_translation())
        j += 1

        if i != frame_start and i != frame_end - 1:
            boundaries_vertices_indexes.append(j - 1)
            boundaries_vertices_indexes.append(j - 2)


    # create and add a vertices
    for vertice in vertices:
        bm.verts.new(vertice)
    
    face_vert_indices = []
    # create a list of vertex indices that are part of a given face
    for i in range(0, len(vertices) - 2, 2):
        face_vert_indices.append((i, i + 1, i + 3, i + 2))

    bm.verts.ensure_lookup_table()

    for vert_indices in face_vert_indices:
        bm.faces.new([bm.verts[index] for index in vert_indices])

    # writes the bmesh data into the mesh data
    bm.to_mesh(mesh_data)

    # [Optional] update the mesh data (helps with redrawing the mesh in the viewport)
    mesh_data.update()

    # clean up/free memory that was allocated for the bmesh
    bm.free()

    # Set auto_smooth on mesh
    mesh_data.use_auto_smooth = True

    # Create a vertex group containing all vertices but not boundaries
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = mesh_obj

    bpy.ops.object.vertex_group_add()
    vg = mesh_obj.vertex_groups.active
    vg.name = "all_without_boundaries"
    vg.add(index=boundaries_vertices_indexes, weight=1, type='REPLACE')

    return mesh_obj

##########################################################################################

def saturate(x):
        return max(0, min(1, x))

def remap(original_value, original_min, original_max, new_min, new_max):
    return new_min + (new_max - new_min) * saturate(float(float(original_value - original_min) / float(original_max - original_min)))

def getvColorByFrame(frame, frame_start, frame_end, border):
    vColor = [0, 0, 0, 1]     

    colorValue = remap(frame, frame_start, frame_end, 0, 255) / 255

    vColor[0] = colorValue
    vColor[1] = 1 - colorValue # invert r
    
    if border:
        vColor[2] = 0
    else:
        vColor[2] = 1

    return vColor      

def setVColors(mesh, frame_start, frame_end):
    mesh.sculpt_vertex_colors.new()

    vIndex = 0
    for i in range(frame_start, frame_end):
        color = getvColorByFrame(i, frame_start, frame_end, False)
        mesh.sculpt_vertex_colors[0].data[vIndex].color = color

        color = getvColorByFrame(i, frame_start, frame_end, True)
        mesh.sculpt_vertex_colors[0].data[vIndex + 1].color = color
        vIndex += 2

def subdivideWiperObject(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj

    # Add subdivision modifier
    modifier = obj.modifiers.new(type='SUBSURF', name='subdivide')
    modifier.subdivision_type = 'SIMPLE'
    modifier.levels = 3

    # Apply modifier
    bpy.ops.object.modifier_apply(modifier=modifier.name)

def smoothWiperObject(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj

    # Add subdivision modifier
    modifier = obj.modifiers.new(type='LAPLACIANSMOOTH', name='smooth')
    modifier.iterations = 4
    modifier.lambda_factor = 0
    modifier.lambda_border = 6
    modifier.vertex_group = obj.vertex_groups[0].name

    # Apply modifier
    bpy.ops.object.modifier_apply(modifier=modifier.name)

##########################################################################################

def prepareWiperMaterial(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj

    old_area = bpy.context.area.ui_type
    bpy.context.area.ui_type = "ShaderNodeTree"

    material_count = len(bpy.data.materials)
    bpy.ops.material.new()
    material = bpy.data.materials['Material']
    material.name = 'Material_%d' % material_count
    
    material.use_nodes = True
    obj.data.materials.append(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    vertexColorNode = nodes.new("ShaderNodeVertexColor")
    vertexColorNode.location = (-200, 200)
    vertexColorNode.layer_name = "Col"

    principled = nodes["Principled BSDF"]

    links.new(vertexColorNode.outputs[0], principled.inputs[0])

    bpy.context.area.ui_type = old_area

def prepareWindshieldMaterial(obj, img):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj

    if len(obj.data.materials) > 0:
        material = obj.active_material
        material.use_nodes = True

        nodes = material.node_tree.nodes

        if img.name in nodes:
            texture_node = nodes[img.name]
        else:
            texture_node = nodes.new(type="ShaderNodeTexImage")
        if img is not None:
            texture_node.name = img.name
            texture_node.image = img

def cleanWindshieldMaterial(obj, nodeName):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj

    if len(obj.data.materials) > 0:
        material = obj.active_material
        nodes = material.node_tree.nodes
        if nodes.find(nodeName) > -1:
            texture_node = nodes[nodeName]
            nodes.remove(texture_node)

##########################################################################################

def prepareOutputTexture(name='wiperMask', output_texture_size=2048, output_path=None):
    old_area = bpy.context.area.ui_type
    bpy.context.area.ui_type = "IMAGE_EDITOR"
    
    output_path = os.path.join(output_path, name + ".png")
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except Exception:
            print(f"File {output_path} is readonly.")
            

    if name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[name])

    bpy.ops.image.new(name=name, color=(0, 0, 0, 0), width=output_texture_size, height=output_texture_size)
    img = bpy.data.images[name]

    bpy.context.area.spaces.active.image = img
    bpy.ops.image.save_as(filepath=output_path)

    bpy.context.area.ui_type = old_area


##########################################################################################
def bakeTexture(start_time = 0, end_time = 0, configurations = None, output_texture_name = "", output_texture_size = 1024, output_path = ""):
    ## Set render engine to cycles
    old_engine = bpy.context.scene.render.engine
    bpy.context.scene.render.engine = 'CYCLES'

    ## Setup output path
    prepareOutputTexture(name=output_texture_name, output_texture_size=output_texture_size, output_path=output_path)

    ## Clear output texture
    output_texture = bpy.data.images[output_texture_name]
    output_texture.source = 'FILE'
    output_texture.colorspace_settings.name = 'Linear'

    wiperMaskObjects = []
    for configuration in configurations:
        ## Setup material for windshield node
        prepareWindshieldMaterial(configuration.windshield_object, output_texture)

        ## Create new object following the animation of the wipers 
        wiperMaskObject = createProjectedMesh(configuration, start_time, end_time)
        wiperMaskObjects.append(wiperMaskObject)
        
        ## Set Vertex Colors following the animation of the wipers 
        setVColors(wiperMaskObject.data, start_time, end_time)
        
        ## Smooth wiper object
        subdivideWiperObject(wiperMaskObject)
        smoothWiperObject(wiperMaskObject)

        ## Setup the material of the wiper object
        prepareWiperMaterial(wiperMaskObject)
        
        ## select wiperobject to windshield node
        bpy.ops.object.select_all(action="DESELECT")
        wiperMaskObject.select_set(True)
        configuration.windshield_object.select_set(True)

        ## Set windshield node as active object
        bpy.context.view_layer.objects.active = configuration.windshield_object

        ## Bake vcolors of wiperobject to windshield node
        bpy.ops.object.bake(
                        type='DIFFUSE',
                        pass_filter = {'COLOR'},
                        use_selected_to_active = True,
                        use_clear = False,
                        cage_extrusion = 0.1,
                        max_ray_distance = 0.5
        )

        ## Clean Windshild nodes material
        cleanWindshieldMaterial(configuration.windshield_object, output_texture_name)

    ## Save output texture
    old_area = bpy.context.area.ui_type
    bpy.context.area.ui_type = "IMAGE_EDITOR"
    bpy.context.area.spaces.active.image = output_texture
    bpy.ops.image.save()

    ## Restore context
    bpy.context.area.ui_type = old_area
    bpy.context.scene.render.engine = old_engine

    ## Clean generated wiper mask objects after bake
    for wiperMaskObject in wiperMaskObjects:
        remove_object(wiperMaskObject)

    return

