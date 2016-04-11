__author__ = 'tobchen'

from model import Scene, ImageLayer, Polygon, Vertex
import tempfile
import json
from zipfile import ZipFile
import os
from PIL import Image
from io import BytesIO


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
    zip_file = ZipFile(path, 'w')

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
    zipfile = ZipFile(path, 'r')

    # Read data
    data_file = zipfile.open('data.json', 'r')
    if not data_file:
        zipfile.close()
        return None
    json_scene = json.loads(data_file.read().decode("utf-8"))
    data_file.close()

    try:
        scene = Scene(json_scene["width"], json_scene["height"])
    except KeyError:
        zipfile.close()
        return None

    if "layers" in json_scene:
        for i in range(0, len(json_scene["layers"])):
            json_layer = json_scene["layers"][i]
            name = "Layer " + str(i)
            if "name" in json_layer:
                name = json_layer["name"]

            try:
                layer = ImageLayer(name, json_layer["x"], json_layer["y"],
                                   Image.open(BytesIO(zipfile.read(
                                       json_layer["image"]))))
            except KeyError:  # TODO Find out about image loading errors
                continue

            vertices = list()
            if "vertices" in json_layer:
                for json_vertex in json_layer["vertices"]:
                    try:
                        vertices.append(Vertex(json_vertex["x"],
                                               json_vertex["y"]))
                    except KeyError:
                        pass

            if "polygons" in json_layer:
                for json_polygon in json_layer["polygons"]:
                    polygon = Polygon()
                    for index in json_polygon:
                        polygon.add_vertex(vertices[index])
                    layer.add_polygon(polygon)

            scene.add_layer(layer)

    zipfile.close()

    return scene
