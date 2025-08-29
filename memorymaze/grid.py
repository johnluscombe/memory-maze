import random

from memorymaze.result import SelectResult


class MemoryMazeGrid:
    """
    Class for encapsulating the state of the game grid and performing actions
    on it.
    """

    def __init__(self):
        self._path = None
        self._current_index = 0
    
    @property
    def path(self):
        """
        Returns the current path.

        Returns:
            list
        """
        
        return self._path
    
    def generate_path(self, path_length, grid_size):
        """
        Generates a path on the grid of the given length and grid size.

        Arguments:
            path_length (int): Desired length of the path.
            grid_size (int): Size of one dimension of the grid (ex. 5x5 => 5).
        """

        self._path = self._generate_path(path_length, grid_size, [])
        self._current_index = 0
        return self.path
    
    def select(self, x, y):
        """
        Selects a grid coordinate and returns the result of that action.
        If the user selects a square that is *not* adjacent to the previously
        selected square, None is returned.
        If the user selects an incorrect square, an INCORRECT result is
        returned.
        If the user selects a correct square, a CORRECT result is returned.
        If the user completes the grid, a COMPLETE result is returned.
        This class is not aware of game state so GAME_OVER result is never
        returned.

        Arguments:
            x (int): X grid coordinate.
            y (int): Y grid coordinate.

        Returns:
            :class:`~SelectResult`
        """

        if self._path[self._current_index] == (x, y):
            self._current_index += 1
            if self._current_index >= len(self._path):
                return SelectResult.COMPLETE
            return SelectResult.CORRECT
        
        if self._is_adjacent(x, y):
            self._current_index = 0
            return SelectResult.INCORRECT
        
        # Do not register clicks on squares that are not adjacent to the
        # previously selected square.
        return None
    
    def _is_adjacent(self, x, y):
        """
        Returns whether the given grid coordinates are adjacent to the
        previously selected square. Clicks on squares *not* adjacent to the
        previously selected square are ignored.

        Arguments:
            x (int): X grid coordinate.
            y (int): Y grid coordinate.

        Returns:
            bool
        """

        if self._current_index == 0:
            # We are on the first square, count any click on the bottom row
            # We do not have access to grid size in this class, but the first
            # square is guaranteed to have a Y coordinate of the bottom row
            return y == self._path[0][1]

        px, py = self._path[self._current_index - 1]
        return (x, y) in [(px-1, py), (px, py-1), (px+1, py)]
    
    def _generate_path(self, path_length, grid_size, current_path):
        """
        Recursively generates a path of the given length and grid size.

        Arguments:
            path_length (int): Desired length of the path.
            grid_size (int): Size of one dimension of the grid (ex. 5x5 => 5).
            current_path (list): The current generated path.
        
        Returns:
            list or None: list of successful path generation, None if path of
                given length not possible from current position.
        """

        # If we have generated a path of the desired length
        if len(current_path) == path_length:
            # If we are at the top
            if current_path[-1][1] == 0:
                # Success! Return the path
                return current_path
            else:
                # Not at the top, invalid path
                return None
        
        # If we are at the top and the path is too short
        if len(current_path) > 0 and current_path[-1][1] == 0:
            # Invalid path
            return None

        # If we are placing starter piece
        if len(current_path) == 0:
            # Choose random X
            x = random.randint(0, grid_size - 1)
            # Start at bottom
            y = grid_size - 1

            current_path = [(x, y)]
        
        x, y = current_path[-1]

        # Up is always an option
        options = [(x, y-1)]
        # Left if not on left or bottom edge
        # Do not want more than one step on the bottom
        if x > 0 and y < grid_size - 1:
            options.append((x-1, y))
        # Right if not on right or bottom edge
        # Do not want more than one step on the bottom
        if x < grid_size - 1 and y < grid_size - 1:
            options.append((x+1, y))
        if y < grid_size - 1:
            options.append((x, y+1))
        
        random.shuffle(options)

        for option in options:
            if option not in current_path:
                path = self._generate_path(path_length, grid_size, current_path + [option])
                if path is not None:
                    return path
        
        return None
