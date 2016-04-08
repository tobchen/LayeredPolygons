__author__ = 'tobchen'

from tkinter import Canvas


class LayPolyCanvas(Canvas):
    def __init__(self, master=None, cnf={}, **kw):
        # TODO Get good at Python, correctly subclass Canvas
        # Canvas.__init__(self, master, cnf, kw)
        Canvas.__init__(self, master, cnf)
