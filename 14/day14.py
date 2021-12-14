import os
from typing import Tuple, Dict

EXAMPLE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/example.txt"
INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

def parse_input(filepath: str) -> Tuple[Dict[str,Dict[str,int]], Dict[str,str]]:
    with open(filepath, "r", encoding="UTF-8") as input:
        pairings, rules = {}, {}

        for i in range(len(sequence := input.readline().rstrip()) - 1):
            update_pairing(pairings, sequence[i], sequence[i+1])
        input.readline()

        while (line := input.readline().rstrip()):
            pair, insertion = line.split(" -> ")
            rules[pair] = insertion

    return pairings, rules

def update_pairing(pairings: Dict[str,Dict[str,int]], left_element: str, right_element: str, count: int = 1) -> None:
    if left_element not in pairings:
        pairings[left_element] = {}
    if right_element not in pairings[left_element]:
        pairings[left_element][right_element] = count
    else:
        pairings[left_element][right_element] += count

def perform_insertion(pairings: Dict[str,Dict[str,int]], rules: Dict[str,str]) -> Dict[str,Dict[str,int]]:
    result = {}
    for left_element in pairings.keys():
        for right_element in pairings[left_element]:
            insert_element = rules[left_element + right_element]
            update_pairing(result, left_element, insert_element, pairings[left_element][right_element])
            update_pairing(result, insert_element, right_element, pairings[left_element][right_element])
    return result

def calculate_result(pairings: Dict[str,Dict[str,int]]) -> int:
    count = {}

    for element in pairings.keys():
        count[element] = 1

    for elements in pairings.values():
        for element in elements.keys():
            count[element] += elements[element]

    return max(count.values()) - min(count.values())

def run(filepath: str, iterations: int) -> int:
    pairings, rules = parse_input(filepath)
    for i in range(iterations):
        pairings = perform_insertion(pairings, rules)

    return calculate_result(pairings)


if __name__ == "__main__":
    assert run(EXAMPLE_PATH, 10) == 1588
    assert run(EXAMPLE_PATH, 40) == 2188189693529

    print("\nChallenge 1:")
    print(run(INPUT_PATH, 10))
    print("\nChallenge 2:")
    print(run(INPUT_PATH, 40))
