from typing import Optional

from graphics import Window, Line, Point


class Cell:
    def __init__(self, window: Optional[Window] = None):
        self.has_top_wall: bool = True
        self.has_right_wall: bool = True
        self.has_bottom_wall: bool = True
        self.has_left_wall: bool = True
        self._win: Window = window

        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1: int = x1
        self._x2: int = x2
        self._y1: int = y1
        self._y2: int = y2

        color = "black" if self.has_top_wall else "#d9d9d9"
        self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), color)

        color = "black" if self.has_right_wall else "#d9d9d9"
        self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), color)

        color = "black" if self.has_bottom_wall else "#d9d9d9"
        self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), color)

        color = "black" if self.has_left_wall else "#d9d9d9"
        self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), color)

    def draw_move(self, to_cell: "Cell", undo=False):
        if self._win is None:
            return
        x1 = (self._x1 + self._x2) // 2
        y1 = (self._y1 + self._y2) // 2
        x2 = (to_cell._x1 + to_cell._x2) // 2
        y2 = (to_cell._y1 + to_cell._y2) // 2
        line = Line(Point(x1, y1), Point(x2, y2))
        color = "gray" if undo else "red"
        self._win.draw_line(line, color)
