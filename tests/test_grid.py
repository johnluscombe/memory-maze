import unittest

from memorymaze.grid import MemoryMazeGrid
from memorymaze.result import SelectResult


class TestGrid(unittest.TestCase):

    def setUp(self):
        self._grid = MemoryMazeGrid()
    
    def test_path_notGenerated(self):
        self.assertIsNone(self._grid.path)
    
    def test_path_generated(self):
        self._grid.generate_path(8, 5)
        self.assertIsNotNone(self._grid.path)
    
    def test_path_afterComplete_newPathNotGeneratedYet(self):
        path = self._grid.generate_path(8, 5)

        # Select every coordinate in the path, completing the level
        for coord in path:
            self._grid.select(*coord)
        
        self.assertEqual(self._grid.path, path)
    
    def test_lastPosition_nothingSelectedYet(self):
        self.assertIsNone(self._grid.last_position)
    
    def test_lastPosition_afterOneCorrect(self):
        path = self._grid.generate_path(8, 5)
        self._grid.select(*path[0])
        self.assertEqual(self._grid.last_position, path[0])
    
    def test_lastPosition_afterOneIncorrect(self):
        path = self._grid.generate_path(8, 5)

        # Determine a wrong guess
        guess = (0, 4)
        if guess == path[0]:
            # In case random guess actually ends up being correct
            guess = (1, 4)
        
        self._grid.select(*guess)
        self.assertIsNone(self._grid.last_position)
    
    def test_lastPosition_afterOneCorrectAndOneIncorrect(self):
        path = self._grid.generate_path(8, 5)

        # Select correct
        self._grid.select(*path[0])

        # Select incorrect - one square up from the previous position
        guess = (path[0][0], path[0][1]-1)

        if guess == path[1]:
            # If one square up is correct, do one square left of previous
            # position
            guess = (path[0][0]-1, path[0][1])

            if guess[0] == -1:
                # If we're already on the left edge, do one square right of
                # previous position
                guess = (path[0][0]+1, path[0][1])
        
        self._grid.select(*guess)
        self.assertIsNone(self._grid.last_position)
    
    def test_lastPosition_afterComplete_netResetYet(self):
        path = self._grid.generate_path(8, 5)

        # Select every coordinate in the path, completing the level
        for coord in path:
            self._grid.select(*coord)
        
        self.assertEqual(self._grid.last_position, path[-1])
    
    def test_generatePath(self):
        path = self._grid.generate_path(8, 5)
        self.assertEqual(8, len(path))
    
    def test_generatePath_notPossible_returnsNone(self):
        path = self._grid.generate_path(5, 8)
        self.assertIsNone(path)
    
    def test_generatePath_negativePathLength_returnsNone(self):
        with self.assertRaises(ValueError) as error:
            self._grid.generate_path(-1, 8)
        self.assertEqual(str(error.exception), "Path length must be positive")
    
    def test_generatePath_zeroPathLength_returnsNone(self):
        with self.assertRaises(ValueError) as error:
            self._grid.generate_path(0, 8)
        self.assertEqual(str(error.exception), "Path length must be positive")
    
    def test_generatePath_negativeGridSize_returnsNone(self):
        with self.assertRaises(ValueError) as error:
            self._grid.generate_path(5, -1)
        self.assertEqual(str(error.exception), "Grid size must be positive")
    
    def test_generatePath_zeroGridSize_returnsNone(self):
        with self.assertRaises(ValueError) as error:
            self._grid.generate_path(5, 0)
        self.assertEqual(str(error.exception), "Grid size must be positive")
    
    def test_generatePath_startsAtBottom(self):
        path = self._grid.generate_path(8, 5)
        self.assertEqual(path[0][1], 4)
    
    def test_generatePath_endsAtTop(self):
        path = self._grid.generate_path(8, 5)
        self.assertEqual(path[-1][1], 0)
    
    def test_generatePath_onlyOneAtBottom(self):
        path = self._grid.generate_path(8, 5)
        ys = list(map(lambda coord: coord[1], path))
        self.assertEqual(ys.count(4), 1)
    
    def test_generatePath_onlyOneAtTop(self):
        path = self._grid.generate_path(8, 5)
        ys = list(map(lambda coord: coord[1], path))
        self.assertEqual(ys.count(0), 1)
    
    def test_generatePath_eachSquareIsAdjacentToPrevious(self):
        path = self._grid.generate_path(8, 5)
        previous = path[0]
        for coord in path[1:]:
            self.assertTrue(coord[0] == previous[0] or coord[1] == previous[1])
            previous = coord
    
    def test_generatePath_noDuplicates(self):
        path = self._grid.generate_path(8, 5)
        self.assertEqual(len(path), len(set(path)))
    
    def test_select_beforePathGeneration(self):
        self.assertIsNone(self._grid.select(0, 0))
    
    def test_select_correct(self):
        path = self._grid.generate_path(8, 5)
        result = self._grid.select(*path[0])
        self.assertEqual(result, SelectResult.CORRECT)
    
    def test_select_incorrect(self):
        path = self._grid.generate_path(8, 5)

        # Determine a wrong guess
        guess = (0, 4)
        if guess == path[0]:
            # In case random guess actually ends up being correct
            guess = (1, 4)
        
        result = self._grid.select(*guess)
        self.assertEqual(result, SelectResult.INCORRECT)
    
    def test_select_complete(self):
        path = self._grid.generate_path(8, 5)

        # Select every coordinate in the path except for the last one
        for coord in path[:len(path) - 1]:
            self._grid.select(*coord)
        
        # Get result of selecting the last coordinate in the path
        result = self._grid.select(*path[-1])

        self.assertEqual(result, SelectResult.COMPLETE)
    
    def test_select_firstMove_allowsSelectingAnySquareOnFirstRow(self):
        path = self._grid.generate_path(8, 5)

        # Test every square on the first row, except for the correct one
        for i in range(5):
            if (i, 4) != path[0]:
                result = self._grid.select(i, 4)
                self.assertEqual(result, SelectResult.INCORRECT)
        
        # Now test the correct one
        result = self._grid.select(*path[0])
        self.assertEqual(result, SelectResult.CORRECT)
    
    def test_select_allowsSelectingLeftOrRight(self):
        path = self._grid.generate_path(8, 5)

        # Get a path where the first square is not on the edge
        while path[0][0] == 0 or path[0][0] == 4:
            path = self._grid.generate_path(8, 5)
        
        x, y = path[0]
        
        # Select first square. Next one is guaranteed to be above it.
        self._grid.select(x, y)

        # Left, guaranteed to be incorrect
        result = self._grid.select(x - 1, y)
        self.assertEqual(result, SelectResult.INCORRECT)

        # Right, guaranteed to be incorrect
        result = self._grid.select(x + 1, y)
        self.assertEqual(result, SelectResult.INCORRECT)
    
    def test_select_allowsSelectingUp(self):
        path = self._grid.generate_path(8, 5)
        
        # Find the part in the grid where the next correct square is NOT above
        # the previously selected one
        for i in range(8):
            x, y = path[i]
            self._grid.select(x, y)
            if path[i + 1] != (x, y - 1):
                break

        result = self._grid.select(x, y - 1)
        self.assertEqual(result, SelectResult.INCORRECT)
    
    def test_select_allowsSelectingDown(self):
        path = self._grid.generate_path(8, 5)
        
        # Find the first part in the grid where the next correct square is left
        # or right of the previously selected one.
        for i in range(8):
            x, y = path[i]
            self._grid.select(x, y)
            if path[i + 1] != (x, y - 1):
                x, y = path[i + 1]
                self._grid.select(x, y)
                break
        
        result = self._grid.select(x, y + 1)
        self.assertEqual(result, SelectResult.INCORRECT)
    
    def test_select_doesNotAllowSelectingKittyCorner(self):
        path = self._grid.generate_path(8, 5)

        # Get a path where the first square is not on the edge
        while path[0][0] == 0 or path[0][0] == 4:
            path = self._grid.generate_path(8, 5)
        
        x, y = path[0]
        
        self._grid.select(x, y)

        self.assertIsNone(self._grid.select(x + 1, y + 1))
        self.assertIsNone(self._grid.select(x - 1, y + 1))
        self.assertIsNone(self._grid.select(x + 1, y - 1))
        self.assertIsNone(self._grid.select(x - 1, y - 1))
    
    def test_select_doesNotAllowSelectingSameSquare(self):
        path = self._grid.generate_path(8, 5)

        self._grid.select(*path[0])
        result = self._grid.select(*path[0])

        self.assertIsNone(result)
    
    def test_select_doesNotAllowSelectingPreviousSquare(self):
        path = self._grid.generate_path(8, 5)

        self._grid.select(*path[0])
        self._grid.select(*path[1])
        result = self._grid.select(*path[0])

        self.assertIsNone(result)
    
    def test_select_doesNotAllowSelectingOutOfBounds_bottom(self):
        path = self._grid.generate_path(8, 5)

        x, y = path[0]
        self._grid.select(x, y)
        result = self._grid.select(x, y + 1)

        self.assertIsNone(result)
    
    def test_select_doesNotAllowSelectingOutOfBounds_left(self):
        path = self._grid.generate_path(8, 5)

        # Get a path where the first square is on the left edge
        while path[0][0] != 0:
            path = self._grid.generate_path(8, 5)

        x, y = path[0]
        self._grid.select(x, y)
        result = self._grid.select(x - 1, y)

        self.assertIsNone(result)
    
    def test_select_doesNotAllowSelectingOutOfBounds_right(self):
        path = self._grid.generate_path(8, 5)

        # Get a path where the first square is on the left edge
        while path[0][0] != 4:
            path = self._grid.generate_path(8, 5)

        x, y = path[0]
        self._grid.select(x, y)
        result = self._grid.select(x + 1, y)

        self.assertIsNone(result)
    
    def test_select_doesNotAllowSelectingOutOfBounds_top(self):
        path = self._grid.generate_path(8, 5)

        result = self._grid.select(0, -1)

        self.assertIsNone(result)
