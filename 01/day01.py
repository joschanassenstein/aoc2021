import os
from typing import List


def challenge_one(numbers: List) -> int:
    result = 0
    previous_number = None

    for current_number in numbers:
        if previous_number and current_number > previous_number:
            result += 1
        previous_number = current_number

    return result

def challenge_two(numbers: List, window_size: int) -> int:
    result = 0
    previous_window = None

    for index in range(len(numbers)-(window_size-1)):
        current_window = sum(numbers[index:index+window_size])
        if previous_window and current_window > previous_window:
            result += 1
        previous_window = current_window

    return result


if __name__ == "__main__":

    numbers = []
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/input.txt", "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            numbers.append(int(line))

        print(f"Challenge 1: {challenge_one(numbers)}")
        print(f"Challenge 2: {challenge_two(numbers, 3)}")
