# Day 8: Resonant Collinearity
import collections
import copy
import os
import pathlib


def main():
    antennas, height, width = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(antennas), copy.deepcopy(height), copy.deepcopy(width))
    part_two(copy.deepcopy(antennas), copy.deepcopy(height), copy.deepcopy(width))


def parse(file_path):
    antennas = collections.defaultdict(list)
    height = 0
    width = 0
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            height = y + 1
            for x, char in enumerate(line):
                width = x + 1
                if char != ".":
                    position = x + y * 1j
                    antennas[char].append(position)
    return list(antennas.values()), height, width


def part_one(antennas, height, width):
    antinodes = set().union(*(get_antinodes(positions) for positions in antennas))
    antinodes = [e for e in antinodes if 0 <= e.real < width and 0 <= e.imag < height]
    answer = len(antinodes)
    print(f"Part one: {answer}")


def part_two(antennas, height, width):
    lines = set().union(*(get_lines(positions) for positions in antennas))
    answer = 0
    for y in range(height):
        for x in range(width):
            for a, b, c in lines:
                if a * x + b * y + c == 0:  # Check if point (x, y) is on line parameterized with (a, b, c).
                    answer += 1
                    break
    print(f"Part two: {answer}")


def get_antinodes(antenna_positions):
    antinodes = set()
    for first in antenna_positions:
        for second in antenna_positions:
            if first == second:
                continue
            vector = second - first
            antinodes.add(first - vector)
    return antinodes


def get_lines(antenna_positions):
    # Representation: ax + by + c = 0
    # a = y0 - y1, b = x1 - x0, c = x0*y1 - x1*y0.
    lines = set()
    for i, first in enumerate(antenna_positions):
        for second in antenna_positions[i + 1 :]:
            a = first.imag - second.imag
            b = second.real - first.real
            c = first.real * second.imag - second.real * first.imag
            lines.add((a, b, c))
    return lines


if __name__ == "__main__":
    main()
