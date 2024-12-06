# Day 6: Guard Gallivant
import copy
import os
import pathlib


class Loop(Exception):
    pass


def main():
    start, grid = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(start), copy.deepcopy(grid))
    part_two(copy.deepcopy(start), copy.deepcopy(grid))


def parse(file_path):
    start = None
    grid = {}
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                position = x + y * 1j
                if char == "^":
                    start = position
                    char = "."
                assert char in {".", "#"}
                grid[position] = char
    return start, grid


def part_one(start, grid):
    answer = len(walk(start, grid))
    print(f"Part one: {answer}")


def part_two(start, grid):
    candidates = walk(start, grid)
    candidates.remove(start)
    answer = 0
    for position in candidates:
        grid[position] = "#"
        try:
            walk(start, grid)
        except Loop:
            answer += 1
        grid[position] = "."
    print(f"Part two: {answer}")


def walk(start, grid):
    position = start
    direction = -1j
    visited = set()
    while True:
        state = (position, direction)
        if state in visited:
            raise Loop
        visited.add(state)
        if position + direction not in grid:
            break
        if grid[position + direction] == "#":
            direction *= 1j
        else:
            position += direction
    return set(position for position, _ in visited)


if __name__ == "__main__":
    main()
