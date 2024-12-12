# Day 12: Garden Groups
import collections
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
                grid[position] = char
    return grid


def part_one(grid):
    answer = sum(len(area) * len(perimiter) for area, perimiter in iterate_areas(grid))
    print(f"Part one: {answer}")


def part_two(grid):
    answer = 0
    for area, perimiter in iterate_areas(grid):
        perimiter_grid = {p: "X" for p in perimiter}
        sides = sum(1 for _ in iterate_areas(perimiter_grid))
        answer += len(area) * sides
    print(f"Part two: {answer}")


def iterate_areas(grid):
    visited = set()
    for position in grid:
        if position in visited:
            continue
        area, perimiter = flood_fill(position, grid)
        visited.update(area)
        yield area, perimiter


def flood_fill(start, grid):
    plant = grid[start]
    queue = collections.deque([start])
    visited = set()
    perimiter = set()
    while queue:
        position = queue.popleft()
        if position in visited:
            continue
        visited.add(position)
        assert grid[position] == plant
        directions = (-1, 1, -1j, 1j)
        for d in directions:
            neighbor = position + d
            if neighbor not in grid or grid[neighbor] != plant:
                perimiter.add(position + d * 0.25)
                continue
            queue.append(neighbor)
    return visited, perimiter


if __name__ == "__main__":
    main()
