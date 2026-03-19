from typing import List, Dict
from os import listdir
from sys import argv
from random import randint
import json
import os


class CardNode:
    def __init__(self, a_side: str, b_side: str):
        self.a_side = a_side
        self.b_side = b_side

    def __repr__(self):
        return "%s: %s" % (self.a_side, self.b_side)

    @staticmethod
    def get_card_nodes(file_path: str) -> List["CardNode"]:
        flashcard_set: Dict[str, str]
        with open(file_path, "r") as f:
            flashcard_set = json.load(f)

        return [
            CardNode(key, item)
            for key, item in flashcard_set.items()
            if key != "set_title"
        ]


class CardEngine:
    def __init__(self) -> None:
        file_path: str | None = self.get_file_path()
        self.card_nodes: List[CardNode] | None = (
            CardNode.get_card_nodes(file_path) if file_path != None else None
        )

    @staticmethod
    def get_input(prefix: str = "") -> str:
        return input([f"{[prefix]} ", ""][prefix == ""] + "> ")

    @staticmethod
    def is_valid_file(file_path: str) -> bool:
        file = open(file_path, "r")

        try:
            file_data: Dict[str, str] = json.load(file)
        except (json.JSONDecodeError, ValueError):
            return False

        if not os.path.isfile(file_path):
            return False

        if not "set_title" in file_data.keys():
            return False

        return True

    @staticmethod
    def get_file_path() -> str | None:
        if len(argv) <= 1:
            available_sets: List[str] = listdir(".\\sets")

            valid_sets: List[str] = list(
                filter(
                    lambda file_name: CardEngine.is_valid_file(f".\\sets\\{file_name}"),
                    available_sets,
                )
            )

            if len(available_sets) == 0 or len(valid_sets) == 0:
                print("No valid sets in the sets directory.")
                return None

            print("Please choose a set from the list of existing sets:")

            for iteration, file_name in enumerate(valid_sets):
                file = open(f".\\sets\\{file_name}", "r")

                file_data: Dict[str, str] = json.load(file)

                print(f"    {iteration + 1}: {file_data["set_title"]}")

                file.close()

            while True:
                try:
                    choice = int(CardEngine.get_input())
                    if 1 <= choice <= len(valid_sets):
                        return ".\\sets\\%s" % valid_sets[choice - 1]
                    print(f"Invalid selection, try again.")
                except ValueError:
                    print("Please enter a number.")
        elif os.path.isfile(argv[1]):
            return str(argv[1])
        else:
            argv.pop(1)
            return CardEngine.get_file_path()

    @staticmethod
    def compare_similarity(a: str, b: str) -> float:
        set_a, set_b = set(a), set(b)
        return len(set_a.intersection(set_b)) / len(set_a.union(set_b))

    def study_set(self) -> None:
        if not self.card_nodes:
            return

        nodes_to_study: List[CardNode] = list(self.card_nodes)

        while len(nodes_to_study) > 0:
            node = nodes_to_study.pop(randint(0, len(nodes_to_study) - 1))
            print(node.a_side)
            response = CardEngine.get_input()
            print(self.compare_similarity(node.b_side, response))


if __name__ == "__main__":
    card_engine = CardEngine()
    card_engine.study_set()
