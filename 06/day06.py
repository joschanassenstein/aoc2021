import os

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"


def default_population() -> dict:
    return {key: 0 for key in range(9)}

def run(filepath: str, days: int) -> int:

    population = default_population()

    with open(filepath, "r", encoding="UTF-8") as input:
        for fish in [int(initial_value) for initial_value in input.readline().rstrip().split(",")]:
            population[fish] += 1

    for day in range(days):
        updated_population = default_population()
        for subpopulation in population.keys():
            if subpopulation == 0:
                updated_population[6] += population[subpopulation]
                updated_population[8] += population[subpopulation]
            else:
                updated_population[subpopulation - 1] += population[subpopulation]
        population = updated_population

    return sum(population.values())


if __name__ == "__main__":
    assert run(EXAMPLE_PATH, 80) == 5934
    assert run(EXAMPLE_PATH, 256) == 26984457539

    print("\nChallenge 1:")
    print(run(INPUT_PATH, 80))

    print("\nChallenge 2:")
    print(run(INPUT_PATH, 256))
