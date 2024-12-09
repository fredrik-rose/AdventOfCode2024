# Day 9: Disk Fragmenter
import copy
import os
import pathlib


class Node:
    def __init__(self, data, p=None, n=None):
        self.data = data
        self.p = p
        self.n = n

    def insert_before(self, data):
        node = Node(data, p=self.p, n=self)
        self.p.n = node
        self.p = node


def main():
    data = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(data))
    part_two(copy.deepcopy(data))


def parse(file_path):
    with open(file_path) as file:
        return [int(e) for e in file.readline().strip()]


def part_one(data):
    blocks = get_blocks(data)
    fixed_blocks = fix_blocks(blocks)
    answer = sum(i * block_id for i, block_id in enumerate(fixed_blocks))
    print(f"Part one: {answer}")


def part_two(data):
    files = get_files(data)
    fix_files(files[0], files[-1])
    answer = 0
    node = files[0]
    i = 0
    while node:
        file_id, size = node.data
        for _ in range(size):
            if file_id:
                answer += i * file_id
            i += 1
        node = node.n
    print(f"Part two: {answer}")


def get_blocks(data):
    blocks = []
    for i, n in enumerate(data):
        block_id = i // 2 if i % 2 == 0 else None
        for _ in range(n):
            blocks.append(block_id)
    return blocks


def fix_blocks(blocks):
    right = len(blocks) - 1
    fixed_blocks = []
    for left, block_id in enumerate(blocks):
        if left > right:
            break
        if block_id is None:
            fixed_blocks.append(blocks[right])
            right -= 1
            while blocks[right] is None:
                right -= 1
        else:
            fixed_blocks.append(block_id)
    return fixed_blocks


def get_files(data):
    files = [Node([0, data[0]])]
    for i, size in enumerate(data[1:]):
        i = i + 1
        block_id = i // 2 if i % 2 == 0 else None
        node = Node([block_id, size], p=files[-1])
        files[-1].n = node
        files.append(node)
    return files


def fix_files(first, last):
    while last.p:
        file_id, size = last.data
        if file_id:
            search = first
            while search is not last:
                candidate_file_id, candidate_size = search.data
                if candidate_file_id is None and candidate_size >= size:
                    search.insert_before([last.data[0], last.data[1]])
                    search.data[1] -= size
                    last.data[0] = None
                    break
                search = search.n
        last = last.p


if __name__ == "__main__":
    main()
