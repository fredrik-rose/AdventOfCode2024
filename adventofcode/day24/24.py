# Day 24: Crossed Wires
import collections
import copy
import operator
import os
import pathlib


def main():
    wires, gates, operators = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(wires), copy.deepcopy(gates), copy.deepcopy(operators))
    part_two(copy.deepcopy(wires), copy.deepcopy(gates), copy.deepcopy(operators))


def parse(file_path):
    wires = {}
    gates = {}
    operators = {}
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line:
                break
            name, value = line.split(": ")
            wires[name] = int(value)
        for line in file:
            line = line.strip()
            rest, output = line.split(" -> ")
            a, op, b = rest.split(" ")
            gates[output] = (a, b)
            if op == "AND":
                operators[output] = operator.and_
            elif op == "OR":
                operators[output] = operator.or_
            elif op == "XOR":
                operators[output] = operator.xor
            else:
                assert False
    return wires, gates, operators


def part_one(wires, gates, operators):
    answer = simulate(wires, gates, operators)
    print(f"Part one: {answer}")


def part_two(wires, gates, operators):
    swaps = fix_errors(wires, gates, operators)
    answer = ",".join(sorted(swaps))
    print(f"Part two: {answer}")


def simulate(wires, gates, operators):
    graph = build_graph(gates)
    queue = collections.deque(list(wires.items()))
    activations = collections.defaultdict(list)
    while queue:
        name, value = queue.popleft()
        for node in graph[name]:
            node_inputs = activations[node]
            node_inputs.append(value)
            if len(node_inputs) == 2:
                activations[node] = operators[node](*node_inputs)
                queue.append((node, activations[node]))
    if not all(isinstance(e, int) for e in activations.values()):
        return None
    output = [str(value) for name, value in reversed(sorted(activations.items())) if name.startswith("z")]
    return int("".join(output), 2)


def build_graph(gates):
    graph = collections.defaultdict(set)
    for output, (a, b) in gates.items():
        graph[a].add(output)
        graph[b].add(output)
    return graph


def fix_errors(wires, gates, operators, progress=0):
    print(f"Step: {progress}/44", flush=True)
    if progress == 44:
        return set()
    if is_valid(wires, gates, operators, progress):
        return fix_errors(wires, gates, operators, progress + 1)
    print("Error detected, trying to fix it.")
    candidates = list(gates.keys())
    for i, a in enumerate(candidates):
        for b in candidates[i + 1 :]:
            if a == b:
                continue
            swap_keys(gates, a, b)
            swap_keys(operators, a, b)
            if is_valid(wires, gates, operators, progress):
                print(f"Trying to swap {a} with {b}.")
                swaps = fix_errors(wires, gates, operators, progress + 1)
                if swaps is not None:
                    return swaps | {a, b}
                print("Did not work, backtrack.")
            swap_keys(gates, a, b)
            swap_keys(operators, a, b)
    return None


def is_valid(wires, gates, operators, progress):
    wires = {name: 0 for name in wires.keys()}
    for i in range(progress + 1):
        wires[f"x{i:02d}"] = 1
        wires[f"y{i:02d}"] = 1
    x = set_n_bits(progress + 1)
    mask = set_n_bits(progress + 2)  # Include carry bit.
    for i in range(progress + 1):
        wires[f"y{progress - i:02d}"] = 0
        z_sim = simulate(wires, gates, operators)
        if z_sim is None:
            return False
        z_sim = z_sim & mask
        y = set_n_bits(progress - i)
        z = x + y
        if z != z_sim:
            return False
    return True


def set_n_bits(n):
    return 2**n - 1


def swap_keys(dictionary, a, b):
    dictionary[a], dictionary[b] = dictionary[b], dictionary[a]


if __name__ == "__main__":
    main()
