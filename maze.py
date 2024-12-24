import random
import time
from typing import List, Optional, Any

from cell import Cell
from graphics import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Optional[Window] = None,
        seed: Optional[int | float | str] = None,
    ):
        if seed is not None:
            random.seed(seed)

        self._win = win
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells: List[List[Cell]] = [
            [Cell(self._win) for _ in range(self._num_rows)]
            for _ in range(self._num_cols)
        ]
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        x1 = self._x1 + self._cell_size_x * i
        y1 = self._y1 + self._cell_size_y * j
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i: int, j: int):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        coordinates = {
            "S": (i, j + 1),
            "E": (i + 1, j),
            "N": (i, j - 1),
            "W": (i - 1, j),
        }

        while True:
            target_directions = []
            for direction, (neighbour_i, neighbour_j) in coordinates.items():
                if not (
                    0 <= neighbour_i < self._num_cols
                    and 0 <= neighbour_j < self._num_rows
                ):
                    continue
                neighbour = self._cells[neighbour_i][neighbour_j]
                if not neighbour.visited:
                    target_directions.append(direction)

            if len(target_directions) == 0:
                break

            direction = random.choice(target_directions)
            target_directions.remove(direction)

            target_i, target_j = coordinates[direction]
            target = self._cells[target_i][target_j]
            match direction:
                case "S":
                    current_cell.has_bottom_wall = False
                    target.has_top_wall = False
                case "E":
                    current_cell.has_right_wall = False
                    target.has_left_wall = False
                case "N":
                    current_cell.has_top_wall = False
                    target.has_bottom_wall = False
                case "W":
                    current_cell.has_left_wall = False
                    target.has_right_wall = False

            self._break_walls_r(target_i, target_j)

        self._draw_cell(i, j)

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int):
        cell = self._cells[i][j]
        cell.visited = True

        # reached end cell?
        if cell == self._cells[-1][-1]:
            return True

        coordinates = {
            "S": (i, j + 1),
            "E": (i + 1, j),
            "N": (i, j - 1),
            "W": (i - 1, j),
        }

        for direction, (n_i, n_j) in coordinates.items():
            # check direction is valid
            match direction:
                case "S":
                    if cell.has_bottom_wall:
                        continue
                case "E":
                    if cell.has_right_wall:
                        continue
                case "N":
                    if cell.has_top_wall:
                        continue
                case "W":
                    if cell.has_left_wall:
                        continue

            # check neighbour is within bounds
            if not (0 <= n_i < self._num_cols and 0 <= n_j < self._num_rows):
                continue

            # traverse
            target = self._cells[n_i][n_j]
            if not target.visited:
                cell.draw_move(target)
                self._animate()

                found_exit = self._solve_r(n_i, n_j)
                if found_exit:
                    return True

                target.draw_move(cell, undo=True)
                self._animate()
        return False
