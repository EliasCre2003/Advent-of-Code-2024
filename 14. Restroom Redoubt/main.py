from re import findall
from math import prod


class Robot:
    def __init__(self, start_pos: tuple[int, int], velocity: tuple[int, int]):
        self.position = start_pos
        self.velovity = velocity

    def step(self, n: int, dimensions: tuple[int, int]):
        self.position = (
            (self.position[0] + self.velovity[0] * n) % dimensions[0],
            (self.position[1] + self.velovity[1] * n) % dimensions[1]
        )


def count_quadrants(robots: list[Robot], dimensions: tuple[int, int]) -> tuple[int, int, int, int]:
    middle = dimensions[0] // 2, dimensions[1] // 2
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        if robot.position[0] < middle[0] and robot.position[1] < middle[1]:
            quadrants[0] += 1
        elif robot.position[0] > middle[0] and robot.position[1] < middle[1]:
            quadrants[1] += 1
        elif robot.position[0] < middle[0] and robot.position[1] > middle[1]:
            quadrants[2] += 1
        elif robot.position[0] > middle[0] and robot.position[1] > middle[1]:
            quadrants[3] += 1
    return tuple(quadrants)


def parse_robots(input: str) -> list[Robot]:
    return [Robot((int(line[0]), int(line[1])), (int(line[2]), int(line[3]))) 
            for line in findall(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', input)]


def part1(robots: list[Robot], test: bool = False):
    dimensions = (11, 7) if test else (101, 103)
    for robot in robots: robot.step(100, dimensions)
    return prod(count_quadrants(robots, dimensions))

def part2(robots: list[Robot], test: bool = False):
    if test: return None
    dimensions = (101, 103)
    i = 1
    while True:
        for robot in robots: robot.step(1, dimensions)
        positions = set((robot.position[0],robot.position[1]) for robot in robots)
        for y in range(dimensions[1]):
            line_len = 0
            for x in range(dimensions[0]):
                if (x, y) in positions:
                    if x == 0: line_len += 1
                    elif (x-1, y) in positions:
                        line_len += 1
                    if line_len > 20:
                        return i
                else:
                    line_len = 0
        i += 1


def main():
    test = False
    with open(f"14. Restroom Redoubt/{["input", "test"][test]}.txt", 'r') as f:
        input = f.read()
    for i, part in enumerate([part1, part2]):
        robots = parse_robots(input)
        print(f"Part {i+1} {part(robots, test=test)}")

    
if __name__ == '__main__':
    main()