import os
from dataclasses import dataclass

@dataclass
class Submarine1():
    position: int = 0
    depth: int = 0

    def handle_command(self, input: str):
        inputs = input.split(" ")
        command, value = inputs[0], int(inputs[1])

        if command == "forward":
            self.position += value
        elif command == "down":
            self.depth += value
        elif command == "up":
            self.depth -= value

@dataclass
class Submarine2():
    position: int = 0
    depth: int = 0
    aim: int = 0

    def handle_command(self, input: str) -> None:
        inputs = input.split(" ")
        command, value = inputs[0], int(inputs[1])

        if command == "forward":
            self.position += value
            self.depth += self.aim * value
        elif command == "down":
            self.aim += value
        elif command == "up":
            self.aim -= value


if __name__ == "__main__":

    submarine1 = Submarine1()
    submarine2 = Submarine2()

    with open(f"{os.path.dirname(os.path.realpath(__file__))}/input.txt", "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            submarine1.handle_command(line)
            submarine2.handle_command(line)

    print("Challenge 1:")
    print(f"Position: {submarine1.position}")
    print(f"Depth: {submarine1.depth}")
    print(f"Multiplied: {submarine1.position * submarine1.depth}")

    print("\nChallenge 2:")
    print(f"Position: {submarine2.position}")
    print(f"Depth: {submarine2.depth}")
    print(f"Aim: {submarine2.aim}")
    print(f"Multiplied: {submarine2.position * submarine2.depth}")
