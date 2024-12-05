# Day 5: Print Queue
import collections
import copy
import functools
import os
import pathlib


def main():
    ordering, updates = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(ordering), copy.deepcopy(updates))
    part_two(copy.deepcopy(ordering), copy.deepcopy(updates))


def parse(file_path):
    ordering = collections.defaultdict(set)
    updates = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line:
                break
            a, b = line.split("|")
            ordering[int(a)].add(int(b))
        for line in file:
            updates.append([int(n) for n in line.strip().split(",")])
    return ordering, updates


def part_one(ordering, updates):
    answer, _ = solve(ordering, updates)
    print(f"Part one: {answer}")


def part_two(ordering, updates):
    _, answer = solve(ordering, updates)
    print(f"Part two: {answer}")


def solve(ordering, updates):
    def compare(a, b):
        return 1 if a in ordering[b] else -1

    valid = 0
    invalid = 0
    for update in updates:
        assert len(update) % 2 == 1
        ordered = sorted(update, key=functools.cmp_to_key(compare))
        center = ordered[len(ordered) // 2]
        if update == ordered:
            valid += center
        else:
            invalid += center
    return valid, invalid


if __name__ == "__main__":
    main()
