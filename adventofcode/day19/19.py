# Day 19: Linen Layout
import copy
import os
import pathlib


def main():
    patterns, designs = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(patterns), copy.deepcopy(designs))
    part_two(copy.deepcopy(patterns), copy.deepcopy(designs))


def parse(file_path):
    patterns = []
    designs = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line:
                break
            patterns.extend(line.split(", "))
        for line in file:
            line = line.strip()
            designs.append(line)
    return patterns, designs


def part_one(patterns, designs):
    answer = sum(1 for d in designs if count_possible(d, patterns))
    print(f"Part one: {answer}")


def part_two(patterns, designs):
    answer = sum(count_possible(d, patterns) for d in designs)
    print(f"Part two: {answer}")


DP = {}


def count_possible(design, patterns):
    if not design:
        return 1
    if design in DP:
        return DP[design]
    DP[design] = sum(count_possible(design[len(p) :], patterns) for p in patterns if design.startswith(p))
    return DP[design]


if __name__ == "__main__":
    main()
