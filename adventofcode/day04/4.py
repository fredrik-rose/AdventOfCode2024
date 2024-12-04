# Day 4: Ceres Search
import copy
import os
import pathlib

import numpy as np

from scipy import ndimage


def main():
    word_search = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(word_search))
    part_two(copy.deepcopy(word_search))


def parse(file_path):
    word_search = []
    with open(file_path) as file:
        word_search = [[ord(e) for e in line.strip()] for line in file]
    return np.array(word_search, dtype=np.int64)


def part_one(word_search):
    def kernel(x):
        return 1 if is_word(x, "XMAS") else 0

    horizontal_footprint = np.ones((1, 4), dtype=np.int64)
    vertical_footprint = np.ones((4, 1), dtype=np.int64)
    diagonal_footprint = np.diag(np.ones(4, dtype=np.int64))
    anti_diagonal_footprint = np.fliplr(diagonal_footprint)
    answer = 0
    for footprint in (horizontal_footprint, vertical_footprint, diagonal_footprint, anti_diagonal_footprint):
        answer += np.sum(ndimage.generic_filter(word_search, kernel, footprint=footprint, mode="constant", cval=0))
    print(f"Part one: {answer}")


def part_two(word_search):
    def kernel(x):
        a = np.array([x[0], x[2], x[4]])
        b = np.array([x[1], x[2], x[3]])
        word = "MAS"
        return is_word(a, word) and is_word(b, word)

    footprint = np.array(
        [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
    )
    answer = np.sum(ndimage.generic_filter(word_search, kernel, footprint=footprint, mode="constant", cval=0))
    print(f"Part two: {answer}")


def is_word(x, word):
    x = "".join(chr(e) for e in x.astype(np.int64))
    return x in {word, word[::-1]}


if __name__ == "__main__":
    main()
