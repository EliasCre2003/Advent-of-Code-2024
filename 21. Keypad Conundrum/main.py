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
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, value: 'Coord') -> bool:
        if type(value) is not Coord: return False
        return self.x == value.x and self.y == value.y
    
    def __str__(self) -> str:
        return str((self.x, self.y))

    def __repr__(self) -> str:
        return str(self)


class Keypad:
    def __init__(self, robot: 'Robot', empty_coord: Coord):
        self.robot = robot
        self.empty_coord = empty_coord

    def click_key(self, key: str) -> int: ...


class Robot:
    def __init__(self, keypad: Keypad, arm: Coord):
        self.keypad = keypad
        self.arm = arm

    def clicks_required(self, coord: Coord, empty_coord: Coord) -> int:
        clicks: list[str] = []
        delta = coord - self.arm
        for x in range(1, abs(delta.x)+1):
            if delta.x < 0: x *= -1
            if self.arm + Coord(x, 0) == empty_coord:
                for _ in range(abs(delta.y)): clicks.append(['^','v'][delta.y >= 0])
                for _ in range(abs(delta.x)): clicks.append(['<','>'][delta.x >= 0])
                break
        else:
            for _ in range(abs(delta.x)): clicks.append(['<','>'][delta.x >= 0])
            for _ in range(abs(delta.y)): clicks.append(['^','v'][delta.y >= 0])
        self.arm = coord
        return sum(self.keypad.click_key(button) for button in clicks + ['A'])


class NumericKeypad(Keypad):
    def __init__(self, robot: Robot):
        super().__init__(robot, Coord(0, 3))

    def click_key(self, key: str) -> int:
        return self.robot.clicks_required({
            '7': Coord(0, 0),
            '8': Coord(1, 0),
            '9': Coord(2, 0),
            '4': Coord(0, 1),
            '5': Coord(1, 1),
            '6': Coord(2, 1),
            '1': Coord(0, 2),
            '2': Coord(1, 2),
            '3': Coord(2, 2),
            '0': Coord(1, 3),
            'A': Coord(2, 3)
        }[key], self.empty_coord)


class DirectionalKeypad(Keypad):
    def __init__(self, robot: Robot):
        super().__init__(robot, Coord(0, 0))

    def click_key(self, key: str) -> int:
        if self.robot is None: return 1
        return self.robot.clicks_required({
            '^': Coord(1, 0),
            'A': Coord(2, 0),
            '<': Coord(0, 1),
            'v': Coord(1, 1),
            '>': Coord(2, 1)
        }[key], self.empty_coord)


def part1(keypad: DirectionalKeypad, lines: list[str]) -> int:
    return sum(
        sum(
            map(keypad.click_key, (stripped := line.strip()))) * 
            int(stripped[:-1]
        ) for line in lines
    )


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
        ), arm=Coord(2, 3)
    ))
    for i, part in enumerate([part1, part2]):
        print(f'Part {i+1}: {part(keypad, lines)}')


if __name__ == '__main__':
    main()