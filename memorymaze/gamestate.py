import uuid

# Grid size on Level 1.
START_GRID_SIZE = 5

# How many lives to start with.
STARTING_LIVES = 3

# Multiplier to use when calculating how long the path should be based on the
# grid size. The purpose of this is to get levels of fairly consistent
# difficulty, and that a it isn't just a straight line, for example.
PATH_SIZE_MULTIPLER = 1.6


class GameState:
    """
    Class for capturing the state of the game, such as the current level and
    number of lives.
    """
    
    def __init__(self):
        self._session = uuid.uuid4()
        self._level = 1
        self._lives = STARTING_LIVES
    
    @property
    def session(self):
        """
        Returns the session ID. Used to associate individual game plays and
        persist data.

        Returns:
            str
        """

        return self._session
    
    @property
    def level(self):
        """
        Returns the current level.

        Returns:
            int
        """

        return self._level
    
    def next_level(self):
        """
        Increments the level by 1, for example, when the current grid path is
        complete.
        """

        self._level += 1
    
    @property
    def lives(self):
        """
        Returns the number of lives remaining.

        Returns:
            int
        """

        return self._lives
    
    def lose_life(self):
        """
        Decrements the number of lives by 1, for example, when the user selects
        an incorrect square.

        Returns:
            bool: False if number of lives is zero after decrementing (Game Over),
                otherwise True.
        """

        self._lives -= 1
        return self._lives > 0

    @property
    def is_game_over(self):
        """
        Returns whether the game is over.

        Returns:
            bool
        """

        return self._lives <= 0
    
    @property
    def grid_size(self):
        """
        Returns the grid size based on the current level.

        Returns:
            int
        """

        return self._level + START_GRID_SIZE - 1
    
    @property
    def path_size(self):
        """
        Returns the desired path size based on the current level and grid size.

        Returns:
            int
        """

        return round(self.grid_size * PATH_SIZE_MULTIPLER)
    
    def reset(self):
        """
        Resets the game to its initial state.
        """

        self._session = uuid.uuid4()
        self._level = 1
        self._lives = STARTING_LIVES
