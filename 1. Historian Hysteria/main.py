
def part1(left: list[int], right: list[int]) -> int:
    return sum(abs(num1 - num2) for num1, num2 in zip(sorted(left), sorted(right)))

def part2(left: list[int], right: list[int]) -> int:
    return sum(num * right.count(num) for num in left)

def main():
    with open("1. Historian Hysteria/input.txt", "r") as f:
        lines = f.readlines()
    
    lines = [[int(num) for num in line.strip().split('   ')] for line in lines]
    left, right = list(zip(*lines))
    
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(left, right)}")

if __name__ == "__main__":
    main()