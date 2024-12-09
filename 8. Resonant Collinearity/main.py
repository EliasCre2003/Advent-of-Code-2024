class AntennaCoordinate:
    def __init__(self, x, y, frequency):
        self.x = x
        self.y = y
        self.frequency = frequency
    
    def xy(self) -> tuple[int, int]:
        return self.x, self.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.frequency))


class CityMap:
    def __init__(self, cells: list[str]):
        self.cells = cells
        self.antennas = {}
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                if cell == '.':
                    continue
                if cell not in self.antennas:
                    self.antennas[cell] = set()
                self.antennas[cell].add((x, y))

    def get_at(self, coord: tuple[int, int], default_val: str = '|'):
        if 0 > coord[0] or 0 > coord[1]: return default_val
        try: return self.cells[coord[1]][coord[0]]
        except IndexError: return default_val

    def generate_pairs(self) -> set[tuple[AntennaCoordinate, AntennaCoordinate]]:
        pairs: set[tuple[AntennaCoordinate, AntennaCoordinate]] = set()
        for frequency, coords in self.antennas.items():
            for i in range(length := len(coord_list := list(coords))):
                antenna1 = coord_list[i]
                for j in range(i+1, length):
                    antenna2 = coord_list[j]
                    pairs.add((AntennaCoordinate(*antenna1, frequency), 
                               AntennaCoordinate(*antenna2, frequency)))
        return pairs
    
    # def num_antinodes(self) -> int:
    #     antinodes: set[tuple[int, int]] = set()
    #     for pair in self.generate_pairs():
    #         for antinode_coord in antinode_coords(pair):
    #             if self.get_at(antinode_coord.xy()) != '|':
    #                 antinodes.add(antinode_coord.xy())
    #     return len(antinodes)


def antinode_coords(antenna_coords: tuple[AntennaCoordinate, AntennaCoordinate], depth: int = 2) -> list[AntennaCoordinate, AntennaCoordinate]:
    difference = antenna_coords[1].x - antenna_coords[0].x, antenna_coords[1].y - antenna_coords[0].y
    antinodes =  []
    for i in range(1, (depth // 2) + 1):
        antinodes.append(AntennaCoordinate(antenna_coords[0].x - i * difference[0], antenna_coords[0].y - i * difference[1], antenna_coords[0].frequency))
        antinodes.append(AntennaCoordinate(antenna_coords[1].x + i * difference[0], antenna_coords[1].y + i * difference[1], antenna_coords[1].frequency))
    return antinodes

    # return (AntennaCoordinate(antenna_coords[0].x - difference[0], antenna_coords[0].y - difference[1], antenna_coords[0].frequency),
    #         AntennaCoordinate(antenna_coords[1].x + difference[0], antenna_coords[1].y + difference[1], antenna_coords[1].frequency))

def part1(city_map: CityMap) -> int:
    antinodes: set[tuple[int, int]] = set()
    for pair in city_map.generate_pairs():
        for antinode_coord in antinode_coords(pair):
            if city_map.get_at(antinode_coord.xy()) != '|':
                antinodes.add(antinode_coord.xy())
    return len(antinodes)

def part2(city_map: CityMap) -> int:
    antinodes: set[tuple[int, int]] = set()
    for pair in city_map.generate_pairs():
        for antinode_coord in antinode_coords(pair, 100):
            if city_map.get_at(antinode_coord.xy()) != '|':
                antinodes.add(antinode_coord.xy())
    for antinode in antinodes:
        city_map.cells[antinode[1]][antinode[0]] = '#'
    total = len(antinodes)
    for row in city_map.cells:
        for cell in row:
            if cell not in ('.#'): total += 1
    return total
    # return len(antinodes)

def main():
    with open("8. Resonant Collinearity/input.txt", 'r') as f:
        lines = f.readlines()
    
    city_map = CityMap([list(line.strip()) for line in lines])

    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(city_map)}")
    
if __name__ == "__main__":
    main()
