from enum import Enum
from sortedcontainers import SortedSet

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Step:
    def __init__(self, coord: tuple[int, int], direction: Direction):
        self.coord = coord
        self.direction = direction

    def __hash__(self) -> int:
        return hash((self.coord, self.direction))
    
    def __eq__(self, other) -> bool:
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1] and self.direction.value == other.direction.value


class GameMap:
    def __init__(self, cells: list[list[str]], start_pos: tuple[int, int]) -> None:
        self.cells = cells
        self.start_pos = start_pos

    def get_at(self, coord: tuple[int, int], outside_char: str = '*'):
        if not (0 <= coord[0] and 0 <= coord[1]): return outside_char
        try: return self.cells[coord[1]][coord[0]]
        except IndexError: return outside_char

    def set_at(self, coord: tuple[int, int], val: str) -> bool:
        if not (0 <= coord[0] and 0 <= coord[1]): return False
        try: 
            self.cells[coord[1]][coord[0]] = val
            return True
        except IndexError: return False

    def travel(self, progress: list[Step] = None) -> tuple[bool, list[Step]]:
        """Returns true if the guard has left the area, 
        returns false if the guard gets stuck in a loop"""

        dir_index = 0
        if not progress:
            position = self.start_pos
            steps = [Step(position, Direction.UP)]
        else:
            steps = progress.copy()
            position = steps[-1].coord
        prev_step = step

        while True:
            direction = [(0, -1), (1, 0), (0, 1), (-1, 0)][dir_index]
            next_pos = position[0] + direction[0], position[1] + direction[1]
            if next_pos == (7, 9):
                pass
            done = False
            loop = False
            next_direction = Direction(dir_index)

            match self.get_at(next_pos):
                case '#':
                    dir_index = (dir_index + 1) % 4
                    steps[-1].direction = Direction(dir_index)
                case '*':
                    done = True
                case _:
                    step = Step(next_pos, next_direction)
                    if step in steps: loop = True
                    else: steps.append(step)
                    position = next_pos
            if loop:
                return False, None
            elif done:
                return True, steps


def parse_map(lines: list[str]) -> GameMap:
    cells = [None] * len(lines)
    for i, line in enumerate(lines):
        cells[i] = list(line)
        if '^' in line: 
            start_pos = (si := line.index('^')), i
            cells[i][si] = '.'
    return GameMap(cells, start_pos)

def part1(game_map: GameMap) -> int:
    return len(set(step.coord for step in game_map.travel()[1]))

def part2(game_map: GameMap) -> int:
    steps = game_map.travel()[1]
    obstacles = set()
    for a, step in enumerate(steps):
        i = a-1 if a > 0 else 0
        look_dir = [(0, -1), (1, 0), (0, 1), (-1, 0)][step.direction.value]
        obstacle_coord = step.coord[0] + look_dir[0], step.coord[1] + look_dir[1]
        if not game_map.set_at(obstacle_coord, '#'):
            continue
        if not game_map.travel()[0]:
            obstacles.add(obstacle_coord)
        game_map.set_at(obstacle_coord, '.')
        print(f"Progress: {a+1} / {len(steps)}")
    return len(obstacles)



def main():
    with open("6. Guard Gallivant/input.txt", 'r') as f:
        lines = f.readlines()

    print(part2(parse_map(lines)))


if __name__ == "__main__":
    main()
    # print([5, 4, 6][:1])
