# Day 3: Mull It Over
import copy
import os
import pathlib
import re


def main():
    instructions = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(instructions))
    part_two(copy.deepcopy(instructions))


def parse(file_path):
    with open(file_path) as file:
        instructions = [line.strip() for line in file]
    return instructions


def part_one(instructions):
    answer = 0
    for step in instructions:
        for a, b in re.findall(r"mul\((\d+)\,(\d+)\)", step):
            answer += int(a) * int(b)
    print(f"Part one: {answer}")


def part_two(instructions):
    answer = 0
    enabled = True
    for step in instructions:
        for match in re.finditer(r"mul\((\d+)\,(\d+)\)|(do)\(\)|(don't)\(\)", step):
            match_text = match.group(0)
            if match_text.startswith("don't"):
                enabled = False
            elif match_text.startswith("do"):
                enabled = True
            elif enabled:
                answer += int(match.group(1)) * int(match.group(2))
    print(f"Part two: {answer}")


if __name__ == "__main__":
    main()
