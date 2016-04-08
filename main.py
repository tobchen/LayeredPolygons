__author__ = 'tobchen'

from tkinter import Tk
from controller import Controller


if __name__ == '__main__':
    tk = Tk()
    app = Controller(tk)
    tk.mainloop()
