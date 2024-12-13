# Day 13: Claw Contraption
import dataclasses
import copy
import os
import pathlib
import re


@dataclasses.dataclass
class Pair:
    x: int
    y: int


@dataclasses.dataclass
class Record:
    button_a: Pair
    button_b: Pair
    prize: Pair


def main():
    data = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(data))
    part_two(copy.deepcopy(data))


def parse(file_path):
    data = []
    with open(file_path) as file:
        file_content = file.read().strip().split("\n\n")
        for record in file_content:
            button_a, button_b, prize = record.split("\n")
            data.append(
                Record(Pair(*extract_ints(button_a)), Pair(*extract_ints(button_b)), Pair(*extract_ints(prize)))
            )
    return data


def extract_ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def part_one(data):
    answer = get_solution(data, 100)
    print(f"Part one: {answer}")


def part_two(data):
    for record in data:
        record.prize.x += 10000000000000
        record.prize.y += 10000000000000
    answer = get_solution(data, None)
    print(f"Part two: {answer}")


def get_solution(data, limit):
    answer = 0
    for record in data:
        a, b = solve(record, limit)
        answer += 3 * a + b
    return answer


def solve(record, limit):
    ax = record.button_a.x
    ay = record.button_a.y
    bx = record.button_b.x
    by = record.button_b.y
    px = record.prize.x
    py = record.prize.y
    b_numerator = ay * px - ax * py
    b_denominator = ay * bx - ax * by
    if b_numerator % b_denominator != 0:
        return 0, 0
    b = b_numerator // b_denominator
    a_numerator = py - b * by
    a_denominator = ay
    if a_numerator % a_denominator != 0:
        return 0, 0
    a = a_numerator // a_denominator
    if limit is not None and (a > limit or b > limit):
        return 0, 0
    return a, b


if __name__ == "__main__":
    main()
