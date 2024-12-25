class Space:
    def __init__(self, byte_positions: list[tuple[int, int]], size: tuple[int, int]):
        self.byte_positions = byte_positions
        self.bytes: list[list[bool]] = [[False for _ in range(size[0])] for _ in range(size[1])]
        self.size = size
        self.bytes_dropped: int = 0

    def drop_bytes(self, n: int = 1):
        for _ in range(n):
            if self.bytes_dropped == len(self.byte_positions): return
            coord = self.byte_positions[self.bytes_dropped]
            self.bytes[coord[1]][coord[0]] = True
            self.bytes_dropped += 1

    def is_corrupted(self, coord: tuple[int, int]) -> bool:
        if 0 > coord[0] or 0 > coord[1]: return True
        try: return self.bytes[coord[1]][coord[0]]
        except IndexError: return True

    def shortest_path(self) -> int:
        '''An implementation of the A star algorithm for finding the length of the shortest path to the end'''
        goal = self.size[0]-1, self.size[1]-1
        open_list: dict[tuple[int, int], set[tuple[int, int]]] = {(0, 0): {(0, 0)}}
        closed_list: dict[tuple[int, int], set[tuple[int, int]]] = {}
        while open_list:
            q = min(open_list.items(), key=lambda item: min(item[1], key=lambda tup: sum(tup)))
            q = q[0], min(q[1], key=sum)
            open_list[q[0]].remove(q[1])
            if len(open_list[q[0]]) == 0: open_list.pop(q[0])
            for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_coord = q[0][0] + dir[0], q[0][1] + dir[1]
                if self.is_corrupted(new_coord): continue
                if new_coord == goal: return sum(q[1])
                g = q[1][0] + 1
                h = distance(new_coord, goal)
                if (new_coord in open_list and 
                    len(open_list[new_coord]) > 0 and
                    sum(min(open_list[new_coord], key=sum)) < g + h):
                        continue
                if (new_coord not in closed_list or
                    len(closed_list[new_coord]) == 0 or
                    sum(min(closed_list[new_coord], key=sum)) >= g + h):
                    if new_coord not in open_list:
                        open_list[new_coord] = {(g, h)}
                    else:
                        open_list[new_coord].add((g, h))
            if q[0] not in closed_list:
                closed_list[q[0]] = set()
            closed_list[q[0]].add(q[1])

    def pretty_print(self):
        for row in self.bytes:
            print(''.join('#' if byte else '.' for byte in row))

    def reset(self):
        self.bytes_dropped = 0
        for y in range(len(self.bytes)):
            for x in range(len(self.bytes[0])):
                self.bytes[y][x] = False


def distance(coord1, coord2) -> int:
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def parse_input(lines: list[str], size: tuple[int, int]) -> Space:
    coords = [(int((pair := line.strip().split(','))[0]), int(pair[1])) for line in lines]
    return Space(coords, size)


def part1(space: Space, length: int) -> int:
    for _ in range(length):
        space.drop_bytes()
    return space.shortest_path()


def part2(space: Space) -> str:
    max_time, min_time = len(space.byte_positions), 0
    while max_time - min_time > 1:
        time = (max_time - min_time) // 2 + min_time
        space.drop_bytes(time)
        if space.shortest_path(): min_time = time
        else: max_time = time
        space.reset()
    return str(space.byte_positions[time])[1:-1].replace(' ','')


def main():
    test = False
    with open(f"18. RAM Run/{['input', 'test'][test]}.txt", 'r') as f:
        lines = f.readlines()
    space = parse_input(lines, size=[(71, 71), (7, 7)][test])
    for i, result in enumerate([part1(space, [1024, 12][test]), part2(space)]):
        print(f"Part {i+1}: {result}")
    

if __name__ == '__main__':
    main()