from enum import Enum
from sys import setrecursionlimit
from typing import TypeAlias
from time import sleep

Coordinate: TypeAlias = tuple[int, int]

class Direction(Enum):
    NORTH = 0    
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn(self, dir: int) -> 'Direction':
        return Direction((self.value + dir) % 4)

    def turn_counter_clockwise(self) -> 'Direction':
        return self.turn(-1)
    
    def turn_clockwise(self) -> 'Direction':
        return self.turn(1)
    
    def to_coord(self) -> Coordinate:
        return {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }[self]

def move_print_cursor_up(n: int):
    print(f"{"\033[F"}{"\033[A" * (n-1)}", end='')

class Maze:
    def __init__(self, tiles: list[list[str]]):
        self.tiles = tiles
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == 'S': self.start = x, y
                elif tile == 'E': self.end = x, y
        self._score = None


    def get_at(self, coord: Coordinate, error_value = '#') -> int:
        if 0 > coord[0] or 0 > coord[1]: return error_value
        try: return self.tiles[coord[1]][coord[0]]
        except IndexError: return error_value

    def score(self):
        def score_inner(pos: Coordinate, direction: Direction, visited: dict[Coordinate, int], score: int) -> int:
            if (key := pos) in visited and visited[key] <= score: return None
            if self.get_at(pos) == '#': return None
            visited[key] = score
            if pos == self.end: return score
            path_scores: list[int] = []
            for dir in [0, -1, 1]:
                new_dir = direction.turn(dir)
                dir_coord = new_dir.to_coord()
                next_pos = pos[0] + dir_coord[0], pos[1] + dir_coord[1]
                result = score_inner(next_pos, new_dir, visited, score + 1 + 1000 * abs(dir))
                if result: path_scores.append(result)
            try: return min(path_scores)
            except ValueError: return None
        if self._score is None:
            self._score = score_inner(self.start, Direction.EAST, {}, 0)
        return self._score
    
    def best_seats(self):
        CacheDict: TypeAlias = dict[Coordinate, tuple[int, set[Coordinate]]]
        def best_seats_inner(pos: Coordinate, direction: Direction, visited: CacheDict, score: int, seats: set[Coordinate]):
            seats = seats.union({pos})
            if pos == (15,6):
                pass
            if (key := (*pos, direction)) in visited:
                if visited[key][0] < score: return None
                if visited[key][0] == score: 
                    seats = seats.union(visited[key][1])
                    visited[key] = score, seats
                    return None
            if self.get_at(pos) == '#': return None
            self.print(pos, ['^', '>', 'v', '<'][direction.value])
            print(score)
            move_print_cursor_up(len(self.tiles)+1)
            # sleep(0.2)
            visited[key] = score, seats
            if pos == self.end: return score
            path_scores: list[int] = []
            for dir in [0, 1, -1]:
                new_dir = direction.turn(dir)
                dir_coord = new_dir.to_coord()
                next_pos = pos[0] + dir_coord[0], pos[1] + dir_coord[1]
                result = best_seats_inner(next_pos, new_dir, visited, score + 1 + 1000 * abs(dir), seats)
                if result: path_scores.append(result)
            try: return min(path_scores)
            except ValueError: return None
        path_dict: CacheDict = {}
        smallest = best_seats_inner(self.start, Direction.EAST, path_dict, 0, set())
        seats = set()
        for i in range(4):
            direction = Direction(i)
            if (key := (*self.end, direction)) in path_dict and path_dict[key][0] == smallest:
                seats = seats.union(path_dict[key][1])
        return seats

    
    
    def print(self, pos: Coordinate, char: str = 'O') -> str:
        for y, row in enumerate(self.tiles):
            for x, cell in enumerate(row):
                if (x, y) == pos: print(char, end='')
                else: print(cell, end='')
            print()



def parse_maze(lines: list[str]) -> Maze:
    return Maze([list(line.strip()) for line in lines])


def part1(maze: Maze) -> int:
    return maze.score()

def part2(maze: Maze) -> int:
    seats = maze.best_seats()
    for y, row in enumerate(maze.tiles):
        for x, tile in enumerate(row):
            if (x, y) in seats: print('O', end='')
            else: print(tile, end='')
        print()
    return len(seats)

def main():
    setrecursionlimit(50000)
    with open("16. Reindeer Maze/test2.txt", 'r') as f:
        lines = f.readlines()
    maze = parse_maze(lines)
    print(part2(maze))


if __name__ == "__main__":
    main()