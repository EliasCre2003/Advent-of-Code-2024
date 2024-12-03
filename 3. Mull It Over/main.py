import re

def get_all_mull(text: str) -> list[str]:
    return re.findall(r"mul\(\d+,\d+\)", text)

def remove_first_occurence(string: str, regex: str) -> tuple[str, str]:
    match = re.search(regex, string)
    if match:
        return match.group(), re.sub(regex, '', string, count=1)
    return match, string

def parse_mull(string: str) -> tuple[int, int]:
    string = string.removeprefix("mul(")
    string = string.removesuffix(")")
    string = string.split(",")
    return int(string[0]), int(string[1])

def part1(input: str) -> str:
    mulls = [parse_mull(mull) for mull in get_all_mull(input)]
    return sum(mull[0] * mull[1] for mull in mulls)

def part2(input: str) -> str:
    mull = True
    total = 0
    while input:
        term, input = remove_first_occurence(input, r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
        if not term: break
        if term == "do()": mull = True
        elif term == "don't()": mull = False
        elif mull:
            mull = parse_mull(term)
            total += mull[0] * mull[1]
    return total

def main():
    with open("3. Mull It Over/input.txt", 'r') as f:
        lines = f.read()

    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(lines)}")

if __name__ == "__main__":
    main()