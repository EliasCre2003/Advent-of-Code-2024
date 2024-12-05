
def parse_first(lines: list[str]) -> dict[int: set[int]]:
    ordering = {}
    for line in lines:
        pair = line.strip().split('|')
        num1, num2 = int(pair[0]), int(pair[1])
        if num1 in ordering:
            ordering[num1].add(num2)
        else:
            ordering[num1] = {num2}
    return ordering

def parse_second(lines: list[str]) -> list[list[str]]:
    return [[int(num) for num in line.strip().split(",")] 
            for line in lines]


def part1(ordering: dict[int: set[int]], updates: list[list[int]]) -> int:
    total = 0
    to_remove = []
    for update in updates:
        occured: set[int] = set()
        for num in update:
            if len(occured) == 0:
                occured.add(num)
            elif num not in ordering:
                occured.add(num)
            elif len(occured.intersection(ordering[num])) == 0:
                    occured.add(num)
            else:
                break
        else:
            total += update[len(update) // 2]
            to_remove.append(update)
    for update in to_remove:
        updates.remove(update)
    return total


def dfs(ordering: dict[int: set[int]], key: int) -> set[int]:
    afters: set = ordering[key]
    for k in afters:
        afters = afters.union(dfs(ordering, k))
    return afters


def part2(ordering: dict[int: set[int]], updates: list[list[int]]) -> int:
    total = 0
    


def main():
    with open("5/input.txt", 'r') as f:
        lines = f.readlines()
    
    sections = []
    for i, line in enumerate(lines):
        if line == '\n':
            sections.append(lines[:i])
            sections.append(lines[i+1:])
    sections = (parse_first(sections[0]), parse_second(sections[1]))

    print(part1(*sections))
    print(len(sections[1]))

    # for i, part in enumerate([part1, part2]):
    #     print(f"Part {i+1}: {part(parse_first(sections[0]), parse_second(sections[1]))}")

    print(dfs(sections[0], 95))

if __name__ == "__main__":
    main()
