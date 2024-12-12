from copy import deepcopy
from enum import Enum

class Side(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def next_coord(self, coord: tuple[int, int], clockwise: bool = True) -> tuple[int, int]:
        match self:
            case Side.UP:
                dir = [[-1, 0], [1, 0]][clockwise]
            case Side.RIGHT:
                dir = [[0, -1], [0, 1]][clockwise]
            case Side.DOWN:
                dir = [[1, 0], [-1, 0]][clockwise]
            case Side.LEFT:
                dir = [[0, 1], [0, -1]][clockwise]
        return coord[0] + dir[0], coord[1] + dir[1]
    
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

class Fence:
    def __init__(self, coord: tuple[int, int], side: Side):
        self.coord = coord
        self.side = side

    def __str__(self) -> str:
        return f"[{self.coord}, {self.side}]"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other: 'Fence'):
        return self.coord == other.coord and self.side == other.side
    
    def __hash__(self):
        return hash((self.coord, self.side))



class Region:
    def __init__(self, plot_coords: set[tuple[int, int]], char: str):
        self.plot_coords = plot_coords
        self.char = char
    
    def fences(self) -> set[Fence]:
        fences: set[Fence] = set()
        for coord in self.plot_coords:
            for dir_index, dir_coord in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
                side = coord[0] + dir_coord[0], coord[1] + dir_coord[1]
                if side not in self.plot_coords:
                    fences.add(Fence(side, Side(dir_index)))
        return fences
    
    def corners(self) -> list[tuple[int, int]]:
        corners: dict[tuple[int, int], int] = {}
        for coord in self.plot_coords:
            for corner_offset in [(0, 0), (1, 0), (1, 1), (0, 1)]:
                corner = coord[0] + corner_offset[0], coord[1] + corner_offset[1]
                if corner in corners: corners[corner] += 1
                else: corners[corner] = 1
        extra_corners = set()
        for corner, occ in corners.items():
            if occ != 2: continue
            pattern = []
            for dir in [(0, 0), (0, -1), (-1, -1), (-1, 0)]:
                coord = corner[0] + dir[0], corner[1] + dir[1]
                if coord in self.plot_coords: 
                    pattern.append(1)
                else:
                    pattern.append(0)
            if pattern in (
                    [1, 0, 1, 0],
                    [0, 1, 0, 1]
                ):
                extra_corners.add(coord)
        corners: list[tuple[int, int]] = [corner for corner, occ in corners.items() if occ in (1, 3)]
        for corner in extra_corners:
            corners.append(corner)
            corners.append(corner)
        if len(corners) % 2 != 0:
            pass
        return corners
            
    def perimeter(self) -> int:
        return len(self.fences())
    
    def area(self) -> int:
        return len(self.plot_coords)

    def price(self) -> int:
        return self.perimeter() * self.area()

class Farm:
    def __init__(self, plots: list[list[str]]):
        self._plots = plots
    
    def get_regions(self) -> list[Region]:
        plots = deepcopy(self._plots)
        regions: set[Region] = set()
        for y, row in enumerate(self._plots):
            for x, char in enumerate(row):
                if (region_set := Farm.find_whole_region(char, (x, y), plots)):
                    regions.add(Region(region_set, char))
        return regions
    
    @staticmethod
    def find_whole_region(target_char: str, coord: tuple[int, int], grid: list[list[str]]) -> set[tuple[int, int]]:
        def get(x: int, y: int) -> str:
            if 0 > x or 0 > y: return '*'
            try: return grid[y][x]
            except IndexError: return '*'    
        if get(*coord) != target_char:
            return set()
        coord_set = set()
        coord_set.add(coord)
        grid[coord[1]][coord[0]] = '*'     
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_coord = coord[0] + dir[0], coord[1] + dir[1]
            coord_set = coord_set.union(Farm.find_whole_region(target_char, next_coord, grid))
        return coord_set

def part1(farm: Farm) -> int:
    return sum(
        region.price()
        for region in farm.get_regions()
    )

def part2(farm: Farm) -> int:
    return sum(
        len(region.corners()) * region.area() 
        for region in farm.get_regions()
    )

def main():
    with open("12. Garden Groups/input.txt", 'r') as f:
        lines = f.readlines()
    farm = Farm([list(line.strip()) for line in lines])
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(farm)}")
    

if __name__ == '__main__':
    main()