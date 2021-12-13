import os
from typing import Set, List, Tuple

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

def parse_input(filepath: str) -> Tuple[Set[Tuple[int,int]], List[Tuple[str,int]]]:
    marks = set()
    instructions = []

    with open(filepath, "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            x,y = [int(point) for point in line.split(",")]
            marks.add((x,y))

        while (line := input.readline().rstrip()):
            axis, value = line[11:].split("=")
            instructions.append((axis,int(value)))

    return marks, instructions

def fold(marks: Set[Tuple[int,int]], instruction: Tuple[str,int]) -> Set[Tuple[int,int]]:
    axis, fold = instruction
    index = 0 if axis == "x" else 1
    updated = set()

    for mark in marks:
        if mark[index] < fold:
            updated.add(mark)
        elif mark[index] > fold:
            if axis == "x":
                 updated.add((fold - (mark[0] - fold), mark[1]))
            else:
                 updated.add((mark[0], fold - (mark[1] - fold)))

    return updated

def as_string(marks: Set[Tuple[int,int]]) -> str:
    output = []

    for column in range(max(mark[1] for mark in marks) + 1):
        output.append([])
        for row in range(max(mark[0] for mark in marks) + 1):
            output[column].append(".")

    for mark in marks:
        output[mark[1]][mark[0]] = "#"

    result = ""

    for row in output:
        result += "".join(row)
        result += "\n"

    return result


def part_1(filepath: str) -> int:
    marks, instructions = parse_input(filepath)
    return len(fold(marks, instructions[0]))

def part_2(filepath: str) -> str:
    marks, instructions = parse_input(filepath)
    for instruction in instructions:
        marks = fold(marks, instruction)

    return as_string(marks)


if __name__ == "__main__":

    assert part_1(EXAMPLE_PATH) == 17
    print("\nExample:")
    print(part_2(EXAMPLE_PATH))

    print("\nChallenge 1:")
    print(part_1(INPUT_PATH))
    print("\nChallenge 2:")
    print(part_2(INPUT_PATH))
