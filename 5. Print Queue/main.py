
class OrderingMap:

    def __init__(self, d: dict[int, set[int]]):
        self.vals = d

    def allowed_before(self, key_val: int, val) -> bool:
        return val not in self.vals[key_val]
    
    def get_all_not_allowed_before(self, key_val: int) -> set[int]:
        return self.vals[key_val]
    
    def __contains__(self, num: int) -> bool:
        return num in self.vals
    
    def get(self, key_val: int) -> set[int]:
        return self.vals[key_val] if key_val in self.vals else set()

    def __getitem__(self, key: int) -> set[int]:
        return self.vals[key] if key in self.vals else set()


class NumSequence:
    def __init__(self, vals: list[int]):
        self.vals = vals
        self.dfs_cache = {}

    def __hash__(self) -> int:
        return tuple(self.vals).__hash__()
    
    def __contains__(self, val: int) -> bool:
        return val in self.vals
    
    def __getitem__(self, index: int) -> int:
        return self.vals[index]
    
    def __len__(self) -> int:
        return len(self.vals)
    
    def is_ordered(self, ordering: OrderingMap) -> bool:
        occured: set[int] = set()
        for num in self.vals:
            if (not occured or
                num not in ordering or
                not occured.intersection(ordering.get(num))
                ): occured.add(num)
            else: return False
        return True

    def get_all_required_after(self, ordering: OrderingMap, key) -> set[int]:
        if key in self.dfs_cache:
            return self.dfs_cache[key]
        if key not in ordering:
            return set()
        afters: set[int] = ordering[key]
        for new_key in afters:
            if new_key not in self: continue
            afters = afters.union(self.get_all_required_after(ordering, new_key))
        self.dfs_cache[key] = afters
        return afters
    

    def correct_order(self, ordering: OrderingMap) -> None:
        self.dfs_cache = {}
        lengths = {k: len(self.get_all_required_after(ordering, k)) for k in self.vals}
        self.vals = list(reversed(sorted(self.vals, key=lambda x: lengths[x])))


def parse_map(lines: list[str]) -> OrderingMap:
    ordering = {}
    for line in lines:
        pair = line.strip().split('|')
        num1, num2 = int(pair[0]), int(pair[1])
        if num1 in ordering:
            ordering[num1].add(num2)
        else:
            ordering[num1] = {num2}
    return OrderingMap(ordering)

def parse_sequences(lines: list[str]) -> list[NumSequence]:
    return [NumSequence([int(num) for num in line.strip().split(",")] )
            for line in lines]


def part1(ordering: OrderingMap, sequences: list[NumSequence]) -> int:
    total = 0
    for sequence in sequences:
        if sequence.is_ordered(ordering):
            total += sequence[len(sequence) // 2]
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

def part2(ordering: OrderingMap, sequences: list[NumSequence]) -> int:
    total = 0
    for sequence in sequences:
        if sequence.is_ordered(ordering): continue
        sequence.correct_order(ordering)
        total += sequence[len(sequence) // 2]
    return total



def main():
    with open("5. Print Queue/input.txt", 'r') as f:
        lines = f.readlines()
    
    sections = []
    for i, line in enumerate(lines):
        if line == '\n':
            sections.append(lines[:i])
            sections.append(lines[i+1:])
    sections = (parse_map(sections[0]), parse_sequences(sections[1]))
    ordering = OrderingMap(sections[0])
    sequences = [NumSequence(sequence) for sequence in sections[1]]

    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(ordering, sequences)}")


if __name__ == "__main__":
    main()