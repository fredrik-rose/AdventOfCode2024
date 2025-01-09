# Day 23: LAN Party
import collections
import os
import pathlib


def main():
    edges = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    graph = create_graph(edges)
    components = find_fully_connected_components(graph)
    # deepcopy is very slow, none of the parts are modifying 'components'
    part_one(components)
    part_two(components)


def parse(file_path):
    edges = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            first, second = line.split("-")
            edges.append((first, second))
    return edges


def create_graph(edges):
    graph = collections.defaultdict(set)
    for first, second in edges:
        graph[first].add(second)
        graph[second].add(first)
    return graph


def find_fully_connected_components(graph):
    components = set()
    for node, neighbors in graph.items():
        neighbors = list(neighbors)
        queue = collections.deque([(0, {node})])
        while queue:
            index, nodes = queue.popleft()
            if index == len(neighbors):
                components.add(tuple(sorted(nodes)))
                continue
            n = neighbors[index]
            if nodes <= graph[n]:
                queue.append((index + 1, nodes | {n}))
            queue.append((index + 1, nodes))
    return components


def part_one(components):
    valid_components = set()
    for c in components:
        if len(c) == 3 and any(e.startswith("t") for e in c):
            valid_components.add(c)
    answer = len(valid_components)
    print(f"Part one: {answer}")


def part_two(components):
    largest_component = []
    for c in components:
        if len(c) > len(largest_component):
            largest_component = c
    assert largest_component
    answer = ",".join(largest_component)
    print(f"Part two: {answer}")


if __name__ == "__main__":
    main()
