__author__ = 'tobchen'

from PIL import Image
import math


class Vertex:
    def __init__(self, x: int, y: int):
        self._x = int(x)
        self._y = int(y)

    def set_coords(self, x: int, y: int):
        self._x = int(x)
        self._y = int(y)

    def get_coords(self) -> (int, int):
        return self._x, self._y


class Polygon:
    def __init__(self, vertices: list=None):
        self._vertices = list()
        if vertices:
            self._vertices.extend(vertices)

    def add_vertex(self, vertex: Vertex):
        self._vertices.append(vertex)

    def remove_vertex_at(self, index: int):
        try:
            del self._vertices[index]
        except IndexError:
            pass

    # TODO Implement
    def contains(self, x: int, y: int) -> bool:
        return False

    def get_vertex_coords_list(self) -> list:
        result = list()

        for vertex in self._vertices:
            result.extend(vertex.get_coords())

        return result

    def get_vertex_count(self) -> int:
        return len(self._vertices)

    def get_vertex_at(self, index: int) -> Vertex:
        try:
            return self._vertices[index]
        except IndexError:
            return None


class ImageLayer:
    def __init__(self, name: str, x: int, y: int, image: Image):
        self._name = str(name)
        self._x = int(x)
        self._y = int(y)
        self._image = image

        self._polygons = list()

    def set_name(self, name:  str):
        self._name = str(name)

    def add_polygon(self, polygon: Polygon):
        self._polygons.append(polygon)

    def remove_polygon_at(self, index: int):
        try:
            del self._polygons[index]
        except IndexError:
            pass

    def get_name(self) -> str:
        return self._name

    def get_coords(self) -> (int, int):
        return self._x, self._y

    def get_image(self) -> Image:
        return self._image

    def get_polygon_count(self) -> int:
        return len(self._polygons)

    def get_polygon_at(self, index: int) -> Polygon:
        try:
            return self._polygons[index]
        except IndexError:
            return None

    def get_closest_vertex(self, x: int, y: int, radius: int) -> Vertex:
        result = None
        result_distance = radius + 1

        for polygon in self._polygons:
            for i in range(0, polygon.get_vertex_count()):
                vertex = polygon.get_vertex_at(i)
                vert_x, vert_y = vertex.get_coords()
                vert_distance = math.hypot(x-vert_x, y-vert_y)

                if vert_distance <= radius and vert_distance < result_distance:
                    result = vertex
                    result_distance = vert_distance

        return result

    def get_vertex_list(self) -> list:
        vertices = list()
        for polygon in self._polygons:
            for k in range(0, polygon.get_vertex_count()):
                vertex = polygon.get_vertex_at(k)
                if vertex not in vertices:
                    vertices.append(vertex)
        return vertices


class Scene:
    def __init__(self, width: int, height: int):
        self._width = int(width)
        self._height = int(height)

        self._layers = list()

    def add_layer(self, layer: ImageLayer):
        self._layers.append(layer)

    def get_size(self) -> (int, int):
        return self._width, self._height

    def get_layer_count(self) -> int:
        return len(self._layers)

    def get_layer_at(self, index: int) -> ImageLayer:
        try:
            return self._layers[index]
        except IndexError:
            return None
