"""
Utility functions related to the keyboard.
"""

UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

W = "W"
S = "S"
A = "A"
D = "D"

def is_up(key: str) -> bool:
    """
    Returns whether the given key is up (up arrow or "w").
    """

    return key == UP or key.upper() == W

def is_down(key: str) -> bool:
    """
    Returns whether the given key is down (down arrow or "s").
    """

    return key == DOWN or key.upper() == S

def is_left(key: str) -> bool:
    """
    Returns whether the given key is left (left arrow or "a").
    """

    return key == LEFT or key.upper() == A

def is_right(key: str) -> bool:
    """
    Returns whether the given key is right (right arrow or "d").
    """

    return key == RIGHT or key.upper() == D
