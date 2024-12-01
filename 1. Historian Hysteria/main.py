
def part1(left: list[int], right: list[int]) -> int:
    left, right = sorted(left), sorted(right)
    return sum(abs(num1 - num2) for num1, num2 in zip(left, right))

def part2(left: list[int], right: list[int]) -> int:
    left_map = {num: 0 for num in set(left)}
    for num in right:
        if num in left_map: left_map[num] += 1
    return sum(num * left_map[num] for num in left)

def main():
    with open("1. Historian Hysteria/input.txt", "r") as f:
        lines = f.readlines()
    
    lines = [line.strip().split('   ') for line in lines]
    left, right = [int(line[0]) for line in lines], [int(line[1]) for line in lines]
    
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(left, right)}")

if __name__ == "__main__":
    main()