from graphics import Window
from maze import Maze


if __name__ == "__main__":
    win_width = 800
    win_height = 600
    win = Window(win_width, win_height)

    padding = 50
    cell_size = 25
    num_rows = (win_height - padding * 2) // cell_size
    num_cols = (win_width - padding * 2) // cell_size
    maze = Maze(padding, padding, num_rows, num_cols, cell_size, cell_size, win)

    solved = maze.solve()
    print("Maze solved!" if solved else "Not solved :(")
    win.wait_for_close()
