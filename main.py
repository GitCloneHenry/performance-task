from typing import List, Dict
from os import listdir
from sys import argv
import json

class CardNode:
    def __init__(self, a_side: str, b_side: str):
        self.a_side = a_side
        self.b_side = b_side
    
    @staticmethod
    def get_card_nodes(file_path: str) -> List["CardNode"]:
        flashcard_set: Dict[str, str] 
        with open(file_path, "r") as f:
            flashcard_set = json.load(f)
        
        return [CardNode(keys, items) for keys, items in flashcard_set.items()]

class CardEngine:
    def __init__(self) -> None:
        card_nodes: List[CardNode]

    @staticmethod
    def get_file_path() -> str:
        if len(argv) <= 1:
            
        else:
            return argv[1]

print(listdir(".\\sets"))
print(argv[1:])

with open(r".\\sets\\example_set.json", "r") as f:
    print(json.load(f))