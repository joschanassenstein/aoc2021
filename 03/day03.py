import os
from dataclasses import dataclass, field
from typing import List, Callable

@dataclass
class Submarine():
    report_lines: List = field(default_factory=lambda: [])

    @staticmethod
    def __most_common(values: List) -> str:
        count_0, count_1 = 0, 0
        for char in values:
            if char == "0":
                count_0 += 1
            else:
                count_1 += 1

        return "0" if count_0 > count_1 else "1"

    @staticmethod
    def __least_common(values: List) -> str:
        count_0, count_1 = 0, 0
        for char in values:
            if char == "0":
                count_0 += 1
            else:
                count_1 += 1

        return "0" if count_0 <= count_1 else "1"

    def __get_rating(self, measurements: List, bitcriteria_function: Callable[[List], str], position: int = 0) -> int:
        remaining = []
        bitcriteria = bitcriteria_function([measurement[position] for measurement in measurements])

        for measurement in measurements:
            if measurement[position] == bitcriteria:
                remaining.append(measurement)

        if len(remaining) == 1:
            return int(remaining[0],2)

        return self.__get_rating(remaining, bitcriteria_function, position+1)

    def __get_oxygen_generator_rating(self) -> int:
        return self.__get_rating(self.report_lines, Submarine.__most_common)

    def __get_co2_scrubber_rating(self) -> int:
        return self.__get_rating(self.report_lines, Submarine.__least_common)


    def calculate_power_consumption(self) -> int:
        gamma, epsilon = "", ""

        for position in range(len(self.report_lines[0])):
            gamma += self.__most_common(line[position] for line in self.report_lines)
            epsilon += self.__least_common(line[position] for line in self.report_lines)

        return int(gamma,2) * int(epsilon,2)

    def calculate_life_support_rating(self) -> int:
        return self.__get_oxygen_generator_rating() * self.__get_co2_scrubber_rating()


if __name__ == "__main__":

    submarine = Submarine()

    with open(f"{os.path.dirname(os.path.realpath(__file__))}/input.txt", "r", encoding="UTF-8") as input:
        while (line := input.readline().rstrip()):
            submarine.report_lines.append(line)

        print("\nChallenge 1:")
        print(submarine.calculate_power_consumption())

        print("\nChallenge 2:")
        print(submarine.calculate_life_support_rating())
