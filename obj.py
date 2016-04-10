__author__ = 'tobchen'

from model import Scene
import os


def get_paths(path_obj: str) -> (str, str, str):
    if path_obj.lower()[-4:] != ".obj":
        path_obj += ".obj"
    path_mtl = path_obj[:-4] + ".mtl"
    path_data = path_obj[:-4] + "_data"
    return path_obj, path_mtl, path_data


def save(path_obj: str, path_mtl: str, path_data: str, scene: Scene,
         scale: float=0.01, z_distance: float=1.0):
    # TODO Keep files in temp and only after save move them to specified paths
    # TODO Save only relevant part of texture
    name = os.path.basename(path_obj)[:-4].replace(" ", "")
    scene_height = scene.get_size()[1]

    file_obj = open(path_obj, 'w')

    # Material file
    file_obj.write("mtllib " + os.path.relpath(path_mtl,
                                               os.path.dirname(path_obj))
                   + '\n\n')

    # Generate vertex list
    vertices = list()
    for i in range(0, scene.get_layer_count()):
        vertices.append(scene.get_layer_at(i).get_vertex_list())

    # Save vertex coordinates
    for i in range(0, scene.get_layer_count()):
        if len(vertices[i]) <= 0:
            continue
        file_obj.write("# " + scene.get_layer_at(i).get_name() + '\n')
        for vertex in vertices[i]:
            x, y = vertex.get_coords()
            y = scene_height - y
            file_obj.write("v " + str(x * scale) + " "
                           + str(y * scale)
                           + " " + str(-i * z_distance) + '\n')
    file_obj.write('\n')

    # Texture coordinates
    for i in range(0, scene.get_layer_count()):
        if len(vertices[i]) <= 0:
            continue
        layer = scene.get_layer_at(i)
        file_obj.write("# " + layer.get_name() + '\n')
        width, height = layer.get_image().size
        off_x, off_y = layer.get_coords()
        for vertex in vertices[i]:
            x, y = vertex.get_coords()
            x -= off_x
            y -= off_y
            file_obj.write("vt " + str(x / width) + " " + str(1.0 - y / height)
                           + '\n')
    file_obj.write('\n')

    # Faces
    index_offset = 0
    for i in range(0, scene.get_layer_count()):
        if len(vertices[i]) <= 0:
            continue
        layer = scene.get_layer_at(i)
        file_obj.write("# " + layer.get_name() + '\n')
        file_obj.write("usemtl mat_" + name + '_' + str(i) + '\n')
        for j in range(0, layer.get_polygon_count()):
            polygon = layer.get_polygon_at(j)
            face_line = 'f'
            for k in range(0, polygon.get_vertex_count()):
                index = index_offset\
                        + vertices[i].index(polygon.get_vertex_at(k))
                face_line += ' ' + str(index + 1) + '/' + str(index + 1)
            file_obj.write(face_line + '\n')
        index_offset += len(vertices[i])

    file_obj.close()

    file_mtl = open(path_mtl, 'w')

    # Materials
    for i in range(0, scene.get_layer_count()):
        if len(vertices[i]) <= 0:
            continue
        tex_path = os.path.join(path_data, "tex_" + name + '_' + str(i)
                                + ".png")
        tex_path_relative = os.path.relpath(tex_path, os.path.dirname(path_mtl))
        layer = scene.get_layer_at(i)
        file_mtl.write("# " + layer.get_name() + '\n')
        file_mtl.write("newmtl mat_" + name + '_' + str(i) + '\n')
        file_mtl.write("Ka 1.0 1.0 1.0\nKd 1.0 1.0 1.0\nKs 0.0 0.0 0.0\n")
        file_mtl.write("illum 1\n")
        # file_mtl.write("map_Kd " + tex_path_relative + '\n')
        file_mtl.write("map_Kd -clamp on " + tex_path_relative + '\n')
        if layer.get_image().mode.lower().find('a') >= 0:
            file_mtl.write("map_d -clamp on " + tex_path_relative + '\n')

    file_mtl.close()

    # Save textures
    for i in range(0, scene.get_layer_count()):
        if len(vertices[i]) <= 0:
            continue
        os.makedirs(path_data, exist_ok=True)
        scene.get_layer_at(i).get_image().save(os.path.join(path_data, "tex_"
                                                            + name + '_'
                                                            + str(i) + ".png"))
