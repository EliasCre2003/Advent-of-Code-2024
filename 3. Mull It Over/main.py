from re import findall
from math import prod

def parse_mull(string: str) -> tuple[int, int]:
    string = string.removeprefix("mul(")
    string = string.removesuffix(")")
    string = string.split(",")
    return int(string[0]), int(string[1])

def part1(input: str) -> str:
    regex = r"mul\(\d+,\d+\)"
    mulls = [parse_mull(mull) for mull in findall(regex, input)]
    return sum(mull[0] * mull[1] for mull in mulls)

def part2(input: str) -> str:
    mull = True
    total = 0
    regex = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
    for term in findall(regex, input):
        match term:
            case "do()": mull = True
            case "don't()": mull = False
            case _:
                if not mull: continue
                total += prod(parse_mull(term))
    return total

def main():
    with open("3. Mull It Over/input.txt", 'r') as f:
        input = f.read()

    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(input)}")

if __name__ == "__main__":
    main()