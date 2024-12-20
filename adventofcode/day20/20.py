# Day 20: Race Condition
import collections
import copy
import os
import pathlib


def main():
    grid, start, end = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid), copy.deepcopy(start), copy.deepcopy(end))
    part_two(copy.deepcopy(grid), copy.deepcopy(start), copy.deepcopy(end))


def parse(file_path):
    grid = set()
    start = None
    end = None
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                position = x + y * 1j
                if char == "#":
                    continue
                if char == "S":
                    start = position
                elif char == "E":
                    end = position
                else:
                    assert char == "."
                grid.add(position)
    assert start is not None
    assert end is not None
    return grid, start, end


def part_one(grid, start, end):
    answer = solve(grid, start, end, 2)
    print(f"Part one: {answer}")


def part_two(grid, start, end):
    answer = solve(grid, start, end, 20)
    print(f"Part two: {answer}")


def solve(grid, start, end, max_cheat_length, min_save=100):
    start_distances = bfs(grid, start=start, end=end)
    end_distances = bfs(grid, start=end, end=start)
    cheats = cheat(grid, start_distances, end_distances, max_cheat_length)
    no_cheat_length = start_distances[end]
    saves = {no_cheat_length - length: count for length, count in cheats.items()}
    answer = sum(count for save, count in saves.items() if save >= min_save)
    return answer


def bfs(grid, start, end):
    queue = collections.deque([(0, start)])
    visited = {}
    while queue:
        distance, position = queue.popleft()
        if position in visited:
            continue
        visited[position] = distance
        if position == end:
            continue
        for n in (-1, 1, -1j, 1j):
            next_position = position + n
            if next_position in grid:
                queue.append((distance + 1, next_position))
    return visited


def cheat(grid, start_distances, end_distances, max_cheat_length):
    cheats = collections.defaultdict(int)
    for y in range(-max_cheat_length, max_cheat_length + 1):
        for x in range(-max_cheat_length, max_cheat_length + 1):
            cheat_length = abs(x) + abs(y)
            if not 2 <= cheat_length <= max_cheat_length:
                continue
            for start in grid:
                offset = x + y * 1j
                end = start + offset
                if end not in grid:
                    continue
                length = start_distances[start] + cheat_length + end_distances[end]
                cheats[length] += 1
    return cheats


if __name__ == "__main__":
    main()
