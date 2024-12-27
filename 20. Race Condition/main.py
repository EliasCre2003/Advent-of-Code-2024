from sys import setrecursionlimit

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
        elif type(other) is int:
            return Coord(self.x * other, self.y * other)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, value: 'Coord') -> bool:
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

    
    

class Track:
    def __init__(self, track_coords: list[Coord]):
        self.track_times = {coord: i for i, coord in enumerate(track_coords)}

    def generate_cheats(self) -> list[Cheat]:
        cheats: list[Cheat] = []
        for coord, time in self.track_times.items():
            for dir in [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]:
                if (other_coord := coord + dir * (cheat_len := 1)) in self.track_times: pass
                elif (other_coord := coord + dir * (cheat_len := 2)) in self.track_times: pass
                else: continue
                cheats.append(Cheat(coord, other_coord, self.track_times[other_coord] - time - cheat_len))
        return cheats




def parse_input(lines: list[str]) -> Track:
    for y, line in enumerate(lines):
        start_coord = False
        for x, cell in enumerate(line):
            if cell == 'S': 
                start_coord = Coord(x, y)
                break
        if start_coord is not False: break

    track_coords: list[Coord] = [] 
    def inner(coord: Coord) -> bool:
        if lines[coord.y][coord.x] == '#' or coord in track_coords: return False
        track_coords.append(coord)
        if lines[coord.y][coord.x] == 'E': return True
        for offset_coord in [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]:
            if inner(coord + offset_coord): return True
        return False
    inner(start_coord)
    return Track(track_coords)


def part1(track: Track) -> int:
    return sum(cheat.time_saved >= 100 for cheat in track.generate_cheats())


def part2(track: Track):
    ...


def main():
    setrecursionlimit(999999)
    with open('20. Race Condition/input.txt', 'r') as f:
        lines = f.readlines()
    track = parse_input(lines)
    print(part1(track))


if __name__ == '__main__':
    main()