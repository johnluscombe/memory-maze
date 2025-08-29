from memorymaze.gamestate import GameState
from memorymaze.grid import MemoryMazeGrid
from memorymaze.result import SelectResult


class MemoryMaze:
    """
    Class handling the business logic for the MemoryMaze game.
    """

    def __init__(self):
        self._game_state = GameState()
        self._grid = MemoryMazeGrid()
        self._locked = False

        self._generate_path()
    
    @property
    def game_state(self):
        """
        Returns the game state.

        Returns:
            :class:`~GameState`
        """

        return self._game_state
    
    @property
    def grid(self):
        """
        Returns the grid.
        
        Returns:
            :class:`~MemoryMazeGrid`
        """

        return self._grid
    
    def select(self, x, y):
        """
        Selects a grid coordinate, updates the game state and grid
        accordingly, and returns the result of that action.
        If the game is locked, None is returned.
        If the user selects an incorrect square, the game state is updated to
        lose a life and the result of that action is returned to the caller.
        If the user selects a correct square, the result of that action is
        simply returned to the caller.
        If the user completes the grid, the game state is updated to the next
        level, a new path is generated, and the completion result is returned
        to the caller.
        If the number of lives reaches zero, the game over result is returned
        to the caller.

        Arguments:
            x (int): X grid coordinate.
            y (int): Y grid coordinate.

        Returns:
            :class:`~SelectResult`
        """

        if not self._locked:
            result = self._grid.select(x, y)
            if result == SelectResult.COMPLETE:
                self._game_state.next_level()
                self._generate_path()
            elif result == SelectResult.INCORRECT:
                self._game_state.lose_life()
                if self._game_state.lives <= 0:
                    return SelectResult.GAME_OVER
            return result
        return None
    
    def next_level(self):
        """
        Updates the game state to the next level and generates a new path.
        """

        self._game_state.next_level()
        self._generate_path()
    
    def reset(self):
        """
        Resets the game state and generates a new path.
        """

        self._game_state.reset()
        self._generate_path()
    
    def lock(self):
        """
        Locks the grid so selecting a grid position does nothing. This is
        useful for disabling mouse events, for example, when the grid path is
        being shown.
        """

        self._locked = True
    
    def unlock(self):
        """
        Unlocks the grid, so selecting a grid position is registered.
        """

        self._locked = False
    
    def _generate_path(self):
        """
        Convenience method for generating a new path on the grid, using the
        path and grid size from the game state.
        """

        self._grid.generate_path(self._game_state.path_size, self._game_state.grid_size)
