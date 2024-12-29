from sys import setrecursionlimit


def next_number(number: int) -> int:
    for val in [1/64, 32, 1/2048]:
        number = (number ^ int(number / val)) % 16777216
    return number


def price_sequences(number: int, length: int) -> list[tuple[list[int], int]]:
    differences = [0] * length
    sequences: list[tuple[tuple[int], int]] = []
    last_price = last_digit(number)
    for i in range(length):
        new_number = next_number(number)
        price = last_digit(new_number)
        differences[i] = price - last_price
        last_price = price
        number = new_number
        if i >= 3: sequences.append((tuple(differences[i-3:i+1]), price))
    return sequences


def last_digit(number: int) -> int:
    return number % 10


def part1(numbers: list[int]) -> int:
    for _ in range(2000):
        numbers = map(next_number, numbers)
    return sum(numbers)


def part2(numbers: list[int]) -> int:
    num_sequences: dict[tuple[int], int] = {}
    for iteration, number in enumerate(numbers):
        sequences = price_sequences(number, 2000)
        if iteration == 0:
            for seq in sequences:
                if seq[0] in num_sequences: continue
                num_sequences[seq[0]] = seq[1]
            continue
        occured = set()
        for seq in sequences:
            if seq[0] not in num_sequences: continue
            if seq[0] in occured: continue
            occured.add(seq[0])
            num_sequences[seq[0]] += seq[1]
    return max(num_sequences.values())


def main():
    setrecursionlimit(10**6)
    with open('22. Monkey Market/input.txt', 'r') as f:
        lines = f.readlines()
    numbers = [int(line.strip()) for line in lines]
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(numbers)}")


if __name__ == "__main__":
    main()