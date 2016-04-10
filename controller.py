__author__ = 'tobchen'

from tkinter import Tk, Menu, filedialog, PanedWindow, Listbox, Frame, Canvas,\
    Scrollbar
from tkinter import BOTH, SINGLE, HORIZONTAL, BOTTOM, X, VERTICAL, RIGHT, Y,\
    LEFT, ALL, NW, RAISED
from model import Scene, Vertex, Polygon
from view import LayPolyCanvas
import ora
import obj
import lp


class Controller:
    SNAP_RADIUS = 5

    def __init__(self, tk: Tk):
        tk.title("Layered Polygons")

        menubar = Menu(tk)

        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="New...", command=self._new_scene)
        menu_file.add_command(label="Open...")
        menu_file.add_separator()
        menu_file.add_command(label="Save", command=self._save_scene)
        menu_file.add_command(label="Save As...", command=self._save_scene_as)
        menu_file.add_separator()
        menu_export = Menu(menu_file, tearoff=0)
        menu_export.add_command(label="Wavefront (.obj)...",
                                command=self._export_obj)
        menu_file.add_cascade(label="Export", menu=menu_export)
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
        self._canvas.bind("<Button-3>", self._canvas_right_click)
        self._canvas.bind("<Motion>", self._canvas_mouse_moved)
        self._layer_list.bind("<<ListboxSelect>>", self._layer_change)

        self._current_path = None

    def _canvas_left_click(self, event):
        if not self._scene or not self._current_layer:
            return
        x, y = self._canvas.window_to_canvas_coords(event.x, event.y)

        if self._is_drawing_polygon:
            polygon = self._current_layer.get_polygon_at(-1)

            # Move vtx away from mouse to not interfere with search for closest
            polygon.get_vertex_at(-1).\
                set_coords(x-self.SNAP_RADIUS, y-self.SNAP_RADIUS)

            closest_vertex = self._current_layer.get_closest_vertex(
                x, y, self.SNAP_RADIUS)

            if closest_vertex:
                polygon.remove_vertex_at(-1)
                if closest_vertex is polygon.get_vertex_at(0):
                    self._is_drawing_polygon = False
                else:
                    polygon.add_vertex(closest_vertex)
                    polygon.add_vertex(Vertex(x, y))
            else:
                polygon.get_vertex_at(-1)\
                    .set_coords(x, y)
                polygon.add_vertex(Vertex(x, y))

            self._canvas.notify_polygon_change(self._current_layer
                                               .get_polygon_count()-1)
        else:
            # Create start vertex or use already existing one
            start_vertex = self._current_layer\
                .get_closest_vertex(x, y, self.SNAP_RADIUS)
            if not start_vertex:
                start_vertex = Vertex(x, y)

            # Vertex for mouse cursor
            next_vertex = Vertex(x, y)

            self._current_layer.add_polygon(
                Polygon([start_vertex, next_vertex]))

            self._is_drawing_polygon = True

            self._canvas.notify_layer_change()

    def _canvas_right_click(self, event):
        if not self._current_layer:
            return

        if self._is_drawing_polygon:
            self._current_layer.remove_polygon_at(-1)
            self._is_drawing_polygon = False
        else:
            # TODO Delete polygon
            pass

        self._canvas.notify_layer_change()

    def _canvas_mouse_moved(self, event):
        if self._is_drawing_polygon:
            x, y = self._canvas.window_to_canvas_coords(event.x, event.y)
            self._current_layer.get_polygon_at(-1).get_vertex_at(-1)\
                .set_coords(x, y)
            self._canvas.notify_polygon_change(self._current_layer
                                               .get_polygon_count()-1)

    def _layer_change(self, event):
        selection = self._layer_list.curselection()
        if len(selection) > 0 and self._scene:
            layer = self._scene.get_layer_at(selection[0])
            if layer:
                self._is_drawing_polygon = False
                self._current_layer = layer
                self._canvas.notify_new_layer(self._current_layer)

    def _set_scene(self, scene: Scene):
        if scene.get_layer_count() <= 0:
            # TODO Error popup
            return

        self._scene = scene

        # Prepare canvas
        # TODO Extra 10px padding for canvas
        width, height = self._scene.get_size()
        self._canvas.config(scrollregion=(0, 0, width, height))

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
        self._current_path = None

    def _open_scene(self):
        pass

    def _save_scene(self):
        if not self._current_path:
            self._save_scene_as()
            return
        lp.save(self._current_path, self._scene)

    def _save_scene_as(self):
        if not self._scene:
            return
        path = filedialog.asksaveasfilename(defaultextension=".lp",
                                            filetypes=[("Layered polygons"
                                                        " files", ".lp")])
        if path:
            self._current_path = path
            self._save_scene()

    def _export_obj(self):
        if not self._scene:
            return

        path_obj = filedialog.asksaveasfilename(defaultextension=".obj",
                                                filetypes=[("Wavefront object"
                                                            " files",
                                                            ".obj")])
        if not path_obj:
            return
        path_obj, path_mtl, path_data = obj.get_paths(path_obj)
        obj.save(path_obj, path_mtl, path_data, self._scene)

    def _quit_app(self):
        self._tk.quit()
        exit()
