
def split_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str_stone := str(stone)) % 2 == 0:
        half_length = len(str_stone) // 2
        return [
            int(str_stone[:half_length]),
            int(str_stone[half_length:])
        ]
    else:
        return [stone * 2024]


def width_at_depth(stone: int, target_depth: int, cache: dict[tuple[int, int], int], current_depth: int = 0):
    if target_depth == current_depth:
        return 1
    if (stone, current_depth) in cache:
        return cache[(stone, current_depth)]
    result = sum(
        width_at_depth(stone, target_depth, cache, current_depth + 1) 
        for stone in split_stone(stone)
    )
    cache[(stone, current_depth)] = result
    return result


def main():
    with open('11. Plutonian Pebbles/input.txt', 'r') as f:
        stones = [int(n) for n in f.read().strip().split(' ')]
    for i, depth in enumerate([25, 75]):
        print(f"Part {i+1}: {sum(width_at_depth(stone, depth, cache={}) for stone in stones)}")


if __name__ == "__main__":
    main()
