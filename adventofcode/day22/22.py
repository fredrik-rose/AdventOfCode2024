# Day 22: Monkey Market
import os
import pathlib


def main():
    numbers = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    prices = generate_prices(numbers)
    # deepcopy is very slow, none of the parts are modifying 'prices'
    part_one(prices)
    part_two(prices)


def parse(file_path):
    with open(file_path) as file:
        return [int(line.strip()) for line in file]


def generate_prices(numbers, length=2000):
    prices = []
    for n in numbers:
        generator = pseudo_random(n)
        prices.append([next(generator) for _ in range(length)])
    return prices


def part_one(prices):
    answer = sum(e[-1][0] for e in prices)
    print(f"Part one: {answer}")


def part_two(prices):
    luts = [create_change_sequence_lut(e) for e in prices]
    answer = find_max_price(luts)
    print(f"Part two: {answer}")


def pseudo_random(number):
    digit = number % 10
    while True:
        next_number = ((number << 6) ^ number) & (2**24 - 1)
        next_number = ((next_number >> 5) ^ next_number) & (2**24 - 1)
        next_number = ((next_number << 11) ^ next_number) & (2**24 - 1)
        next_digit = next_number % 10
        diff = next_digit - digit
        number = next_number
        digit = next_digit
        yield number, digit, diff


def create_change_sequence_lut(sequence):
    lut = {}
    for a, b, c, d in zip(sequence[::], sequence[1::], sequence[2::], sequence[3::]):
        key = (a[2], b[2], c[2], d[2])
        if key in lut:
            continue
        lut[key] = d[1]
    return lut


def find_max_price(luts):
    candidate_sequences = set().union(*[e.keys() for e in luts])
    max_price = max(sum(e[sequence] for e in luts if sequence in e) for sequence in candidate_sequences)
    return max_price


if __name__ == "__main__":
    main()
