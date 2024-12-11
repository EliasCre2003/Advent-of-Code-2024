from math import floor, log10
from time import time


def split_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    n_digits = floor(log10(stone)) + 1
    if n_digits % 2 == 0:
        tens = 10 ** (n_digits // 2)
        return [
            stone // tens,
            stone % tens
        ]    
    return [stone * 2024]


def width_at_depth(stone: int, target_depth: int, cache: dict[tuple[int, int], int], current_depth: int = 0):
    if target_depth == current_depth:
        return 1
    key = (stone, target_depth - current_depth)
    if key in cache:
        return cache[key]
    result = sum(
        width_at_depth(stone, target_depth, cache, current_depth + 1) 
        for stone in split_stone(stone)
    )
    cache[key] = result
    return result


def main():
    with open('11. Plutonian Pebbles/input.txt', 'r') as f:
        stones = [int(n) for n in f.read().strip().split(' ')]
    cache: dict[tuple[int, int], int] = {}
    total_time = 0
    for i, depth in enumerate([25, 75]):
        start = time()
        result = sum(width_at_depth(stone, depth, cache) for stone in stones)
        runtime = time() - start
        total_time += runtime
        print(f"Part {i+1}: {result}, Runtime: {round(runtime, 4)}s")
    print(f"Total runtime: {round(total_time, 4)}")


if __name__ == "__main__":
    main()
