import os
import traceback

from datetime import datetime, timezone

import xml.etree.cElementTree as ET

from memorymaze.util import resource_path

DEFAULT_DATA_FILE = resource_path("data.dat")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

ENCRYPTION_KEY = "memory-maze"


class HistoryEntry:

    def __init__(self, date_completed, score):
        self._date_completed = date_completed
        self._score = score
    
    @staticmethod
    def now(score):
        return HistoryEntry(datetime.now(timezone.utc), score)
    
    @property
    def date_completed(self):
        return self._date_completed
    
    @property
    def score(self):
        return self._score


class MemoryMazeData:

    def __init__(self):
        self._high_score = 0
        self._history = []
    
    @property
    def high_score(self):
        return self._high_score
    
    @property
    def average(self):
        return sum(map(lambda e: e.score, self._history)) / len(self._history)
    
    def read(self, file):
        if os.path.exists(file):
            try:
                with open(file, "rb") as f:
                    encrypted = f.read()
                    xml_bytes = bytearray()
                    for i in range(len(encrypted)):
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
    
    def read_default(self):
        return self.read(DEFAULT_DATA_FILE)
    
    def record(self, game_state):
        if game_state.level > self._high_score:
            self._high_score = game_state.level

        self._history.append(HistoryEntry.now(game_state.level))
    
    def write(self, file):
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
    
    def write_default(self):
        return self.write(DEFAULT_DATA_FILE)
