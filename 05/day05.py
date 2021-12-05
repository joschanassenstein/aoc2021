import os
import re
from dataclasses import dataclass

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

@dataclass
class Coordinate():
    x: int
    y: int

class VentScanner():
    def __init__(self, size: int, diagonal: bool = False):
        self.diagonal = diagonal
        self.vents = []
        for i in range(size):
            self.vents.append([])
            for j in range(size):
                self.vents[i].append(0)

    def handle_input(self, filepath: str) -> None:
        with open(filepath, "r", encoding="UTF-8") as input:
            while (line := input.readline().rstrip()):
                values = [int(n) for n in re.split(",| -> ", line)]
                start = Coordinate(values[0], values[1])
                stop = Coordinate(values[2], values[3])

                if start.y == stop.y:                                       # ←
                    if start.x > stop.x:
                        diff = start.x - stop.x
                        for i in range(diff + 1):
                            self.vents[start.y][stop.x + i] += 1
                    else:                                                   # →
                        diff = stop.x - start.x
                        for i in range(diff + 1):
                            self.vents[start.y][start.x + i] += 1
                elif start.x == stop.x:
                    if start.y > stop.y:                                    # ↑
                        diff = start.y - stop.y
                        for i in range(diff + 1):
                            self.vents[stop.y + i][start.x] += 1
                    else:                                                   # ↓
                        diff = stop.y - start.y
                        for i in range(diff + 1):
                            self.vents[start.y + i][start.x] += 1
                elif self.diagonal:
                    if start.y < stop.y:
                        diff = stop.y - start.y
                        if start.x < stop.x:                                # ↘
                            for i in range(diff + 1):
                                self.vents[start.y + i][start.x + i] += 1
                        else:                                               # ↙
                            for i in range(diff + 1):
                                self.vents[start.y + i][start.x - i] += 1
                    else:
                        diff = start.y - stop.y
                        if start.x < stop.x:                                # ↗
                            for i in range(diff + 1):
                                self.vents[start.y - i][start.x + i] += 1
                        else:                                               # ↖
                            for i in range(diff + 1):
                                self.vents[start.y - i][start.x - i] += 1

    def result(self) -> int:
        result = 0
        for row in self.vents:
            for value in row:
                if value >= 2:
                    result += 1
        return result

    def __repr__(self) -> str:
        result = "\n"
        for i in range(len(self.vents)):
            for j in range(len(self.vents[i])):
                result += str(self.vents[i][j])
            result += "\n"
        return result


def determine_gridsize(filepath: str) -> int:
    values = []
    with open(filepath, "r", encoding="UTF-8") as input:
        while(line := input.readline().rstrip()):
            values.extend(int(value) for value in re.findall(r'\b\d+\b', line))
    return max(values) + 1


def run(vent_scanner: VentScanner, filepath: str) -> int:
    vent_scanner.handle_input(filepath)
    return vent_scanner.result()

def test(vent_scanner: VentScanner, filepath: str, expected_result: int) -> None:
    result = run(vent_scanner, filepath)
    print(vent_scanner)
    assert result == expected_result


if __name__ == "__main__":

    example_gridsize = determine_gridsize(EXAMPLE_PATH)
    challenge_gridsize = determine_gridsize(INPUT_PATH)

    print("\nTest 1:")
    test(VentScanner(size=example_gridsize), EXAMPLE_PATH, 5)

    print("\nTest 2:")
    test(VentScanner(size=example_gridsize, diagonal=True), EXAMPLE_PATH, 12)

    print("\nChallenge 1:")
    print(run(VentScanner(size=challenge_gridsize), INPUT_PATH))

    print("\nChallenge 2:")
    print(run(VentScanner(size=challenge_gridsize, diagonal=True), INPUT_PATH))
