import os
from typing import List, Tuple
from dataclasses import dataclass

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

@dataclass
class Octopus():
    energy: int
    flashed: bool = False

class OctopusScanner():
    def __init__(self, filepath: str):
        self.adjacent : List[Tuple[int,int]] = [
            (0,1),(-1,1),(-1,0),(-1,-1),
            (0,-1),(1,-1),(1,0),(1,1)
        ]
        self.octopodes: List[List[Octopus]] = []

        with open(filepath, "r", encoding="UTF-8") as input:
            while (line := input.readline().rstrip()):
                self.octopodes.append([Octopus(int(energy)) for energy in line])

    def flash(self, position: Tuple[int,int]) -> None:
        x,y = position
        self.octopodes[y][x].flashed = True
        for dx,dy in self.adjacent:
            if x+dx in range(10) and y+dy in range(10):
                self.octopodes[y+dy][x+dx].energy += 1

    def simulate_step(self) -> Tuple[int, bool]:
        flashes = 0

        for y in range(10):
            for x in range(10):
                self.octopodes[y][x].energy += 1

        while True:
            to_flash = []
            for y in range(10):
                for x in range(10):
                    if self.octopodes[y][x].energy > 9 and not self.octopodes[y][x].flashed:
                        to_flash.append((x,y))

            if to_flash:
                for position in to_flash:
                    flashes += 1
                    self.flash(position)
            else:
                break

        flashed_octopodes = 0
        for y in range(10):
            for x in range(10):
                if self.octopodes[y][x].flashed:
                    self.octopodes[y][x].energy = 0
                    self.octopodes[y][x].flashed = False
                    flashed_octopodes += 1

        return flashes, flashed_octopodes

    def simulate_steps(self, steps: int) -> int:
        result = 0
        for step in range(steps):
            result += self.simulate_step()[0]
        return result

    def find_synchronized_step(self) -> int:
        step = 1
        while True:
            count = self.simulate_step()[1]
            if count == 100:
                return step
            step += 1


if __name__ == "__main__":

    assert OctopusScanner(EXAMPLE_PATH).simulate_steps(100) == 1656
    assert OctopusScanner(EXAMPLE_PATH).find_synchronized_step() == 195

    print("\nChallenge 1:")
    print(OctopusScanner(INPUT_PATH).simulate_steps(100))
    print("\nChallenge 2:")
    print(OctopusScanner(INPUT_PATH).find_synchronized_step())
