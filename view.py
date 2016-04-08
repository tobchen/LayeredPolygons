__author__ = 'tobchen'

from tkinter import Canvas, ALL, NW
from model import ImageLayer


class LayPolyCanvas(Canvas):
    def __init__(self, master=None, cnf={}, **kw):
        # TODO Get good at Python, correctly subclass Canvas
        # Canvas.__init__(self, master, cnf, kw)
        Canvas.__init__(self, master, cnf)

        self._polygons = list()

    def notify_layer_change(self, layer: ImageLayer):
        self.delete(ALL)
        self._polygons.clear()

        if not layer:
            return

        (x, y) = layer.get_coords()
        image = layer.get_image()
        self.create_image(x, y, image=image, anchor=NW)

        for i in range(0, layer.get_polygon_count()):
            coords = layer.get_polygon_at(i)
            polygon = self.create_polygon(coords, fill="red")
            self._polygons.append(polygon)

    def notify_polygon_change(self, layer: ImageLayer, index: int):
        try:
            self._polygons[index].coords =\
                layer.get_polygon_at(index).get_vertex_coords_list()
        except (ValueError, IndexError):
            pass

    def window_to_canvas_coords(self, x: int, y: int) -> (int, int):
        return int(self.canvasx(x)), int(self.canvasy(y))
