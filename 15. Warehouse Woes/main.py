from enum import Enum
import time

class Tile(Enum):
    EMPTY = '.'
    PLAYER = '@'
    WALL = '#'
    BOX = 'O'
    LEFT_BOX = '['
    RIGHT_BOX = ']'

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
    
    def get_at(self, coord: tuple[int, int], error_value = '#') -> int:
        if 0 > coord[0] or 0 > coord[1]: return error_value
        try: return self.tiles[coord[1]][coord[0]]
        except IndexError: return error_value

    def move_part1(self, direction: Direction):

        def depth_search(cur_coord: tuple[int, int], dir_coord: tuple[int, int], depth: int = 0) -> tuple[Tile, int]:
            tile = self.get_at(cur_coord)
            if tile in (Tile.WALL, Tile.EMPTY):
                return tile, depth
            next_coord = cur_coord[0] + dir_coord[0], cur_coord[1] + dir_coord[1]
            return depth_search(next_coord, dir_coord, depth + 1)

        dir_coord = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0)
        }[direction]
        end_tile, depth = depth_search(self.cur_pos, dir_coord)
        if end_tile == Tile.WALL: return   
        first_coord = self.cur_pos[0] + dir_coord[0] * depth, self.cur_pos[1] + dir_coord[1] * depth
        for i in range(depth-1, -1, -1):
            second_coord = self.cur_pos[0] + dir_coord[0] * i, self.cur_pos[1] + dir_coord[1] * i
            (
                self.tiles[second_coord[1]][second_coord[0]], 
                self.tiles[first_coord[1]][first_coord[0]]
            ) = (
                self.tiles[first_coord[1]][first_coord[0]],
                self.tiles[second_coord[1]][second_coord[0]]
            )
            first_coord = second_coord
        self.cur_pos = self.cur_pos[0] + dir_coord[0], self.cur_pos[1] + dir_coord[1]

    def move_part2(self, direction: Direction):
        def vertical_search(cur_coord: tuple[int, int], dir: int, visited: set = None, to_move: set = None) -> tuple[set[tuple[int, int]], int]:
            if to_move is None: to_move = set()
            if visited is None: visited = set()
            elif cur_coord in visited: return 0, to_move
            visited.add(cur_coord)
            tile = self.get_at(cur_coord)
            total = 0
            match tile:
                case Tile.WALL:
                    to_move.add(cur_coord)
                    return 1, to_move, visited
                case Tile.EMPTY:
                    to_move.add(cur_coord)
                    return 0, to_move, visited
                case Tile.LEFT_BOX:
                    total += vertical_search((cur_coord[0]+1, cur_coord[1]), dir, visited, to_move)[0]
                case Tile.RIGHT_BOX:
                    total += vertical_search((cur_coord[0]-1, cur_coord[1]), dir, visited, to_move)[0]
            result = vertical_search((cur_coord[0], cur_coord[1] + dir), dir, visited, to_move)
            return total + result[0], to_move, visited
        
        def horizontal_search(cur_coord: tuple[int, int], dir: int, depth: int = 0, visited = None):
            if visited is None: visited = set()
            visited.add(cur_coord)
            tile = self.get_at(cur_coord)
            if tile == Tile.WALL:
                return None, visited
            elif tile == Tile.EMPTY:
                return cur_coord, visited
            next_coord = cur_coord[0] + dir, cur_coord[1]
            return horizontal_search(next_coord, dir, depth + 1, visited)

        dir_coord = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0)
        }[direction]
        
        if direction in (Direction.UP, Direction.DOWN):
            walls, to_change, visited = vertical_search(self.cur_pos, dir_coord[1])
            if walls > 0: return
        else:
            to_change, visited = horizontal_search(self.cur_pos, dir_coord[0])
            if to_change is None: return
            to_change = {to_change}
        
        for first_coord in to_change:
            while True:
                second_coord = first_coord[0] - dir_coord[0], first_coord[1] - dir_coord[1]
                if second_coord not in visited:
                    break
                if self.get_at(second_coord) in (Tile.EMPTY, Tile.WALL):
                    break
                if second_coord[1] == self.cur_pos[1] and direction in (Direction.UP, Direction.DOWN) and self.get_at(second_coord) != Tile.PLAYER:
                    break
                (
                    self.tiles[second_coord[1]][second_coord[0]], 
                    self.tiles[first_coord[1]][first_coord[0]]
                ) = (
                    self.tiles[first_coord[1]][first_coord[0]],
                    self.tiles[second_coord[1]][second_coord[0]]
                )
                if self.get_at(first_coord) == Tile.PLAYER:
                    break
                first_coord = second_coord
                
        self.cur_pos = self.cur_pos[0] + dir_coord[0], self.cur_pos[1] + dir_coord[1]
    
    
    def sum_gps_coordinates(self, tile_type: Tile) -> int:
        total = 0
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile != tile_type: continue
                total += x + 100 * y
        return total

    def __str__(self) -> str:
        return '\n'.join(' '.join(tile.value for tile in row) for row in self.tiles)
    
    def __repr__(self) -> str:
        return str(self)
    
    
def part1(data: str):
    warehouse_str, dir_str = data.split('\n\n')
    warehouse, directions = (
        Warehouse([[Tile(char) for char in line.strip()] for line in warehouse_str.split('\n')]),
        [Direction(char) for char in dir_str if char != '\n']
    )
    print(warehouse)
    for direction in directions:
        warehouse.move_part1(direction)
        print(f"{"\033[F"}{"\033[A" * (len(warehouse.tiles)-1)}", end='')
        print(warehouse)
        # time.sleep(0.1)
    return warehouse.sum_gps_coordinates(Tile.BOX)


def part2(data: str):
    warehouse_str, dir_str = data.split('\n\n')
    
    warehouse_list = []
    for line in warehouse_str.split('\n'):
        warehouse_row = []
        for char in line.strip():
            if char == '@': 
                warehouse_row.append(Tile('@'))
                warehouse_row.append(Tile('.'))
            elif char == 'O':
                warehouse_row.append(Tile('['))
                warehouse_row.append(Tile(']'))
            else:
                warehouse_row.append(Tile(char))
                warehouse_row.append(Tile(char))
        warehouse_list.append(warehouse_row)
    warehouse = Warehouse(warehouse_list)
    directions = [Direction(char) for char in dir_str if char != '\n']
    # directions = [Direction.LEFT, Direction.DOWN, Direction.LEFT, Direction.UP]

    print(warehouse)
    for direction in directions:
        warehouse.move_part2(direction)
        time.sleep(0.3)
        print(f"{"\033[F"}{"\033[A" * (len(warehouse.tiles)-1)}", end='')
        print(warehouse)
    return warehouse.sum_gps_coordinates(Tile.LEFT_BOX)


def main():
    with open("15. Warehouse Woes/test4.txt", 'r') as f:
        data = f.read()
    print(part2(data))


if __name__ == "__main__":
    main()