import os
from typing import Optional
from statistics import median

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

chunk_delimiters = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

def identity_corrupted_symbol(line: str) -> Optional[str]:
    sequence = []
    for symbol in line:
        if symbol in chunk_delimiters.keys():
            sequence.append(symbol)
        else:
            last_opening = sequence.pop(-1)
            if symbol != chunk_delimiters[last_opening]:
                return symbol
    return None

def identity_missing_symbols_score(line: str) -> int:
    result = 0
    sequence = []
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}

    for symbol in line:
        if symbol in chunk_delimiters.keys():
            sequence.append(symbol)
        else:
            sequence.pop(-1)

    for missing_closing in reversed(sequence):
        result = (result * 5) + scores[missing_closing]

    return result


def part_1(filepath: str) -> int:
    result = 0
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    with open(filepath, "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            if corrupted_symbol := identity_corrupted_symbol(line):
                result += scores[corrupted_symbol]
    return result

def part_2(filepath: str) -> int:
    scores = []
    with open(filepath, "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            if not identity_corrupted_symbol(line):
                scores.append(identity_missing_symbols_score(line))
    return median(sorted(scores))


if __name__ == "__main__":
    assert part_1(EXAMPLE_PATH) == 26397
    assert part_2(EXAMPLE_PATH) == 288957

    print("\nChallenge 1:")
    print(part_1(INPUT_PATH))

    print("\nChallenge 2:")
    print(part_2(INPUT_PATH))
