from copy import deepcopy
from collections.abc import Callable

class FieldPattern:
    
    def __init__(self, coords: list[tuple[int, int]]):
        self.coords = coords.copy()


class LetterSequence:
    
    def __init__(self, letter: list[str]):
        self.letters = letter.copy()
    
    def match(self, sequence: 'LetterSequence') -> bool:
        return self.letters == sequence.letters


class LetterField:
    
    def __init__(self, letters: list[list[str]]):
        self.letters = deepcopy(letters)
    
    def get_at(self, coord: tuple[int, int]) -> str:
        if not (0 <= coord[0] and 0 <= coord[1]): return '.' 
        try:
            return self.letters[coord[1]][coord[0]]
        except IndexError:
            return '.' 

    def get_sequence(self, offset_coord: tuple[int, int], pattern: FieldPattern):
        return LetterSequence([
            self.get_at((coord[0] + offset_coord[0], coord[1] + offset_coord[1])) 
            for coord in pattern.coords
        ])
    
    def scan(self, finder_function: Callable[['LetterField', tuple[int, int]], int]) -> int:
        occurenses = 0
        for y, line in enumerate(self.letters):
            if y >= 6:
                pass
            for x in range(len(line)):
                occurenses += finder_function(self, (x, y))
        return occurenses


def part1(field: LetterField, origin: tuple[int, int]) -> int:
    letter = field.get_at(origin)
    try:
        correct_sequence = {
            'X': LetterSequence(['M', 'A', 'S']),
            'S': LetterSequence(['A', 'M', 'X'])
        }[letter]
    except KeyError:
        return 0
    patterns = [
        FieldPattern([( 1, 0), ( 2, 0), ( 3, 0)]),
        FieldPattern([( 0, 1), ( 0, 2), ( 0, 3)]),
        FieldPattern([( 1, 1), ( 2, 2), ( 3, 3)]),
        FieldPattern([(-1, 1), (-2, 2), (-3, 3)])
    ]
    return sum(
        field.get_sequence(origin, pattern).match(correct_sequence)
        for pattern in patterns
    )


def part2(field: LetterField, origin: tuple[int, int]) -> int:
    letters = [field.get_at(origin),
               field.get_at((origin[0] + 2, origin[1]))]
    correct_sequences = {
        'M': LetterSequence(['A', 'S']),
        'S': LetterSequence(['A', 'M'])
    }
    patterns = [
        FieldPattern([(1, 1), (2, 2)]),
        FieldPattern([(1, 1), (0, 2)])
    ]
    try:
        sequences = [correct_sequences[letter] for letter in letters]
    except KeyError:
        return 0

    return 1 if sum(
        field.get_sequence(origin, patterns[i]).match(sequences[i])
        for i in range(2)
    ) == 2 else 0


def main():
    with open("4. Ceres Search/input.txt", 'r') as f:
        lines = f.readlines()
    input = [list(line.strip()) for line in lines]
    field = LetterField(input)
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {field.scan(part)}")


if __name__ == "__main__":
    main()
