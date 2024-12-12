from copy import deepcopy

class Region:
    def __init__(self, plot_coords: set[tuple[int, int]], char: str):
        self.plot_coords = plot_coords
        self.char = char

    def perimeter(self) -> int:
        total = 0
        for coord in self.plot_coords:
            for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                side = coord[0] + dir[0], coord[1] + dir[1]
                if side not in self.plot_coords:
                    total += 1
        return total


class Farm:
    def __init__(self, plots: list[list[str]]):
        self.plots = plots
    
    def get_regions(self) -> list[Region]:
        plots = deepcopy(self.plots)
        regions: set[Region] = set()
        for y, row in enumerate(self.plots):
            for x, char in enumerate(row):
                if (region_set := Farm.dfs(char, (x, y), plots)):
                    regions.add(Region(region_set, char))
        return regions
    
    @staticmethod
    def dfs(target_char: str, coord: tuple[int, int], grid: list[list[str]]) -> set[tuple[int, int]]:
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
            coord_set = coord_set.union(Farm.dfs(target_char, next_coord, grid))
        return coord_set
    
def main():
    with open("12. Garden Groups/input.txt", 'r') as f:
        lines = f.readlines()
    
    farm = Farm([list(line.strip()) for line in lines])
    regions = farm.get_regions()
    print(sum(
        region.perimeter() * len(region.plot_coords) 
        for region in regions
    ))

if __name__ == '__main__':
    main()