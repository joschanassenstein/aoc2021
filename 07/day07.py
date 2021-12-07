import os
from typing import List

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"


def consumption(pos, dest, increased_burn = False) -> int:
    return abs(dest-pos) if not increased_burn else int(abs(dest-pos) * (abs(dest-pos) + 1) / 2)

def determine_optimum(positions: List, increased_burn = False) -> int:
    return min([sum([consumption(pos, dest, increased_burn) for pos in positions]) for dest in range(max(positions))])

def run(filepath, increased_burn = False) -> int:
    with open(filepath, "r", encoding="UTF-8") as input:
        positions = [int(n) for n in input.readline().rstrip().split(",")]
    return determine_optimum(positions, increased_burn)


if __name__ == "__main__":
    assert run(EXAMPLE_PATH) == 37
    assert run(EXAMPLE_PATH, increased_burn=True) == 168

    print("\nChallenge 1:")
    print(run(INPUT_PATH))

    print("\nChallenge 2:")
    print(run(INPUT_PATH, increased_burn=True))
