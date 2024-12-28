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


class Robot:
    def __init__(self, arm: Coord, keypad: 'Keypad'):
        self.arm = arm # the current position of the robot's arm
        self.keypad = keypad # the keypad that the robot is interacting with

    def exec_click(self, button: str):
        match button:
            case '^': self.arm.y -= 1
            case '<': self.arm.x -= 1
            case 'v': self.arm.y += 1
            case '>': self.arm.x += 1
            case 'A': self.keypad.click(self.arm)
        # print(self.arm, self.keypad.empty_coord)
        # print(self.arm, end=' ')
        if self.arm == self.keypad.empty_coord:
            print('Fucked up')


class Keypad:
    def __init__(self, keymap: dict[Coord, str], robot: Robot, empty_coord: Coord):
        self.robot = robot  # the robot that the keypad is attached to
        self.keymap = keymap # the mapping of coordinates to keys
        self.empty_coord = empty_coord # the coordinate of the empty space

    def click(self, coord: Coord):
        if self.robot is None: print(self.keymap[coord], end='')
        else: self.robot.exec_click(self.keymap[coord])


numpad = {
    Coord(0, 0): '7',
    Coord(1, 0): '8',
    Coord(2, 0): '9',
    Coord(0, 1): '4',
    Coord(1, 1): '5',
    Coord(2, 1): '6',
    Coord(0, 2): '1',
    Coord(1, 2): '2',
    Coord(2, 2): '3',
    Coord(1, 3): '0',
    Coord(2, 3): 'A'
}

dirpad = {
    Coord(1, 0): '^',
    Coord(2, 0): 'A',
    Coord(0, 1): '<',
    Coord(1, 1): 'v',
    Coord(2, 1): '>',
}

lock_pad = Keypad(numpad, None, Coord(0, 3))
first_robot = Robot(Coord(2, 3), lock_pad)
first_robot_keypad = Keypad(dirpad, first_robot, Coord(0, 0))
second_robot = Robot(Coord(2, 0), first_robot_keypad)
second_robot_keypad = Keypad(dirpad, second_robot, Coord(0, 0))
third_robot = Robot(Coord(2, 0), second_robot_keypad)
third_robot_keypad = Keypad(dirpad, third_robot, Coord(0, 0))

# robot = Robot(Coord(2, 0), Keypad(dirpad, Robot(Coord(2, 0), Keypad(dirpad, Robot(Coord(2, 3), Keypad(numpad, None, Coord(0, 3))), Coord(0, 0))), Coord(0, 0)))

# sequences = ['<<vAA>A>^AvAA<^A>A<<vA>>^AvA^A<vA>^A<<vA>^A>AAvA^A<<vA>A>^AAAvA<^A>A',
#                  '<<vA>>^AAAvA^A<<vAA>A>^AvAA<^A>A<<vA>A>^AAAvA<^A>A<vA>^A<A>A',
#                  '<<vAA>A>^AAvA<^A>AvA^A<<vA>>^AAvA^A<vA>^AA<A>A<<vA>A>^AAAvA<^A>A',
#                  '<<vAA>A>^AAvA<^A>AAvA^A<vA>^A<A>A<vA>^A<A>A<<vA>A>^AAvA<^A>A',
#                  '<<vA>>^AvA^A<<vAA>A>^AAvA<^A>AAvA^A<vA>^AA<A>A<<vA>A>^AAAvA<^A>A']

# sequences = ['<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
#              '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
#              '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
#              '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
#              '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A']

# for sequence in sequences: 
#     for char in sequence:
#         robot.exec_click(char)

for char in '<vA<AA>>^AAvA<^A>AvA^Av<<A>>^AAvA^A<vA>^AA<A>Av<<A>A>^AAAvA<^A>A':
    print(char, end='')
    third_robot.exec_click(char)
    if char == 'A': print('|', end='')
print()
    