from enum import Enum


class Stripe(Enum):
    WHITE = 'w'
    BLUE = 'u'
    BLACK = 'b'
    RED = 'r'
    GREEN = 'g'

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class StripeSequence:
    def __init__(self, sequence: list[Stripe]):
        self.sequence = sequence

    def match(self, sequence: 'StripeSequence') -> bool:
        if len(sequence) > len(self): return False
        return self[:len(sequence)] == sequence
    
    def __len__(self) -> int:
        return len(self.sequence)

    def __str__(self):
        return ''.join(map(str, self.sequence))
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other: 'StripeSequence') -> bool:
        return self.sequence == other.sequence
    
    def __getitem__(self, val):
        return StripeSequence(self.sequence[val])
    
    def __hash__(self) -> int:
        return hash(tuple(self.sequence))


def to_stripe_sequence(string: str) -> StripeSequence:
    return StripeSequence([Stripe(char) for char in string])


def parse_input(data: str) -> tuple[list[StripeSequence], list[StripeSequence]]:
    towel_str, pattern_str = data.split('\n\n')
    towels = [to_stripe_sequence(string) for string in towel_str.split(', ')]
    designs = [to_stripe_sequence(line.strip()) for line in pattern_str.split('\n')]
    return towels, designs


def is_possible(design: StripeSequence, towels: list[StripeSequence], cache: dict[StripeSequence, bool] = {}) -> bool:
    if len(design) == 0: return True
    if design in cache: return cache[design]
    for towel in towels:
        if not design.match(towel): continue
        if is_possible(design[len(towel):], towels):
            return True
    cache[design] = False
    return False


def possible_combinations(design: StripeSequence, towels: list[StripeSequence], cache: dict[StripeSequence, int] = {}) -> int:
    if len(design) == 0: return 1
    if design in cache: return cache[design]
    total = 0
    for towel in towels:
        if not design.match(towel): continue
        total += possible_combinations(design[len(towel):], towels)
    cache[design] = total
    return total


def part1(towels: list[StripeSequence], desings: list[StripeSequence]) -> int:
    return sum(is_possible(design, towels) for design in desings)


def part2(towels: list[StripeSequence], desings: list[StripeSequence]) -> int:
    return sum(possible_combinations(design, towels) for design in desings)


def main():
    with open('19. Linen Layout/input.txt', 'r') as f:
        data = f.read()
    towels, designs = parse_input(data)
    for i, part in enumerate([part1, part2]):
        print(f'Part {i+1}: {part(towels, designs)}')


if __name__ == '__main__':
    main()