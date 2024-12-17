# Day 17: Chronospatial Computer
import dataclasses
import copy
import os
import pathlib


@dataclasses.dataclass
class Instruction:
    opcode: int
    operand: int


class Computer:
    def __init__(self):
        self.env = None
        self.ip = 0
        self.output = []

    def run(self, instructions, registers):
        self.env = registers
        self.ip = 0
        while self.ip < len(instructions):
            inst = instructions[self.ip]
            should_step = {
                0: self.adv,
                1: self.bxl,
                2: self.bst,
                3: self.jnz,
                4: self.bxc,
                5: self.out,
                6: self.bdv,
                7: self.cdv,
            }[inst.opcode](inst.operand)
            if should_step:
                self.ip += 1
        return self.output

    def get_operand(self, combo_operand):
        if 0 <= combo_operand <= 3:
            return combo_operand
        elif combo_operand == 4:
            return self.env["A"]
        elif combo_operand == 5:
            return self.env["B"]
        elif combo_operand == 6:
            return self.env["C"]
        else:
            assert False, combo_operand

    def adv(self, operand):
        operand = self.get_operand(operand)
        self.env["A"] = self.env["A"] // 2**operand
        return True

    def bxl(self, operand):
        self.env["B"] = self.env["B"] ^ operand
        return True

    def bst(self, operand):
        operand = self.get_operand(operand)
        self.env["B"] = operand % 8
        return True

    def jnz(self, operand):
        if self.env["A"] == 0:
            return True
        self.ip = operand
        return False

    def bxc(self, operand):
        self.env["B"] = self.env["B"] ^ self.env["C"]
        return True

    def out(self, operand):
        operand = self.get_operand(operand)
        self.output.append(operand % 8)
        return True

    def bdv(self, operand):
        operand = self.get_operand(operand)
        self.env["B"] = self.env["A"] // 2**operand
        return True

    def cdv(self, operand):
        operand = self.get_operand(operand)
        self.env["C"] = self.env["A"] // 2**operand
        return True


def main():
    registers, instructions = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(registers), copy.deepcopy(instructions))
    part_two(copy.deepcopy(registers), copy.deepcopy(instructions))


def parse(file_path):
    registers = {}
    instructions = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line:
                break
            name, value = line.split(": ")
            registers[name[-1]] = int(value)
        program = file.readline().strip().split(": ")[1].split(",")
        for opcode, operand in zip(program[:-1:2], program[1::2]):
            instructions.append(Instruction(int(opcode), int(operand)))
    return registers, instructions


def part_one(registers, instructions):
    output = Computer().run(instructions, registers)
    answer = ",".join(str(e) for e in output)
    print(f"Part one: {answer}")


def part_two(registers, instructions):
    sequence = []
    for inst in instructions:
        sequence.append(inst.opcode)
        sequence.append(inst.operand)
    answer = solve(registers, instructions, sequence)
    print(f"Part two: {answer}")


def solve(registers, program, sequence, start=0):
    if not sequence:
        return start
    target = sequence[-1]
    for i in range(8):
        value = (start << 3) + i
        new_registers = dict(registers)
        new_registers["A"] = value
        output = Computer().run(program, new_registers)[0]
        if output != target:
            continue
        solution = solve(registers, program, sequence[:-1], value)
        if solution is not None:
            return solution
    return None


if __name__ == "__main__":
    main()
