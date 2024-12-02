# Day 1: Historian Hysteria
import collections
import copy
import os
import pathlib


def main():
    first, second = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(first), copy.deepcopy(second))
    part_two(copy.deepcopy(first), copy.deepcopy(second))


def parse(file_path):
    first = []
    second = []
    with open(file_path) as file:
        for line in file:
            a, b = line.strip().split()
            first.append(int(a))
            second.append(int(b))
    return first, second


def part_one(first, second):
    answer = sum(abs(a - b) for a, b in zip(sorted(first), sorted(second)))
    print(f"Part one: {answer}")


def part_two(first, second):
    left = collections.Counter(second)
    answer = sum(a * left[a] for a in first)
    print(f"Part two: {answer}")


if __name__ == "__main__":
    main()
