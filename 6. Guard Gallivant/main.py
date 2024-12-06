class GameMap:
    def __init__(self, cells: list[list[str]], start_pos: tuple[int, int]) -> None:
        self.cells = cells
        self.start_pos = start_pos

    def get_at(self, coord: tuple[int, int], outside_char: str = '*'):
        if not (0 <= coord[0] and 0 <= coord[1]):
            return outside_char
        try:
            return self.cells[coord[1]][coord[0]]
        except IndexError:
            return outside_char
    

def parse_map(lines: list[str]) -> GameMap:
    cells = [None] * len(lines)
    for i, line in enumerate(lines):
        cells[i] = list(line)
        if '^' in line: start_pos = line.index('^'), i
    return GameMap(cells, start_pos)


def part1(game_map: GameMap) -> int:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    dir_index = 0
    position =  game_map.start_pos
    visited_pos: set[tuple[int, int]] = set()
    while True:
        direction = directions[dir_index]
        next_pos = (position[0] + direction[0], position[1] + direction[1])
        match game_map.get_at(next_pos):
            case '#':
                dir_index = (dir_index + 1) % 4
            case '*':
                visited_pos.add(position)
                break
            case _:
                visited_pos.add(position)
                position = next_pos
    return len(visited_pos)            


def part2(game_map: GameMap):
    ...


def main():
    with open("6. Guard Gallivant/input.txt", 'r') as f:
        lines = f.readlines()

    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(parse_map(lines))}")


if __name__ == "__main__":
    main()