
def split_stones(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str_stone := str(stone)) % 2 == 0:
            half_length = len(str_stone) // 2
            new_stones.append(int(str_stone[:half_length]))
            new_stones.append(int(str_stone[half_length:]))
        else:
            new_stones.append(stone * 2024)
    return new_stones

def split_stones_n_times(stones: list[int], n: int) -> list[int]:
    for _ in range(n):
        stones = split_stones(stones)
    return stones

def part1(stones: list[int]) -> int:
    return len(split_stones_n_times(stones, 25))    


def part2() -> int:
    ...


def main():
    with open('11. Plutonian Pebbles/input.txt', 'r') as f:
        stones = [int(n) for n in f.read().strip().split(' ')]

    print(part1(stones))

if __name__ == "__main__":
    main()
