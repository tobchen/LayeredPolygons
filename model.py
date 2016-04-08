__author__ = 'tobchen'

from PIL.ImageTk import PhotoImage
import math.hypot


class Vertex:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def set_coords(self, x: int, y: int):
        self._x = x
        self._y = y

    def get_coords(self) -> (int, int):
        return self._x, self._y


class Polygon:
    def __init__(self):
        self._vertices = list()

    def get_vertex_coords_list(self) -> list:
        result = list()

        for vertex in self._vertices:
            result.extend(vertex.get_coords())

        return result

    def get_vertex_count(self) -> int:
        return len(self._vertices)

    # TODO Use exceptions
    def get_vertex_at(self, index: int) -> Vertex:
        if 0 <= index < len(self._vertices):
            return self._vertices[index]
        else:
            return None


class ImageLayer:
    def __init__(self, name: str, x: int, y: int, image: PhotoImage):
        self._name = name
        self._x = x
        self._y = y
        self._image = image

        self._polygons = list()

    def set_name(self, name:  str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_coords(self) -> (int, int):
        return self._x, self._y

    def get_image(self) -> PhotoImage:
        return self._image

    def get_polygon_count(self) -> int:
        return len(self._polygons)

    # TODO Use exceptions
    def get_polygon_at(self, index: int) -> Polygon:
        if 0 <= index < len(self._polygons):
            return self._polygons[index]
        else:
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


class Scene:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        self._layers = list()

    def add_layer(self, layer: ImageLayer):
        self._layers.append(layer)

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_layer_count(self) -> int:
        return len(self._layers)

    # TODO Use exceptions
    def get_layer_at(self, index: int) -> ImageLayer:
        if 0 <= index < len(self._layers):
            return self._layers[index]
        else:
            return None
