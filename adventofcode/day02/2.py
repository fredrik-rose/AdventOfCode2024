# Day 2: Red-Nosed Reports
import copy
import os
import pathlib

import numpy as np


def main():
    reports = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(reports))
    part_two(copy.deepcopy(reports))


def parse(file_path):
    reports = []
    with open(file_path) as file:
        for line in file:
            level = [int(e) for e in line.strip().split()]
            reports.append(level)
    return reports


def part_one(reports):
    answer = sum(is_levels_safe(levels) for levels in reports)
    print(f"Part one: {answer}")


def part_two(reports):
    answer = 0
    for levels in reports:
        if is_levels_safe(levels) or any(is_levels_safe(levels[:i] + levels[i + 1 :]) for i in range(len(levels))):
            answer += 1
    print(f"Part two: {answer}")


def is_levels_safe(levels):
    diffs = np.diff(np.array(levels))
    safe = np.all(np.abs(diffs) <= 3) and (np.all(diffs < 0) or np.all(diffs > 0))
    return safe


if __name__ == "__main__":
    main()
