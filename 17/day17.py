import os
import re
from dataclasses import dataclass
from typing import Optional, Tuple

INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"


@dataclass
class Probe():
    x_velocity: int
    y_velocity: int
    x_position: int = 0
    y_position: int = 0
    y_max: int = 0

    def next_step(self) -> None:
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        if self.x_velocity > 0:
            self.x_velocity -= 1
        elif self.x_velocity < 0:
            self.x_velocity += 1
        self.y_velocity -= 1
        if self.y_position > self.y_max:
            self.y_max = self.y_position

class Trench():
    def __init__(self, filepath: str) -> None:
        with open(filepath, "r", encoding="UTF-8") as f:
            line = f.readline()
            self.left_border, self.right_border = [int(pos) for pos in re.search("x=(.*),", line).group(1).split("..")]
            self.bottom_border, self.top_border = [int(pos) for pos in re.search("y=(.*)", line).group(1).split("..")]

    def hit(self, probe: Probe) -> Optional[bool]:
        if probe.x_position >= self.left_border and probe.x_position <= self.right_border:
            if probe.y_position <= self.top_border and probe.y_position >= self.bottom_border:
                return True
        if probe.x_position > self.right_border or probe.y_position < self.bottom_border:
            return None
        return False


class Launcher():
    def __init__(self, filepath: str) -> None:
        self.trench = Trench(filepath)

    def launch(self, x_velocity: int, y_velocity: int) -> Optional[Probe]:
        probe = Probe(x_velocity, y_velocity)

        while True:
            if (step_result := self.trench.hit(probe)) == None:
                return None
            elif step_result == True:
                return probe
            elif step_result == False:
                if probe.x_velocity == 0 and probe.x_position < self.trench.left_border:
                    return None

            probe.next_step()

    def simulate_launches(self) -> Tuple[int,int]:
        max_height = 0
        successful_launches = 0
        for x in range(self.trench.right_border + 1):
            for y in range(self.trench.bottom_border, 100):
                probe = self.launch(x,y)
                if probe:
                    successful_launches += 1
                    if probe.y_max > max_height:
                        max_height = probe.y_max

        return max_height, successful_launches


if __name__ == "__main__":
    example = Launcher(EXAMPLE_PATH)
    example_ymax, example_launches = example.simulate_launches()
    assert example_ymax == 45
    assert example_launches == 112

    launcher = Launcher(INPUT_PATH)
    ymax, launches = launcher.simulate_launches()
    print(f"\nChallenge 1: {ymax}")
    print(f"\nChallenge 2: {launches}")
