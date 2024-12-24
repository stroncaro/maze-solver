from tkinter import Tk, BOTH, Canvas
from typing import Literal


class Window:
    def __init__(self, width: int, height: int):
        root = Tk()
        root.title = "Maze Solver"
        root.protocol("WM_DELETE_WINDOW", self.close)
        canvas = Canvas(root, width=width, height=height)
        canvas.pack()
        self._root = root
        self._canvas = canvas
        self._running = False

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()

    def close(self):
        self._running = False

    def draw_line(
        self,
        line: "Line",
        fill_color: Literal["black"] | Literal["red"] | Literal["gray"],
    ):
        line.draw(self._canvas, fill_color)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(
        self,
        canvas: Canvas,
        fill_color: Literal["black"] | Literal["red"] | Literal["gray"],
    ):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
