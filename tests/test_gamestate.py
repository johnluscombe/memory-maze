import unittest

from memorymaze.gamestate import GameState
from memorymaze.gamestate import PATH_SIZE_MULTIPLER
from memorymaze.gamestate import START_GRID_SIZE
from memorymaze.gamestate import STARTING_LIVES


class TestGameState(unittest.TestCase):
    
    def setUp(self):
        self._game_state = GameState()
    
    def test_defaults(self):
        self.assertEqual(self._game_state.level, 1)
        self.assertEqual(self._game_state.lives, STARTING_LIVES)
        self.assertEqual(self._game_state.grid_size, START_GRID_SIZE)

        path_length = round(START_GRID_SIZE * PATH_SIZE_MULTIPLER)
        self.assertEqual(self._game_state.path_size, path_length)
    
    def test_next_level(self):
        self._game_state.next_level()

        self.assertEqual(self._game_state.level, 2)
    
    def test_lose_life(self):
        self._game_state.lose_life()

        self.assertEqual(self._game_state.lives, STARTING_LIVES - 1)
    
    def test_lose_life_after_game_over(self):
        for i in range(self._game_state.lives + 1):
            self._game_state.lose_life()

        self.assertEqual(0, self._game_state.lives)
    
    def test_is_game_over_false(self):
        self.assertFalse(self._game_state.is_game_over)
    
    def test_is_game_over_true(self):
        for i in range(self._game_state.lives):
            self._game_state.lose_life()

        self.assertTrue(self._game_state.is_game_over)
    
    def test_reset(self):
        self._game_state.next_level()
        self._game_state.lose_life()
        self._game_state.reset()

        self.assertEqual(self._game_state.level, 1)
        self.assertEqual(self._game_state.lives, STARTING_LIVES)
        self.assertEqual(self._game_state.grid_size, START_GRID_SIZE)

        path_length = round(START_GRID_SIZE * PATH_SIZE_MULTIPLER)
        self.assertEqual(self._game_state.path_size, path_length)
