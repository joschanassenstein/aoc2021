import os
from typing import DefaultDict, Set
from collections import defaultdict

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"



class Pathfinder():
    def __init__(self, filepath: str) -> None:
        self.caves: DefaultDict[str, Set[str]] = defaultdict(set)

        with open(filepath, "r", encoding="UTF-8") as input:
            while (line := input.readline().rstrip()):
                cave_1, cave_2 = line.split("-")
                self.caves[cave_1].add(cave_2)
                self.caves[cave_2].add(cave_1)

    def find_paths(self, cave: str = "start", visited: Set[str] = {"start"}, allow_second_visit: bool = False) -> int:
        if cave == "end":
            return 1

        count = 0

        for neighbor in self.caves[cave]:
            if neighbor.isupper():
                count += self.find_paths(neighbor, visited, allow_second_visit)
            elif neighbor not in visited:
                count += self.find_paths(neighbor, set.union(visited, {neighbor}), allow_second_visit)
            elif allow_second_visit and neighbor != "start":
                count += self.find_paths(neighbor, visited, False)

        return count


if __name__ == "__main__":

    example = Pathfinder(EXAMPLE_PATH)
    print(example.find_paths())

    challenge = Pathfinder(INPUT_PATH)
    print("\nChallenge 1:")
    print(challenge.find_paths())
    print("\nChallenge 2:")
    print(challenge.find_paths(allow_second_visit=True))
