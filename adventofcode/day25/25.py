# Day 25: Code Chronicle
import copy
import os
import pathlib

import numpy as np


def main():
    locks, keys = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(locks), copy.deepcopy(keys))


def parse(file_path):
    locks = []
    keys = []
    with open(file_path) as file:
        for text in file.read().strip().split("\n\n"):
            lines = text.split("\n")
            empty_counter = [0] * len(lines[0])
            fill_counter = [0] * len(lines[0])
            is_lock = all(e == "#" for e in lines[0])
            for line in lines:
                for i, char in enumerate(line):
                    if char == ".":
                        empty_counter[i] += 1
                    else:
                        assert char == "#"
                        fill_counter[i] += 1
            if is_lock:
                locks.append(np.array(empty_counter))
            else:
                keys.append(np.array(fill_counter))
    return locks, keys


def part_one(locks, keys):
    answer = sum(np.all(key <= lock) for key in keys for lock in locks)
    print(f"Part one: {answer}")


if __name__ == "__main__":
    main()
