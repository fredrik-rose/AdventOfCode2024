# Day 18: RAM Run
import collections
import copy
import os
import pathlib


SIZE = 70
STEPS = 1024


def main():
    bits = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(bits))
    part_two(copy.deepcopy(bits))


def parse(file_path):
    bits = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            x, y = line.split(",")
            bits.append(int(x) + int(y) * 1j)
    return bits


def part_one(bits):
    grid = set(bits[:STEPS])
    answer = bfs(grid, 0, SIZE + SIZE * 1j)
    print(f"Part one: {answer}")


def part_two(bits):
    first_bit = binary_search(bits, 0, SIZE + SIZE * 1j)
    answer = f"{int(first_bit.real)},{int(first_bit.imag)}"
    print(f"Part two: {answer}")


def bfs(grid, start, end):
    queue = collections.deque([(0, start)])
    visited = set()
    while queue:
        distance, position = queue.popleft()
        if position in visited:
            continue
        visited.add(position)
        if position == end:
            return distance
        for direction in (-1, 1, -1j, 1j):
            next_position = position + direction
            if next_position in grid:
                continue
            if not (0 <= next_position.real <= SIZE and 0 <= next_position.imag <= SIZE):
                continue
            queue.append((distance + 1, next_position))
    return None


def binary_search(bits, start, end):
    left = 0
    right = len(bits) - 1
    while left < right:
        center = (right + left) // 2
        grid = set(bits[: center + 1])
        distance = bfs(grid, start, end)
        if distance is None:
            right = center
        else:
            left = center + 1
    return bits[left]


if __name__ == "__main__":
    main()
