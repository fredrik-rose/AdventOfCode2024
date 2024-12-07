# Day 7: Bridge Repair
import copy
import operator
import os
import pathlib


def main():
    equations = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(equations))
    part_two(copy.deepcopy(equations))


def parse(file_path):
    equations = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            target, values = line.split(": ")
            equations.append((int(target), [int(e) for e in values.split(" ")]))
    return equations


def part_one(equations):
    operators = (operator.add, operator.mul)
    answer = solve_equations(equations, operators)
    print(f"Part one: {answer}")


def part_two(equations):
    def concatenate(a, b):
        return int(f"{a}{b}")

    operators = (operator.add, operator.mul, concatenate)
    answer = solve_equations(equations, operators)
    print(f"Part two: {answer}")


def solve_equations(equations, operators):
    answer = 0
    for target, values in equations:
        if is_solvable(target, operators, values[1:], values[0]):
            answer += target
    return answer


def is_solvable(target, operators, values, start):
    if not values:
        return start == target
    for op in operators:
        if is_solvable(target, operators, values[1:], op(start, values[0])):
            return True
    return False


if __name__ == "__main__":
    main()
