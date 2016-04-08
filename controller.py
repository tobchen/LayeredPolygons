__author__ = 'tobchen'

from tkinter import Tk, Menu, filedialog, PanedWindow, Listbox, Frame, Canvas,\
    Scrollbar
from tkinter import BOTH, SINGLE, HORIZONTAL, BOTTOM, X, VERTICAL, RIGHT, Y,\
    LEFT, ALL, NW, RAISED
from model import Scene
from view import LayPolyCanvas
import ora


class Controller:
    SNAP_RADIUS = 5

    def __init__(self, tk: Tk):
        tk.title("Layered Polygons")

        menubar = Menu(tk)

        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="New...", command=self._new_scene)
        menu_file.add_command(label="Open...")
        menu_file.add_separator()
        menu_file.add_command(label="Save")
        menu_file.add_command(label="Save As...")
        menu_file.add_separator()
        menu_file.add_command(label="Export As...")
        menu_file.add_separator()
        menu_file.add_command(label="Quit", command=self._quit_app)
        menubar.add_cascade(label="File", menu=menu_file)

        tk.config(menu=menubar)

        paned = PanedWindow(tk, relief=RAISED)
        paned.pack(fill=BOTH, expand=1)

        frame = Frame(paned)
        paned.add(frame)
        self._canvas = LayPolyCanvas(frame)
        bar_x = Scrollbar(frame, orient=HORIZONTAL)
        bar_x.pack(side=BOTTOM, fill=X)
        bar_x.config(command=self._canvas.xview)
        bar_y = Scrollbar(frame, orient=VERTICAL)
        bar_y.pack(side=RIGHT, fill=Y)
        bar_y.config(command=self._canvas.yview)
        self._canvas.config(xscrollcommand=bar_x.set, yscrollcommand=bar_y.set)
        self._canvas.pack(side=LEFT, expand=True, fill=BOTH)
        # Thanks to the two guys on Stack Overflow for that!
        # ( http://stackoverflow.com/a/7734187 )

        self._layer_list = Listbox(paned, selectmode=SINGLE)
        paned.add(self._layer_list)

        self._scene = None
        self._current_layer = None
        self._is_drawing_polygon = False
        self._tk = tk

        self._canvas.bind("<Button-1>", self._canvas_left_click)
        self._layer_list.bind("<<ListboxSelect>>", self._layer_change)

    def _canvas_left_click(self, event):
        if not self._scene or not self._current_layer:
            return
        x, y = self._canvas.window_to_canvas_coords(event.x, event.y)

        if self._is_drawing_polygon:
            polygon = self._current_layer.get_polygon_at(
                self._current_layer.get_polygon_count()-1)

            # TODO Use -1 as list index for last (when get_vertex_at rewritten)
            # Move vtx away from mouse to not interfere with search for closest
            polygon.get_vertex_at(polygon.get_vertex_count()-1).\
                set_coords(x-self.SNAP_RADIUS, y-self.SNAP_RADIUS)

            closest_vertex = self._current_layer.get_closest_vertex(
                x, y, self.SNAP_RADIUS)

            if closest_vertex:
                pass
            else:
                pass
        else:
            pass

    def _layer_change(self, event):
        selection = self._layer_list.curselection()
        if len(selection) > 0 and self._scene:
            layer = self._scene.get_layer_at(selection[0])
            if layer:
                self._current_layer = layer
                self._canvas.notify_layer_change(self._current_layer)

    def _set_scene(self, scene: Scene):
        if scene.get_layer_count() <= 0:
            # TODO Error popup
            return

        self._scene = scene

        # Prepare canvas
        self._canvas.config(scrollregion=(0, 0, self._scene.get_width(),
                                          self._scene.get_height()))

        # Empty listbox, fill it, select first entry
        self._layer_list.delete(0, self._layer_list.size()-1)
        for i in range(0, self._scene.get_layer_count()):
            self._layer_list.insert(i, self._scene.get_layer_at(i).get_name())
        self._layer_list.selection_set(0)
        self._layer_list.event_generate("<<ListboxSelect>>")

    def _new_scene(self):
        path = filedialog.askopenfilename(defaultextension=".ora",
                                          filetypes=[("OpenRaster files",
                                                      ".ora")])
        if not path:
            return

        scene = ora.read(path)
        if not scene:
            # TODO Error popup
            return

        self._set_scene(scene)

    def _quit_app(self):
        self._tk.quit()
        exit()
