import os
from typing import Generator, List, Optional, Tuple

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"


class Heightmap():
    def __init__(self, filepath: str):
        self.directions = [(0,1),(0,-1),(1,0),(-1,0)]
        self.heights = []

        with open(filepath, "r", encoding="UTF-8") as input:
            while (line := input.readline().rstrip()):
                self.heights.append([int(location) for location in line])

    def get_point_height(self, x: int, y: int) -> Optional[int]:
        if y in range(len(self.heights)) and x in range(len(self.heights[y])):
            return self.heights[y][x]
        return None

    def get_lowpoints(self) -> Generator[Tuple[int,int], None, None]:
        for y in range(len(self.heights)):
            for x in range(len(self.heights[y])):
                adjacents = [self.get_point_height(x+direction[0], y+direction[1]) for direction in self.directions]

                if min([height for height in adjacents if height != None]) > self.heights[y][x]:
                    yield (x,y)

    def get_basin_sizes(self) -> List[int]:
        basins = []

        for start_point in self.get_lowpoints():
            visited = []
            to_visit = [start_point]

            while to_visit:
                current_point = to_visit.pop(0)
                x,y = current_point
                current_height = self.heights[y][x]

                for dy, dx in self.directions:
                    if (adjacent_height := self.get_point_height(x+dx, y+dy)) != None:
                        if adjacent_height < 9 and adjacent_height >= current_height:
                            adjacent_point = (x+dx,y+dy)

                            if adjacent_point not in visited:
                                to_visit.append(adjacent_point)

                if current_point not in visited:
                    visited.append(current_point)

            basins.append(len(visited))
        return basins

    def calculate_risk_level(self) -> int:
        result = 0
        for point in self.get_lowpoints():
            result += self.heights[point[1]][point[0]] + 1
        return result

    def get_product_of_largest_basin_sizes(self, count: int) -> int:
        result = 1
        for size in sorted(self.get_basin_sizes())[-count:]:
            result *= size
        return result


if __name__ == "__main__":

    example_heightmap = Heightmap(EXAMPLE_PATH)
    assert example_heightmap.calculate_risk_level() == 15
    assert example_heightmap.get_product_of_largest_basin_sizes(3) == 1134

    heightmap = Heightmap(INPUT_PATH)
    print("\nChallenge 1:")
    print(heightmap.calculate_risk_level())
    print("\nChallenge 2:")
    print(heightmap.get_product_of_largest_basin_sizes(3))
