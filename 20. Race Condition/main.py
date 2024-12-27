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


class Cheat:
    def __init__(self, start_point: Coord, end_point: Coord, time_saved: int):
        self.start_point = start_point
        self.end_point = end_point
        self.time_saved = time_saved
    
    def __eq__(self, value):
        return (self.start_point == value.start_point and
                self.end_point == value.end_point and
                self.time_saved == value.time_saved)

    def __hash__(self):
        return hash((self.start_point, self.end_point, self.time_saved))


class Track:
    def __init__(self, track_coords: list[Coord]):
        self.track_times = {coord: i for i, coord in enumerate(track_coords)}

    def generate_cheats(self, cheat_time: int) -> set[Cheat]:
        cheats: set[Cheat] = set()
        for coord, time in self.track_times.items():
            for x_offset in range(0, cheat_time+1):
                for y_offset in range(0, cheat_time+1 - x_offset):
                    for mul in [Coord(1, 1), Coord(-1, 1), Coord(1, -1), Coord(-1, -1)]:
                        if (end_coord := coord + Coord(x_offset, y_offset) * mul) in self.track_times:
                            cheats.add(Cheat(coord, end_coord, self.track_times[end_coord] - time - (x_offset+y_offset)))             
        return cheats


def parse_input(lines: list[str]) -> Track:
    for y, line in enumerate(lines):
        coord = False
        for x, cell in enumerate(line):
            if cell == 'S': 
                coord = Coord(x, y)
                break
        if coord is not False: break
    previous_coord = None
    track_coords: list[Coord] = []
    while True:
        track_coords.append(coord)
        if lines[coord.y][coord.x] == 'E': break
        for offset_coord in [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]:
            new_coord = coord + offset_coord
            if lines[new_coord.y][new_coord.x] == '#' or new_coord == previous_coord: continue
            previous_coord = coord
            coord = new_coord
            break
    return Track(track_coords)


def part1(track: Track) -> int:
    return sum(cheat.time_saved >= 100 for cheat in track.generate_cheats(2))


def part2(track: Track) -> int:
    return sum(cheat.time_saved >= 100 for cheat in track.generate_cheats(20))


def main():
    with open('20. Race Condition/input.txt', 'r') as f:
        lines = f.readlines()
    track = parse_input(lines)
    for i, part in enumerate([part1, part2]):
        print(f'Part {i+1}: {part(track)}')


if __name__ == '__main__':
    main()