UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

W = "W"
S = "S"
A = "A"
D = "D"

def is_up(key):
    return key == UP or key.upper() == W

def is_down(key):
    return key == DOWN or key.upper() == S

def is_left(key):
    return key == LEFT or key.upper() == A

def is_right(key):
    return key == RIGHT or key.upper() == D
