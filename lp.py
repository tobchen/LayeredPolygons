__author__ = 'tobchen'

from model import Scene
import tempfile
import json
import zipfile
import os


def _get_tempfile_name() -> str:
    file = tempfile.NamedTemporaryFile(delete=False)
    file.close()
    return file.name


def save(path: str, scene: Scene):
    # TODO First save to temp then move archive to specified path

    # Generate JSON
    json_scene = dict()
    json_scene["width"], json_scene["height"] = scene.get_size()
    json_scene["layers"] = list()
    for i in range(0, scene.get_layer_count()):
        layer = scene.get_layer_at(i)
        vertices = layer.get_vertex_list()

        json_layer = dict()
        json_layer["name"] = layer.get_name()
        json_layer["x"], json_layer["y"] = layer.get_coords()
        json_layer["image"] = str(i) + ".png"
        json_layer["vertices"] = list()
        for vertex in vertices:
            json_vertex = dict()
            json_vertex["x"], json_vertex["y"] = vertex.get_coords()
            json_layer["vertices"].append(json_vertex)
        json_layer["polygons"] = list()
        for j in range(0, layer.get_polygon_count()):
            polygon = layer.get_polygon_at(j)

            json_polygon = list()
            for k in range(0, polygon.get_vertex_count()):
                json_polygon.append(vertices.index(polygon.get_vertex_at(k)))
            json_layer["polygons"].append(json_polygon)
        json_scene["layers"].append(json_layer)

    # Archive
    zip_file = zipfile.ZipFile(path, 'w')

    # Save JSON
    temp_json = _get_tempfile_name()
    temp_json_file = open(temp_json, 'w')
    json.dump(json_scene, temp_json_file)
    temp_json_file.close()
    zip_file.write(temp_json, "data.json")
    os.remove(temp_json)

    # Save images
    for i in range(0, scene.get_layer_count()):
        image = scene.get_layer_at(i).get_image()
        temp_image = _get_tempfile_name()
        image.save(temp_image, "PNG")
        zip_file.write(temp_image, str(i) + ".png")
        os.remove(temp_image)

    # BAMM, done!
    zip_file.close()


def read(path: str) -> Scene:
    # TODO Yeah, obviously
    pass
