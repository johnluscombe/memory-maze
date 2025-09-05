"""
Module encapsulating persisting data for the game.
"""

import os
import traceback

from datetime import datetime, timezone

import xml.etree.cElementTree as ET

from memorymaze.gamestate import GameState
from memorymaze.util import resource_path

DEFAULT_DATA_FILE = resource_path("data.dat")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

ENCRYPTION_KEY = "memory-maze"


class HistoryEntry:
    """
    Class encapsulating one playthrough of the game.

    Arguments:
        date_completed (datetime): Datetime that this playthrough was completed.
        score (int): Level the player reached in this playthrough.
    """

    def __init__(self, date_completed: datetime, score: int):
        self._date_completed = date_completed
        self._score = score
    
    @staticmethod
    def now(score: int):
        """
        Constructs a HistoryEvent object, with a date completed set to the
        current time, in UTC.

        Returns:
            HistoryEntry
        """

        return HistoryEntry(datetime.now(timezone.utc), score)
    
    @property
    def date_completed(self) -> datetime:
        """
        Returns the date completed of this :class:`~HistoryEntry`.

        Returns:
            datetime
        """

        return self._date_completed
    
    @property
    def score(self) -> int:
        """
        Returns the score of this :class:`~HistoryEntry`.

        Returns:
            int
        """

        return self._score


class MemoryMazeData:
    """
    Class encapsulating persistent data for the game.
    """

    def __init__(self):
        self._high_score = 0
        self._history = []
    
    @property
    def high_score(self) -> int:
        """
        The high score.

        Returns:
            int
        """

        return self._high_score
    
    @property
    def average(self) -> float:
        """
        The average score of all the playthroughs.

        Returns:
            float
        """

        return sum(map(lambda e: e.score, self._history)) / len(self._history)
    
    def read(self, file: str) -> bool:
        """
        Reads the Memory Maze data from the file at the given path. Returns
        whether reading was successful.

        Arguments:
            file (str): Path where the file is stored.
        
        Returns:
            bool
        """

        if os.path.exists(file):
            try:
                with open(file, "rb") as f:
                    encrypted = f.read()
                    xml_bytes = bytearray()
                    for i in range(len(encrypted)):
                        # Decrypt data using simple xor encryption
                        xml_bytes.append(encrypted[i] ^ ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)]))
                    
                    root = ET.fromstring(xml_bytes)
                    
                    self._high_score = int(root.find("highScore").text)

                    for entry in root.find("history"):
                        date_completed_str = entry.find("dateCompleted")
                        date_completed = datetime.strptime(date_completed_str.text, DATETIME_FORMAT)
                        score = int(entry.find("score").text)
                        self._history.append(HistoryEntry(date_completed, score))
                    
                    return True
            except:
                print(traceback.format_exc())
                return False
        
        return False
    
    def read_default(self) -> bool:
        """
        Reads the Memory Maze data from the file at the default path. Returns
        whether reading was successful.

        Returns:
            bool
        """

        return self.read(DEFAULT_DATA_FILE)
    
    def record(self, game_state: GameState):
        """
        Records persistent data from the given :class:`~GameState` to memory,
        to be written to the data file later.

        Arguments:
            game_state (:class:`~GameState`): The game state to record.
        """

        if game_state.level > self._high_score:
            self._high_score = game_state.level

        self._history.append(HistoryEntry.now(game_state.level))
    
    def write(self, file: str) -> bool:
        """
        Writes the Memory Maze data to the file at the given path. Returns
        whether writing was successful.

        Arguments:
            file (str): Path where the file should be written.
        
        Returns:
            bool
        """

        try:
            with open(file, "wb") as f:
                root = ET.Element("memoryMaze")
                ET.SubElement(root, "history")

                high_score_node = ET.SubElement(root, "highScore")
                high_score_node.text = str(self._high_score)

                for entry in self._history:
                    history_node = root.find("history")
                    entry_node = ET.SubElement(history_node, "entry")
                    date_completed_node = ET.SubElement(entry_node, "dateCompleted")
                    date_completed_node.text = entry.date_completed.strftime(DATETIME_FORMAT)
                    score_node = ET.SubElement(entry_node, "score")
                    score_node.text = str(entry.score)

                ET.indent(root)

                xml_str = ET.tostring(root)
                encrypted = bytearray()

                for i in range(len(xml_str)):
                    encrypted.append(xml_str[i] ^ ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)]))
                
                f.write(encrypted)

                return True
        except:
            print(traceback.format_exc())
            return False
    
    def write_default(self) -> bool:
        """
        Writes the Memory Maze data to the file at the default path. Returns
        whether writing was successful.

        Returns:
            bool
        """

        return self.write(DEFAULT_DATA_FILE)
