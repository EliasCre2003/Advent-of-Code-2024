class StripeSequence:
    def __init__(self, sequence: list[str]):
        self.sequence = sequence

    def match(self, sequence: 'StripeSequence') -> bool:
        if len(sequence) > len(self): return False
        return self[:len(sequence)] == sequence
    
    def __len__(self) -> int:
        return len(self.sequence)

    def __eq__(self, other: 'StripeSequence') -> bool:
        return self.sequence == other.sequence
    
    def __getitem__(self, val):
        return StripeSequence(self.sequence[val])
    
    def __hash__(self) -> int:
        return hash(tuple(self.sequence))


def to_stripe_sequence(string: str) -> StripeSequence:
    return StripeSequence([char for char in string])


def parse_input(data: str) -> tuple[list[StripeSequence], list[StripeSequence]]:
    towel_str, pattern_str = data.split('\n\n')
    towels = [to_stripe_sequence(string) for string in towel_str.split(', ')]
    designs = [to_stripe_sequence(line.strip()) for line in pattern_str.split('\n')]
    return towels, designs


def possible_combinations(design: StripeSequence, towels: list[StripeSequence], cache: dict[StripeSequence, int] = {}) -> int:
    if len(design) == 0: return 1
    if design in cache: return cache[design]
    total = 0
    for towel in towels:
        if not design.match(towel): continue
        total += possible_combinations(design[len(towel):], towels)
    cache[design] = total
    return total


def main():
    with open('19. Linen Layout/input.txt', 'r') as f:
        data = f.read()
    towels, designs = parse_input(data)
    combination_map = {design: possible_combinations(design, towels) for design in designs}
    print(f'Part 1: {sum(n > 0 for n in combination_map.values())}\n'
          f'Part 2: {sum(n for n in combination_map.values())}')


if __name__ == '__main__':
    main()