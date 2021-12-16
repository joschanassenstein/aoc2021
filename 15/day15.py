import os
from queue import PriorityQueue
from typing import List

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

def parse_input(filepath: str) -> List[List[int]]:
    with open(filepath, "r", encoding="UTF-8") as f:
        return [list(map(int, line)) for line in f.read().splitlines()]

def extend_matrix(matrix: List[List[int]]) -> List[List[int]]:
    new_weight =  {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 1}
    extended_matrix = [row.copy() for row in matrix]

    for factor in range(4):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                extended_matrix[i].append(new_weight[extended_matrix[i][j + len(matrix) * factor]])
    for factor in range(4):
        for i in range(len(matrix)):
            new_list = list()
            for j in range(len(extended_matrix[0])):
                new_list.append(new_weight[extended_matrix[i + len(matrix) * factor][j]])
            extended_matrix.append(new_list)

    return extended_matrix

def find_path(matrix: List[List[int]]) -> int:
    height, width = len(matrix), len(matrix[0])
    queue = PriorityQueue()
    queue.put((0, (0, 0)))
    visited = {(0, 0)}

    while queue:
        risk, (i, j) = queue.get()

        if i == height - 1 and j == width - 1:
            return risk

        for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if 0 <= x < height and 0 <= y < width and (x, y) not in visited:
                weight = matrix[x][y]
                queue.put((risk + weight, (x, y)))
                visited.add((x, y))


if __name__ == "__main__":
    example_matrix = parse_input(EXAMPLE_PATH)
    assert find_path(example_matrix) == 40
    assert find_path(extend_matrix(example_matrix)) == 315

    matrix = parse_input(INPUT_PATH)
    print("\nChallenge 1:")
    print(find_path(matrix))
    print("\nChallenge 2:")
    print(find_path(extend_matrix(matrix)))
