class TopographicMap:
    def __init__(self, map: list[list[int]]):
        self.map = map

    def get_at(self, coord: tuple[int, int], error_value = -1) -> int:
        if 0 > coord[0] or 0 > coord[1]: return error_value
        try: return self.map[coord[1]][coord[0]]
        except IndexError: return error_value

    def trailheads(self) -> list[tuple[int, int]]:
        return [
            (x, y) 
            for y, row in enumerate(self.map) 
            for x, _ in enumerate(row) 
            if self.get_at((x, y)) == 0
        ]
    
    def dfs(self, 
            coord: tuple[int, int], 
            reached: set[tuple[int, int]], 
            paths: set[list[tuple[int, int]]], 
            path: list[tuple[int, int]],  
            previous: int = -1
        ) -> tuple[int, int]:
        level = self.get_at(coord)
        if level != previous + 1: return 0, 0
        if level == 9:
            reached.add(coord)
            paths.add(tuple(path))
            return 0, 0
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            path = path.copy()
            next_coord = (coord[0] + direction[0], coord[1] + direction[1])
            path.append(next_coord)
            self.dfs(next_coord, reached, paths, path, level)
        return len(reached), len(paths)


def main():
    with open("10. Hoof It/input.txt", 'r') as f:
        lines = f.readlines()
    topo_map = TopographicMap(
        [[int(n) if n != '.' else -1 for n in line.strip()] 
         for line in lines]
    )
    total1, total2 = 0, 0
    for trailhead in topo_map.trailheads():
        result = topo_map.dfs(trailhead, set(), set(), [])
        total1 += result[0]
        total2 += result[1]
    print(f"Part 1: {total1}\nPart 2: {total2}" )


if __name__ == "__main__":
    main()
