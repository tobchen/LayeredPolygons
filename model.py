__author__ = 'tobchen'

from PIL.ImageTk import PhotoImage


class Vertex:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y


class Polygon:
    def __init__(self):
        self._vertices = []


class ImageLayer:
    def __init__(self, name: str, x: int, y: int, image: PhotoImage):
        self._name = name
        self._x = x
        self._y = y
        self._image = image

        self._polygons = []

    def set_name(self, name:  str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_coords(self) -> (int, int):
        return self._x, self._y

    def get_image(self) -> PhotoImage:
        return self._image

class Scene:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        self._layers = []

    def add_layer(self, layer: ImageLayer):
        self._layers.append(layer)

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_layer_count(self) -> int:
        return len(self._layers)

    def get_layer_at(self, index: int) -> ImageLayer:
        if 0 <= index < len(self._layers):
            return self._layers[index]
        else:
            return None
