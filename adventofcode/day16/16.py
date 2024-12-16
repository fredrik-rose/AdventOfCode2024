# Day 16: Reindeer Maze
import copy
import heapq
import os
import pathlib


def main():
    start, end, maze = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(start), copy.deepcopy(end), copy.deepcopy(maze))
    part_two(copy.deepcopy(start), copy.deepcopy(end), copy.deepcopy(maze))


def parse(file_path):
    maze = set()
    start = None
    end = None
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                position = x + y * 1j
                if char == ".":
                    maze.add(position)
                elif char == "S":
                    start = position
                    maze.add(position)
                elif char == "E":
                    end = position
                    maze.add(position)
                else:
                    assert char == "#", char
    assert start is not None
    assert end is not None
    return start, end, maze


def part_one(start, end, maze):
    neighbors, is_end = get_dijkstra_functions(maze, end)
    for _, distance in dijkstra_all((start, 1), neighbors, is_end):
        answer = distance
        break
    print(f"Part one: {answer}")


def part_two(start, end, maze):
    neighbors, is_end = get_dijkstra_functions(maze, end)
    nodes_on_shortest_paths = set()
    for path, _ in dijkstra_all((start, 1), neighbors, is_end):
        path = set(e[0] for e in path)
        nodes_on_shortest_paths.update(path)
    answer = len(nodes_on_shortest_paths)
    print(f"Part two: {answer}")


def get_dijkstra_functions(maze, end):
    def is_end(node):
        position, direction = node
        return position == end

    def neighbors(node):
        position, direction = node
        for next_direction in (-1, 1, -1j, 1j):
            next_position = position + next_direction
            if next_position not in maze:
                continue
            if next_direction == -direction:
                continue
            distance = 1
            if next_direction != direction:
                distance += 1000
            yield (next_position, next_direction), distance

    return neighbors, is_end


def dijkstra_all(start, neighbors, is_end, start_distance=0):
    counter = 0  # To support non-comparable types as nodes, e.g. complex numbers.
    queue = [(start_distance, counter, start, [start])]
    costs = {}
    min_distance = 1e9
    while queue:
        distance, _, node, visited = heapq.heappop(queue)
        if distance > min_distance:
            break
        if node in costs:
            assert costs[node] <= distance
            if distance > costs[node]:
                continue
        costs[node] = distance
        if is_end(node):
            min_distance = min(distance, min_distance)
            yield visited, distance
            continue
        for n, d in neighbors(node):
            counter += 1
            heapq.heappush(queue, (distance + d, counter, n, visited + [n]))


if __name__ == "__main__":
    main()
