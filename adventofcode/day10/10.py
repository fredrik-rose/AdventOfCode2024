# Day 10: Hoof It
import copy
import os
import pathlib


def main():
    grid = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid))
    part_two(copy.deepcopy(grid))


def parse(file_path):
    grid = {}
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                position = x + y * 1j
                grid[position] = int(char)
    return grid


def part_one(grid):
    answer = sum(len(set(e)) for e in get_trails(grid))
    print(f"Part one: {answer}")


def part_two(grid):
    answer = sum(len(e) for e in get_trails(grid))
    print(f"Part two: {answer}")


def get_trails(grid):
    trail_heads = [position for position, height in grid.items() if height == 0]
    return [walk_summits(trail, grid) for trail in trail_heads]


def walk_summits(start, grid):
    height = grid[start]
    if height == 9:
        return [start]
    directions = (-1, 1, -1j, 1j)
    summits = []
    for d in directions:
        position = start + d
        if position not in grid:
            continue
        if grid[position] != height + 1:
            continue
        score = walk_summits(position, grid)
        summits.extend(score)
    return summits


if __name__ == "__main__":
    main()
