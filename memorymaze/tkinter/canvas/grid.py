import tkinter as tk

from memorymaze.animation import ANIMATION_CLEAR_DELAY
from memorymaze.animation import ANIMATION_DELAY
from memorymaze.keyutil import is_down
from memorymaze.keyutil import is_left
from memorymaze.keyutil import is_right
from memorymaze.keyutil import is_up
from memorymaze.result import SelectResult
from memorymaze.style import CORRECT_COLOR
from memorymaze.style import EMPTY_COLOR
from memorymaze.style import PATH_COLOR
from memorymaze.style import INCORRECT_COLOR
from memorymaze.style import OUTLINE_COLOR
from memorymaze.style import OUTLINE_WIDTH


class GridCanvas(tk.Canvas):
    """
    Tkinter canvas specifically for the grid.

    Arguments:
        memory_maze (:class:`~MemoryMaze`): Memory maze object for business
            logic.
        parent: Parent widget to pass to the :class:`~tk.Canvas` class.
    """

    def __init__(self, memory_maze, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._memory_maze = memory_maze
        self._showing_path = False

    def redraw(self):
        """
        Redraws the grid.
        """
        
        # Don't allow redrawing if the path is being animated
        if not self._showing_path:
            # Clear the canvas and start with a fresh slate
            self.delete(tk.ALL)

            tile_width, tile_height = self._tile_dimensions

            for i in range(self._grid_size):
                canvas_y0 = tile_height * i
                canvas_y1 = canvas_y0 + tile_height
                
                for j in range(self._grid_size):
                    canvas_x0 = tile_width * j
                    canvas_x1 = canvas_x0 + tile_width

                    self.create_rectangle(canvas_x0, canvas_y0, canvas_x1, canvas_y1,
                        fill=EMPTY_COLOR, outline=OUTLINE_COLOR, width=str(OUTLINE_WIDTH))

    def show_path(self):
        """
        Shows the correct path.
        """

        # Don't allow redraw or input while the path is being shown
        self._showing_path = True
        self._memory_maze.lock()

        # Start drawing first square
        self._wait_and_draw_next_square(0)

    def on_click(self, canvas_x, canvas_y):
        """
        Handles canvas click events.

        Arguments:
            canvas_x (int): Canvas X coordinate.
            canvas_y (int): Canvas Y coordinate.
        """

        x_grid, y_grid = self._to_grid_coords(canvas_x, canvas_y)

        # Don't allow input outside the grid
        if 0 <= x_grid < self._grid_size and 0 <= y_grid < self._grid_size:
            self.select(x_grid, y_grid)
    
    def on_key(self, key):
        """
        Handles keyboard events.

        Arguments:
            key (str): The key that was pressed.
        """

        result = self._memory_maze.grid.last_position
        if result is not None:
            px, py = result
            if is_up(key):
                self.select(px, py - 1)
            elif is_down(key):
                self.select(px, py + 1)
            elif is_left(key):
                self.select(px - 1, py)
            elif is_right(key):
                self.select(px + 1, py)

    def select(self, x, y):
        """
        Selects a position on the grid and returns the result.

        Arguments:
            x (int): Grid X coordinate.
            y (int): Grid Y coordinate.

        Returns:
            :class:`~SelectResult`
        """

        result = self._memory_maze.select(x, y)

        tile_width, tile_height = self._tile_dimensions
        canvas_x0, canvas_y0 = self._to_canvas_coords(x, y, tile_width, tile_height)
        canvas_x1, canvas_y1 = (canvas_x0 + tile_width, canvas_y0 + tile_height)

        if result == SelectResult.CORRECT:
            # Green square
            self.create_rectangle(canvas_x0, canvas_y0, canvas_x1, canvas_y1,
                fill=CORRECT_COLOR, outline=OUTLINE_COLOR, width=str(OUTLINE_WIDTH))
            
            return result
        if result == SelectResult.COMPLETE:
            # Success! Show path for next level
            self._redraw_and_show_path()
            return result
        if result in (SelectResult.INCORRECT, SelectResult.GAME_OVER):
            # Red square
            self.create_rectangle(canvas_x0, canvas_y0, canvas_x1, canvas_y1,
                fill=INCORRECT_COLOR, outline=OUTLINE_COLOR, width=str(OUTLINE_WIDTH))
            
            # Don't allow input after an incorrect square is clicked
            self._memory_maze.lock()

            if result == SelectResult.INCORRECT:
                # Show path again after incorrect guess
                # Show guess was wrong for a beat before redrawing path
                self.after(ANIMATION_DELAY, lambda: self._redraw_and_show_path())
        
        return result

    def _wait_and_draw_next_square(self, idx):
        """
        Recursively draws the next square in the path after a specified delay
        until all path squares are shown.

        Arguments:
            idx: Current index of the path we are drawing.
        """

        x, y = self._memory_maze.grid.path[idx]

        tile_width, tile_height = self._tile_dimensions

        canvas_x0, canvas_y0 = self._to_canvas_coords(x, y, tile_width, tile_height)
        canvas_x1, canvas_y1 = (canvas_x0 + tile_width, canvas_y0 + tile_height)

        # Draw next path space
        self.create_rectangle(canvas_x0, canvas_y0, canvas_x1, canvas_y1,
            fill=PATH_COLOR, outline=OUTLINE_COLOR, width=str(OUTLINE_WIDTH))

        if idx < self._memory_maze.game_state.path_size - 1:
            # Wait and show next square after a delay
            self.after(ANIMATION_DELAY, lambda: self._wait_and_draw_next_square(idx + 1))
        else:
            # Completed path shown, clear after extended delay
            self.after(ANIMATION_CLEAR_DELAY, lambda: self._on_show_path_complete())

    def _on_show_path_complete(self):
        """
        Called when the path drawing is complete.
        """

        # Path showing complete, allow input
        self._showing_path = False
        self._memory_maze.unlock()

        # Redraw grid without completed path
        self.redraw()

    def _redraw_and_show_path(self):
        """
        Convenience method for redrawing the grid and showing the path.
        """

        self.redraw()

        # Wait a beat before showing first square
        self.after(ANIMATION_DELAY, lambda: self.show_path())

    def _to_grid_coords(self, canvas_x, canvas_y):
        """
        Converts canvas coordinates to grid coordinates.

        Arguments:
            canvas_x (int): Canvas X coordinate.
            canvas_y (int): Canvas Y coordinate.

        Returns:
            tuple: Grid coordinates.
        """

        tile_width, tile_height = self._tile_dimensions

        grid_x = canvas_x // tile_width
        grid_y = canvas_y // tile_height

        return grid_x, grid_y

    def _to_canvas_coords(self, grid_x, grid_y, tile_width, tile_height):
        """
        Converts grid coordinates to canvas coordinates.

        Arguments:
            grid_x (int): Grid X coordinate.
            grid_y (int): Grid Y coordinate.
            tile_width (int): Width of each tile.
            tile_height (int): Height of each tile.

        Returns:
            tuple: Canvas coordinates.
        """

        canvas_x = grid_x * tile_width
        canvas_y = grid_y * tile_height
        
        return canvas_x, canvas_y

    @property
    def _tile_dimensions(self):
        """
        Returns the desired dimension of the tiles based on the canvas and grid
        size.

        Returns:
            tuple: Desired tile width and height.
        """

        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        tile_width = canvas_width // self._grid_size
        tile_height = canvas_height // self._grid_size

        return tile_width, tile_height

    @property
    def _grid_size(self):
        """
        Convenience method for getting the grid size from the game state.

        Returns:
            int
        """

        return self._memory_maze.game_state.grid_size
