import os
import re
from typing import Iterable, List, Tuple

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"


def match(string: str, pattern: str, exclude: str = "") -> bool:
    return all([signal in string for signal in [c for c in pattern if c not in exclude]])

def determine_pattern(unique_patterns: List[str]) -> dict:
    result = {}

    # First extract all patterns displayed by a unique number of segments
    for pattern in [pattern for pattern in unique_patterns if len(pattern) in [2,3,4,7]]:
        if len(pattern) == 2:
            result[1] = "".join(sorted(pattern))
        elif len(pattern) == 3:
            result[7] = "".join(sorted(pattern))
        elif len(pattern) == 4:
            result[4] = "".join(sorted(pattern))
        elif len(pattern) == 7:
            result[8] = "".join(sorted(pattern))

    # Then extract all patterns consisting of 6 segments
    for pattern in [pattern for pattern in unique_patterns if len(pattern) == 6]:
        if match(pattern, result[1] + result[4]):
            result[9] = "".join(sorted(pattern))
        elif match(pattern, result[1] + result[7]):
            result[0] = "".join(sorted(pattern))
        else:
            result[6] = "".join(sorted(pattern))

    # Lastly extract all patterns consisting of 5 segments
    for pattern in [pattern for pattern in unique_patterns if len(pattern) == 5]:
        if match(pattern, result[1]):
            result[3] = "".join(sorted(pattern))
        elif match(pattern, result[9], result[1]):
            result[5] = "".join(sorted(pattern))
        else:
            result[2] = "".join(sorted(pattern))

    return {y:x for x,y in result.items()}

def parse_input(filepath: str) -> Iterable[Tuple[List[str],List[str]]]:
    with open(filepath, "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            yield tuple([value.split() for value in re.split(" \| ", line)])

def part_1(filepath: str) -> int:
    count = 0
    for inputs, outputs in parse_input(filepath):
        for value in outputs:
            if len(value) in [2,3,4,7]:
                count+=1
    return count

def part_2(filepath: str) -> int:
    result = 0

    for inputs, outputs in parse_input(filepath):
        displayed_number = ""
        patterns = determine_pattern(inputs)

        for number in outputs:
            for pattern in patterns.keys():
                if "".join(sorted(number)) == pattern:
                    displayed_number += str(patterns[pattern])

        result += int(displayed_number)

    return result


if __name__ == "__main__":
    assert part_1(EXAMPLE_PATH) == 26
    assert part_2(EXAMPLE_PATH) == 61229

    print("\nChallenge 1:")
    print(part_1(INPUT_PATH))

    print("\nChallenge 2:")
    print(part_2(INPUT_PATH))
