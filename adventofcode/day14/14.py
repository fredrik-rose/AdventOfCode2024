# Day 14: Restroom Redoubt
import dataclasses
import collections
import copy
import math
import os
import pathlib
import re


WIDTH = 101
HEIGHT = 103


@dataclasses.dataclass
class Robot:
    position: complex
    veolicty: complex


def main():
    robots = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(robots))
    part_two(copy.deepcopy(robots))


def parse(file_path):
    robots = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            x, y, vx, vy = extract_ints(line)
            robots.append(Robot(x + y * 1j, vx + vy * 1j))
    return robots


def extract_ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def part_one(robots):
    simulate(robots, 100)
    quadrants = count_robots_in_quadrants(robots)
    answer = math.prod(quadrants.values())
    print(f"Part one: {answer}")


def part_two(robots):
    # For a random distribution of robots all quadrants should have roughly equal amount of robots.
    # The product of the quadrants should therefore be large. A Christmas tree on the other hand
    # should have few robots in the top quadrants and many in the bottom quadrants. This results
    # in a relatively smaller product.
    min_product = 1e9
    for i in range(WIDTH * HEIGHT):
        simulate(robots, 1)
        quadrants = count_robots_in_quadrants(robots)
        product = math.prod(quadrants.values())
        if product < min_product:
            min_product = product
            answer = i + 1
            display_robots(robots)
    print(f"Part two: {answer}")


def simulate(robots, time):
    for rob in robots:
        rob.position += rob.veolicty * time
        x = rob.position.real % WIDTH
        y = rob.position.imag % HEIGHT
        rob.position = x + y * 1j


def count_robots_in_quadrants(robots):
    quadrants = collections.defaultdict(int)
    for rob in robots:
        half_width = WIDTH // 2
        half_height = HEIGHT // 2
        if rob.position.real == half_width or rob.position.imag == half_height:
            continue
        q_x = rob.position.real // (half_width + 1)
        q_y = rob.position.imag // (half_height + 1)
        quadrants[(q_x, q_y)] += 1
    return quadrants


def display_robots(robots):
    positions = {rob.position for rob in robots}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            char = "#" if x + y * 1j in positions else " "
            print(char, end="")
        print("")


if __name__ == "__main__":
    main()
