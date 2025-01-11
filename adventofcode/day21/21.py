# Day 21: Keypad Conundrum
import collections
import copy
import os
import pathlib


DIRECTIONS = {
    -1: "<",
    1: ">",
    -1j: "^",
    1j: "v",
}

NUMERIC_KEYPAD = {
    0 + 0j: "7",
    1 + 0j: "8",
    2 + 0j: "9",
    0 + 1j: "4",
    1 + 1j: "5",
    2 + 1j: "6",
    0 + 2j: "1",
    1 + 2j: "2",
    2 + 2j: "3",
    1 + 3j: "0",
    2 + 3j: "A",
}

DIRECTION_KEYPAD = {
    1 + 0j: "^",
    2 + 0j: "A",
    0 + 1j: "<",
    1 + 1j: "v",
    2 + 1j: ">",
}


def main():
    data = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(data))
    part_two(copy.deepcopy(data))


def parse(file_path):
    data = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            data.append(list(line))
    return data


def part_one(data):
    answer = sovle(data, 2)
    print(f"Part one: {answer}")


def part_two(data):
    answer = sovle(data, 25)
    print(f"Part two: {answer}")


def sovle(data, num_direction_keypads):
    shortest_paths_numeric = find_shortest_paths(NUMERIC_KEYPAD)
    shortest_paths_direction = find_shortest_paths(DIRECTION_KEYPAD)
    shortest_paths = {n: shortest_paths_direction for n in range(0, num_direction_keypads + 1)}
    shortest_paths[num_direction_keypads] = shortest_paths_numeric
    answer = 0
    for buttons in data:
        buttons = ["A", *buttons]
        for a, b in zip(buttons[:-1], buttons[1:]):
            answer += find_distance(a, b, shortest_paths, num_direction_keypads) * int("".join(buttons[1:-1]))
    return answer


def find_shortest_paths(keypad):
    buttons = keypad.values()
    positions = {position: button for button, position in keypad.items()}
    shortest_paths = {}
    for a in buttons:
        for b in buttons:
            start = positions[a]
            end = positions[b]
            shortest_paths[(a, b)] = bfs_all(start, end, keypad)
            for path in shortest_paths[(a, b)]:
                path.append("A")
    return shortest_paths


def bfs_all(start, end, keypad):
    queue = collections.deque([(start, [])])
    visited = set()
    min_distance = float("inf")
    shortest_paths = []
    while queue:
        node, path = queue.popleft()
        distance = len(path)
        if distance > min_distance:
            continue
        if node in visited:
            continue
        if node == end:
            min_distance = distance
            shortest_paths.append(path)
        for d, s in DIRECTIONS.items():
            next_node = node + d
            if next_node not in keypad:
                continue
            queue.append((next_node, [*path, s]))
    return shortest_paths


DP = {}


def find_distance(a, b, shortest_paths_for_levels, level):
    state = (a, b, level)
    if state in DP:
        return DP[state]
    shortest_paths = shortest_paths_for_levels[level]
    if level == 0:
        return len(shortest_paths[(a, b)][0])
    shortest = float("inf")
    for candidates in shortest_paths[(a, b)]:
        candidates = ["A", *candidates]
        distance = 0
        for x, y in zip(candidates[:-1], candidates[1:]):
            distance += find_distance(x, y, shortest_paths_for_levels, level - 1)
        shortest = min(shortest, distance)
    DP[state] = shortest
    return shortest


if __name__ == "__main__":
    main()
