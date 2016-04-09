__author__ = 'tobchen'

from tkinter import Canvas, ALL, NW
from model import ImageLayer
from PIL.ImageTk import PhotoImage


class LayPolyCanvas(Canvas):
    def __init__(self, master=None, cnf=None, **kw):
        if not cnf:
            cnf = {}
        Canvas.__init__(self, master, cnf, **kw)

        self._polygons = list()
        self._layer = None
        self._image = None

    def notify_new_layer(self, layer: ImageLayer):
        del self._image
        self._layer = layer
        self._image = PhotoImage(layer.get_image())
        self.notify_layer_change()

    def notify_layer_change(self):
        self.delete(ALL)
        self._polygons.clear()

        if not self._layer:
            return

        (x, y) = self._layer.get_coords()
        self.create_image(x, y, image=self._image, anchor=NW)

        for i in range(0, self._layer.get_polygon_count()):
            coords = self._layer.get_polygon_at(i).get_vertex_coords_list()
            polygon = self.create_polygon(coords, fill="", outline="red")
            self._polygons.append(polygon)

    def notify_polygon_change(self, index: int):
        try:
            coords = self._layer.get_polygon_at(index).get_vertex_coords_list()
            self.delete(self._polygons[index])
            self._polygons[index] = self.create_polygon(coords, fill="",
                                                        outline="red")
        except (ValueError, IndexError):
            pass

    def window_to_canvas_coords(self, x: int, y: int) -> (int, int):
        return int(self.canvasx(x)), int(self.canvasy(y))
