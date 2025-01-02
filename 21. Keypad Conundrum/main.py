class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> 'Coord':
        if type(other) is Coord:
            return Coord(self.x * other.x, self.y * other.y)
        if type(other) is int:
            return Coord(self.x * other, self.y * other)
        raise ValueError(f'Cannot multiply a Coord with a {type(other)}')
    
    def __tuple__(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, value: 'Coord') -> bool:
        if type(value) is not Coord: return False
        return self.x == value.x and self.y == value.y

    def __str__(self) -> str:
        return str((self.x, self.y))

    def __repr__(self) -> str:
        return str(self)


class Keypad:
    def __init__(self, robot: 'Robot', empty_coord: Coord, keymap: dict[str, Coord]):
        self.robot = robot
        self.empty_coord = empty_coord
        self.keymap = keymap

    def click_key(self, key: str) -> int:
        if self.robot is None: return 1
        return self.robot.clicks_required(self.keymap[key], self.empty_coord)


class Robot:
    def __init__(self, keypad: Keypad, arm: Coord):
        self.keypad = keypad
        self.arm = arm

    def clicks_required(self, coord: Coord, empty_coord: Coord) -> int:
        delta = coord - self.arm
        vertical_button, horizontal_button = ['^','v'][delta.y >= 0], ['<','>'][delta.x >= 0]
        clicks = ([vertical_button for _ in range(abs(delta.y))] +
                  [horizontal_button for _ in range(abs(delta.x))])
        for x in range(1, abs(delta.x)+1):
            if delta.x < 0: x *= -1
            if self.arm + Coord(x, 0) == empty_coord: break
        else:
            for y in range(1, abs(delta.y)+1):
                if delta.y < 0: y *= -1
                if self.arm + Coord(y, 0) == empty_coord:
                    clicks.reverse()
                    break
            else:
                distances = [self.distance_to_button(button)
                             for button in [horizontal_button, vertical_button]]
                if distances[0] <= distances[1]: clicks.reverse()
        self.arm = coord
        return sum(self.keypad.click_key(button) for button in clicks + ['A'])

    def distance_to_button(self, button: str) -> int:
        if button not in self.keypad.keymap: return None
        delta = self.arm - self.keypad.keymap[button]
        return abs(delta.x) + abs(delta.y)


class NumericKeypad(Keypad):
    def __init__(self, robot: Robot):
        super().__init__(
            robot,
            Coord(0, 3),
            {'7': Coord(0, 0),
             '8': Coord(1, 0),
             '9': Coord(2, 0),
             '4': Coord(0, 1),
             '5': Coord(1, 1),
             '6': Coord(2, 1),
             '1': Coord(0, 2),
             '2': Coord(1, 2),
             '3': Coord(2, 2),
             '0': Coord(1, 3),
             'A': Coord(2, 3)}
        )


class DirectionalKeypad(Keypad):
    def __init__(self, robot: Robot):
        super().__init__(
            robot,
            Coord(0, 0),
            {'^': Coord(1, 0),
             'A': Coord(2, 0),
             '<': Coord(0, 1),
             'v': Coord(1, 1),
             '>': Coord(2, 1)}
        )


def part1(keypad: DirectionalKeypad, lines: list[str]) -> int:
    total = 0
    for line in lines:
        line = line.strip()
        s = sum(map(keypad.click_key, line))
        total += s * int(line[:-1])
    return total


def part2(keypad: NumericKeypad, lines: list[str]) -> int:
    ...


def main():
    with open('21. Keypad Conundrum/test.txt', 'r') as f:
        lines = f.readlines()
    keypad = NumericKeypad(
        robot=Robot(
        keypad=DirectionalKeypad(
        robot=Robot(
        keypad=DirectionalKeypad(
        robot=Robot(
        keypad=DirectionalKeypad(None),
        arm=Coord(2, 0))
        ), arm=Coord(2, 0))
        ), arm=Coord(2, 3))
    )
    for i, part in enumerate([part1, part2]):
        print(f'Part {i+1}: {part(keypad, lines)}')


if __name__ == '__main__':
    main()