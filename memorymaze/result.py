from enum import Enum

class SelectResult(Enum):
    """
    Enum responsible for communicating the state of the grid after the user
    selects a square.

    Attributes:
        GAME_OVER: The user has selected an incorrect square which causes the
            number of lives remaining to hit zero, resulting in a Game Over
            state.
        INCORRECT: The user has selected an incorrect square, but the number of
            lives is still greater than zero.
        CORRECT: The user has selected a correct square, but the path is not
            complete yet.
        COMPLETE: The user has selected a correct square which causes the path
            to be complete.
    """

    GAME_OVER = -1
    INCORRECT = 0
    CORRECT = 1
    COMPLETE = 2
