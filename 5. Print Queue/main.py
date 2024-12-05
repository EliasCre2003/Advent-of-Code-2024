
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


def dfs(ordering: dict[int: set[int]], key: int, update: list[int], cache: dict[(int, list[int]), set[int]] ={}) -> set[int]:
    if (key, tuple(update)) in cache:
        return cache[(key, tuple(update))]
    if key not in ordering:
        return set()
    afters: set[int] = ordering[key]
    for k in afters:
        if k not in update: continue
        afters = afters.union(dfs(ordering, k, update))
    cache[(key, tuple(update))] = afters
    return afters


def part2(ordering: dict[int: set[int]], updates: list[list[int]]) -> int:
    total = 0
    for update in updates:
        lens = {k: len(dfs(ordering, k, update)) for k in update}
        update = list(reversed(sorted(update, key=lambda x: lens[x])))
        total += update[len(update) // 2]
    return total


def main():
    with open("5. Print Queue/test.txt", 'r') as f:
        lines = f.readlines()
    
    sections = []
    for i, line in enumerate(lines):
        if line == '\n':
            sections.append(lines[:i])
            sections.append(lines[i+1:])
    sections = (parse_first(sections[0]), parse_second(sections[1]))

    print(part1(*sections))
    print(part2(*sections))

    # for i, part in enumerate([part1, part2]):
    #     print(f"Part {i+1}: {part(parse_first(sections[0]), parse_second(sections[1]))}")

    # for i in range(len(sections[1][3])):
    #     print(len(dfs(sections[0], sections[1][3][i], sections[1][3])))

if __name__ == "__main__":
    main()
