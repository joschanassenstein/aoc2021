import os
from typing import List, Tuple, Union

INPUT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"

def parse_input(filepath: str) -> str:
    with open(filepath, "r", encoding="UTF-8") as f:
        return "".join([bin(int(hex, 16))[2:].zfill(4) for hex in f.readline().strip()])

def parse_packet(payload: str, index: int, version_numbers: List[int]) -> Union[int,Tuple[int,int]]:
    if "1" not in payload:
        return index
    if index >= len(payload):
        return index

    version = payload[index:index+3]
    type_id = payload[index+3:index+6]

    version_numbers.append(int(version, 2))

    if type_id == "100":
        end_index, value = parse_literal_groups(payload, index + 6)
        return end_index, value

    length_type = payload[index+6]
    subvalues = []
    parsed_index = None
    if length_type == "0":
        total_length = int(payload[index+7:index+22], 2)
        parsed_index = index + 22
        while parsed_index < index + 22 + total_length:
            parsed_index, value = parse_packet(payload, parsed_index, version_numbers)
            subvalues.append(value)
    elif length_type == "1":
        packet_count = int(payload[index+7:index+18], 2)
        parsed_index = index + 18
        for i in range(packet_count):
            parsed_index, value = parse_packet(payload, parsed_index, version_numbers)
            subvalues.append(value)

    value = None
    if type_id == "000":
        value = sum(subvalues)
    elif type_id == "001":
        value = 1
        for subvalue in subvalues:
            value *= subvalue
    elif type_id == "010":
        value = min(subvalues)
    elif type_id == "011":
        value = max(subvalues)
    elif type_id == "101":
        value = 1 if subvalues[0] > subvalues[1] else 0
    elif type_id == "110":
        value = 1 if subvalues[0] < subvalues[1] else 0
    elif type_id == "111":
        value = 1 if subvalues[0] == subvalues[1] else 0

    return parsed_index, value

def parse_literal_groups(payload: str, index: int) -> Tuple[int,int]:
    group = payload[index : index + 5]
    binary = ""
    while True:
        binary += group[1:]
        if group[0] == "0":
            break
        index += 5
        group = payload[index : index + 5]
    return index + 5, int(binary, 2)


if __name__ == "__main__":

    payload = parse_input(INPUT_PATH)
    version_numbers = []
    index, value = parse_packet(payload, 0, version_numbers)
    print("\nChallenge 1:")
    print(sum(version_numbers))
    print("\nChallenge 2:")
    print(value)
