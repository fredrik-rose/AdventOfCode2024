# Day 11: Plutonian Pebbles
import collections
import copy
import os
import pathlib


def main():
    stones = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(stones))
    part_two(copy.deepcopy(stones))


def parse(file_path):
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            return [int(e) for e in line.split()]


def part_one(stones):
    answer = solve(stones, 25)
    print(f"Part one: {answer}")


def part_two(stones):
    answer = solve(stones, 75)
    print(f"Part two: {answer}")


def solve(stones, steps):
    return sum(expand_stone(s, steps) for s in stones)


def expand_stone(stone, steps):
    stones = {stone: 1}
    for _ in range(steps):
        new_stones = collections.defaultdict(int)
        for s, n in stones.items():
            str_s = str(s)
            if s == 0:
                new_stones[1] += n
            elif len(str_s) % 2 == 0:
                half = len(str_s) // 2
                new_stones[int(str_s[:half])] += n
                new_stones[int(str_s[half:])] += n
            else:
                new_stones[s * 2024] += n
        stones = new_stones
    return sum(n for n in stones.values())


if __name__ == "__main__":
    main()
