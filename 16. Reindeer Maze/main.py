from enum import Enum
from sys import setrecursionlimit

class Direction(Enum):
    UP = 0    
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn(self, dir: int) -> 'Direction':
        return Direction((self.value + dir) % 4)

    def turn_counter_clockwise(self) -> 'Direction':
        return self.turn(-1)
    
    def turn_clockwise(self) -> 'Direction':
        return self.turn(1)
    
    def to_coord(self) -> tuple[int, int]:
        return {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0)
        }[self]


class Maze:
    def __init__(self, tiles: list[list[str]]):
        self.tiles = tiles
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == 'S': self.start = x, y
                elif tile == 'E': self.end = x, y


    def get_at(self, coord: tuple[int, int], error_value = '#') -> int:
        if 0 > coord[0] or 0 > coord[1]: return error_value
        try: return self.tiles[coord[1]][coord[0]]
        except IndexError: return error_value

    def score(self, pos: tuple[int, int] = None, direction: Direction = Direction.LEFT, visited: dict[tuple[int, int, Direction], int] = None, score = 0) -> int:
        if pos is None: pos = self.start
        if visited is None: visited = {}
        elif (key := (*pos, direction)) in visited and visited[key] <= score: return None
        else: visited[key] = score
        # self.print(pos, ['^', '>', 'v', '<'][direction.value])
        # print(score)
        if pos == self.end: return score
        if self.get_at(pos) == '#': return None
        smallest = 99999999999999999999999999999999999999999999999999
        for dir in [0, -1, 1, 2]:
            new_dir = direction.turn(dir)
            dir_coord = new_dir.to_coord()
            next_pos = pos[0] + dir_coord[0], pos[1] + dir_coord[1]
            result = self.score(next_pos, new_dir, visited, score + 1 + 1000 * abs(dir))
            if result: smallest = min(smallest, result)
        return smallest
    
    def print(self, pos: tuple[int, int], char: str = 'O') -> str:
        for y, row in enumerate(self.tiles):
            for x, cell in enumerate(row):
                if (x, y) == pos: print(char, end='')
                else: print(cell, end='')
            print()


def parse_maze(lines: list[str]) -> Maze:
    return Maze([list(line.strip()) for line in lines])


def part1(maze: Maze) -> Maze:
    return maze.score()


def main():
    setrecursionlimit(50000)
    with open("16. Reindeer Maze/input.txt", 'r') as f:
        lines = f.readlines()
    maze = parse_maze(lines)
    print(part1(maze))


if __name__ == "__main__":
    main()