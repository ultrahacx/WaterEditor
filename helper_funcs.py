import bpy


def create_quad(name, verts, faces, material, parentObj, edges=None):
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)

    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    mesh.from_pydata(verts, edges, faces)
    obj.data.materials.append(material)
    obj.parent = parentObj
    return obj


def create_materials(mat_name, color):
    mat = (bpy.data.materials.get(mat_name) or
           bpy.data.materials.new(mat_name))
    mat.use_nodes = True

    mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Principled BSDF'))
    material_output = mat.node_tree.nodes.get('Material Output')
    diffuse = mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')

    diffuse.inputs['Color'].default_value = color

    mat.node_tree.links.new(material_output.inputs[0], diffuse.outputs[0])
    return mat


def quad_min_max(quad_obj):
    all_vert = []
    for vert in quad_obj.data.vertices:
        coord = vert.co
        all_vert.append([coord.x, coord.y])

    min_xy = min(all_vert, key=lambda x: (x[0], x[1]))
    max_xy = max(all_vert, key=lambda x: (x[0], x[1]))

    return (min_xy, max_xy)


def round_to_even(value):
    return round(value / 2) * 2
