import os
from typing import List
from dataclasses import dataclass, field

@dataclass
class Field():
    number: int
    marked: bool = False

@dataclass
class Board():
    fields: List[List[Field]] = field(default_factory=lambda: [])

    def __check_row(self, y_position: int) -> bool:
        for field in self.fields[y_position]:
            if field.marked == False:
                return False
        return True

    def __check_column(self, x_position: int) -> bool:
        for field in [row[x_position] for row in self.fields]:
            if field.marked == False:
                return False
        return True

    def __check_win(self, y_position: int, x_position: int) -> bool:
        return self.__check_row(y_position) or self.__check_column(x_position)

    def handle_number(self, number: int) -> bool:
        for row_index, row in enumerate(self.fields):
            for column_index, field in enumerate(row):
                if field.number == number:
                    field.marked = True
                    return self.__check_win(row_index, column_index)
        return False

    def calculate_unmarked_sum(self) -> int:
        result = 0
        for row in self.fields:
            for field in row:
                if field.marked == False:
                    result += field.number
        return result

@dataclass
class Bingo():
    drawn_numbers: List[int]
    boards: List[Board] = field(default_factory=lambda: [])

    def first_to_win(self):
        for number in self.drawn_numbers:
            for board in self.boards:
                if board.handle_number(number):
                    return board.calculate_unmarked_sum() * number

    def last_to_win(self):
        for number in self.drawn_numbers:
            indexes_to_delete = []
            for index, board in enumerate(self.boards):
                if board.handle_number(number):
                    indexes_to_delete.append(index)

            if len(indexes_to_delete) == 1 and len(self.boards) == 1:
                return self.boards[0].calculate_unmarked_sum() * number
            else:
                for index in sorted(indexes_to_delete, reverse=True):
                    self.boards.pop(index)


if __name__ == "__main__":

    with open(f"{os.path.dirname(os.path.realpath(__file__))}/input.txt", "r", encoding="UTF-8") as input:
        lines = input.readlines()
        bingo = Bingo(list([int(number) for number in lines[0].split(",")]))
        row = 1

        while True:
            row += 1
            if len(lines) < row:
                break

            board = Board()
            for i in range(5):
                board.fields.append(list([Field(int(number)) for number in lines[row].split()]))
                row += 1
            bingo.boards.append(board)

    print("\nChallenge 1:")
    print(bingo.first_to_win())

    print("\nChallenge 2:")
    print(bingo.last_to_win())
