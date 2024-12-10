# class Path:
#     def __init__(self, coords: list[int])

class TopographicMap:
    def __init__(self, map: list[list[int]]):
        self.map = map
        self.trailheads = list(
            (x, y) 
            for y, row in enumerate(self.map) 
            for x, _ in enumerate(row) 
            if self.get_at((x, y)) == 0
        )

    def get_at(self, coord: tuple[int, int]) -> int:
        if 0 > coord[0] or 0 > coord[1]: return -1
        try: return self.map[coord[1]][coord[0]]
        except IndexError: return -1
    
    def dfs(self, 
            coord: tuple[int, int], 
            reached: set[tuple[int, int]], 
            paths: set[list[tuple[int, int]]], 
            path: list[tuple[int, int]],  
            previous: int = -1,
            part: int = 1) -> int:
        level = self.get_at(coord)
        if level == -1: return
        if level != previous + 1: return
        if level == 9:
            reached.add(coord)
            paths.add(tuple(path))
            return
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            path = path.copy()
            next_coord = (coord[0] + direction[0], coord[1] + direction[1])
            path.append(next_coord)
            self.dfs(next_coord, reached, paths, path, level, part)
        if part == 1:
            return len(reached)
        else:
            return len(paths)



def part1(tope_map: TopographicMap) -> int:
    total = 0
    for trailhead in tope_map.trailheads:
        total += tope_map.dfs(trailhead, set(), set(), [], part=1)
    return total

def part2(tope_map: TopographicMap) -> int:
    total = 0
    for trailhead in tope_map.trailheads:
        total += tope_map.dfs(trailhead, set(), set(), [], part=2)
    return total


def main():
    with open("10. Hoof It/input.txt", 'r') as f:
        lines = f.readlines()
    topo_map = TopographicMap(
        [[int(n) if n != '.' else -1 for n in line.strip()] 
         for line in lines]
    )
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(topo_map)}")


if __name__ == "__main__":
    main()
