import unittest

from memorymaze import MemoryMaze
from memorymaze.gamestate import START_GRID_SIZE
from memorymaze.gamestate import STARTING_LIVES
from memorymaze.result import SelectResult


class TestMemoryMaze(unittest.TestCase):
    
    def setUp(self):
        self._memory_maze = MemoryMaze()
    
    def test_gameState(self):
        self.assertIsNotNone(self._memory_maze.game_state)
    
    def test_grid(self):
        self.assertIsNotNone(self._memory_maze.grid)
    
    def test_select(self):
        result = self._memory_maze.select(*self._memory_maze.grid.path[0])
        self.assertEqual(result, SelectResult.CORRECT)
    
    def test_select_gameOver(self):
        # Determine a wrong guess
        guess = (0, START_GRID_SIZE - 1)
        if guess == self._memory_maze.grid.path[0]:
            # In case random guess actually ends up being correct
            guess = (1, START_GRID_SIZE - 1)
        
        for i in range(self._memory_maze.game_state.lives - 1):
            result = self._memory_maze.select(*guess)
        
        result = self._memory_maze.select(*guess)
        self.assertEqual(result, SelectResult.GAME_OVER)
    
    def test_nextLevel(self):
        self._memory_maze.next_level()
        self.assertEqual(self._memory_maze.game_state.level, 2)
    
    def test_reset(self):
        # Determine a wrong guess
        guess = (0, START_GRID_SIZE - 1)
        if guess == self._memory_maze.grid.path[0]:
            # In case random guess actually ends up being correct
            guess = (1, START_GRID_SIZE - 1)
        
        self._memory_maze.select(*guess)
        self._memory_maze.next_level()
        
        self._memory_maze.reset()

        self.assertEqual(self._memory_maze.game_state.level, 1)
        self.assertEqual(self._memory_maze.game_state.lives, STARTING_LIVES)
    
    def test_lock(self):
        self._memory_maze.lock()

        self.assertIsNone(self._memory_maze.select(0, START_GRID_SIZE - 1))
