# Day 15: Warehouse Woes
import dataclasses
import copy
import os
import pathlib


@dataclasses.dataclass
class Box:
    left: complex
    right: complex


def main():
    start, walls, boxes, directions = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(start), copy.deepcopy(walls), copy.deepcopy(boxes), copy.deepcopy(directions))
    part_two(copy.deepcopy(start), copy.deepcopy(walls), copy.deepcopy(boxes), copy.deepcopy(directions))


def parse(file_path):
    walls = set()
    boxes = set()
    start = None
    directions = []
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            if not line:
                break
            for x, char in enumerate(line):
                position = x + y * 1j
                if char == "#":
                    walls.add(position)
                elif char == "O":
                    boxes.add(position)
                elif char == "@":
                    assert start is None
                    start = position
                else:
                    assert char == ".", char
        for line in file:
            line = line.strip()
            for char in line:
                direction = {
                    "<": -1,
                    ">": 1,
                    "^": -1j,
                    "v": 1j,
                }[char]
                directions.append(direction)
    return start, walls, boxes, directions


def part_one(start, walls, boxes, directions):
    def push_box(position, direction):
        last_box_position = position
        while last_box_position in boxes:
            last_box_position += direction
        if last_box_position in walls:
            return False
        boxes.remove(position)
        boxes.add(last_box_position)
        return True

    simulate(start, walls, boxes, directions, push_box)
    answer = sum(int(100 * box.imag + box.real) for box in boxes)
    print(f"Part one: {answer}")


def part_two(start, walls, boxes, directions):
    def push_box(position, direction):
        push = push_boxes_two(boxes[position], direction, walls, boxes)
        should_move = next(push)
        if should_move:
            next(push)
            push.send(True)
            return True
        return False

    start, walls, boxes = extend(start, walls, boxes)
    simulate(start, walls, boxes, directions, push_box)
    answer = sum(int(100 * box.left.imag + box.left.real) for position, box in boxes.items() if position.real % 2 != 0)
    print(f"Part two: {answer}")
    print_grid(start, walls, boxes)


def simulate(start, walls, boxes, directions, push_box):
    position = start
    for direction in directions:
        next_position = position + direction
        if next_position in walls:
            continue
        if next_position in boxes and not push_box(next_position, direction):
            continue
        position = next_position


def extend(start, walls, boxes):
    def get_new_position(position):
        return (position.real * 2) + position.imag * 1j

    new_start = get_new_position(start)
    new_walls = set()
    new_boxes = {}
    for wall in walls:
        left = get_new_position(wall)
        right = left + 1
        new_walls.add(left)
        new_walls.add(right)
    for box in boxes:
        left = get_new_position(box)
        right = left + 1
        box_object = Box(left, right)
        new_boxes[left] = box_object
        new_boxes[right] = box_object
    return new_start, new_walls, new_boxes


def push_boxes_two(box, direction, walls, boxes):
    assert boxes[box.left] is box
    assert boxes[box.right] is box
    next_left = box.left + direction
    next_right = box.right + direction
    left = None
    right = None
    left_ok = True
    right_ok = True
    if next_left in walls:
        left_ok = False
    elif next_left in boxes and boxes[next_left] is not box:
        left = push_boxes_two(boxes[next_left], direction, walls, boxes)
        left_ok = next(left)
    if next_right in walls:
        right_ok = False
    elif next_right in boxes and boxes[next_right] is not box:
        right = push_boxes_two(boxes[next_right], direction, walls, boxes)
        right_ok = next(right)
    if left_ok and right_ok:
        yield True
        should_move = yield
        if should_move:
            if left:
                next(left)
                left.send(True)
            if right:
                next(right)
                right.send(True)
            del boxes[box.left]
            del boxes[box.right]
            box.left = next_left
            box.right = next_right
            assert box.left not in boxes
            assert box.right not in boxes
            boxes[box.left] = box
            boxes[box.right] = box
    yield False


def print_grid(start, walls, boxes):
    height = int(max(e.imag for e in walls))
    width = int(max(e.real for e in walls))
    for y in range(height + 1):
        for x in range(width + 1):
            position = x + y * 1j
            if position in walls:
                char = "#"
            elif position in boxes:
                box = boxes[position]
                char = "[" if position == box.left else "]"
            elif position == start:
                char = "@"
            else:
                char = "."
            print(char, end="")
        print("")


if __name__ == "__main__":
    main()
