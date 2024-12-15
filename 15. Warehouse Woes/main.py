from enum import Enum
import time

class Tile(Enum):
    EMPTY = '.'
    PLAYER = '@'
    WALL = '#'
    BOX = 'O'

class Direction(Enum):
    UP = '^'    
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'


class Warehouse:
    def __init__(self, tiles: list[list[Tile]]):
        self.tiles = tiles
        for y, row in enumerate(self.tiles):
            if (player := Tile('@')) in row: 
                self.cur_pos = (row.index(player), y)
                return
        raise ValueError('There is no player tile in input')


    def move(self, direction: Direction):
        dir_coord = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0)
        }[direction]
        end_tile, depth = self.depth_search(self.cur_pos, dir_coord)
        if end_tile == Tile.WALL: return   
        first_coord = self.cur_pos[0] + dir_coord[0] * depth, self.cur_pos[1] + dir_coord[1] * depth
        for i in range(depth-1, -1, -1):
            second_coord = self.cur_pos[0] + dir_coord[0] * i, self.cur_pos[1] + dir_coord[1] * i
            (
                self.tiles[second_coord[1]][second_coord[0]], 
                self.tiles[first_coord[1]][first_coord[0]]) = (
                self.tiles[first_coord[1]][first_coord[0]],
                self.tiles[second_coord[1]][second_coord[0]]
            )
            first_coord = second_coord
        self.cur_pos = self.cur_pos[0] + dir_coord[0], self.cur_pos[1] + dir_coord[1]

    def sum_box_gps_coordinates(self) -> int:
        total = 0
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile != Tile.BOX: continue
                total += x + 100 * y
        return total


    def depth_search(self, cur_coord: tuple[int, int], dir_coord: tuple[int, int], depth: int = 0) -> tuple[Tile.WALL or Tile.EMPTY, int]:
        tile = self.tiles[cur_coord[1]][cur_coord[0]]
        if tile in (Tile.WALL, Tile.EMPTY):
            return tile, depth
        next_coord = cur_coord[0] + dir_coord[0], cur_coord[1] + dir_coord[1]
        return self.depth_search(next_coord, dir_coord, depth + 1)


    def __str__(self) -> str:
        return '\n'.join(''.join(tile.value for tile in row) for row in self.tiles)
    
    def __repr__(self) -> str:
        return str(self)
    

def parse_input(input: str):
    warehouse_str, dir_str = input.split('\n\n')
    return (
        Warehouse([[Tile(char) for char in line.strip()] for line in warehouse_str.split('\n')]),
        [Direction(char) for char in dir_str if char != '\n']
    )
    

def main():
    with open("15. Warehouse Woes/input.txt", 'r') as f:
        data = f.read()
    warehouse, directions = parse_input(data)

    print(warehouse)
    for direction in directions:
        warehouse.move(direction)
        print(f"{"\033[F"}{"\033[A" * (len(warehouse.tiles)-1)}", end='')
        print(warehouse)
        # time.sleep(0.3)

    print(warehouse.sum_box_gps_coordinates())


if __name__ == "__main__":
    main()