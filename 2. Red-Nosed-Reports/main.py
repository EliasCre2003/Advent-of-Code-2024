class Report:
    def __init__(self, levels: list[int]):
        self.levels = levels

    def is_safe(self) -> bool:
        decreasing = self.levels[0] >= self.levels[1]
        for i in range(len(self.levels) - 1):
            diff = self.levels[i+1] - self.levels[i]
            if (diff > -1 or diff < -3) and decreasing:
                return False
            if (diff > 3 or diff < 1) and not decreasing:
                return False
        return True
    

def part1(reports: list[Report]) -> int:
    return sum(1 for report in reports if report.is_safe())

def part2(reports: list[Report]) -> int:
    n_safe = 0
    for report in reports:
        if report.is_safe():
            n_safe += 1
            continue
        for i in range(len(report.levels)):
            new_levels = report.levels.copy()
            new_levels.pop(i)
            if Report(new_levels).is_safe():
                n_safe += 1
                break
    return n_safe
            

def main():
    with open("2. Red-Nosed-Reports/input.txt", 'r') as f:
        lines = f.readlines()
    
    reports = [Report([int(num) for num in line.strip().split()]) for line in lines]
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(reports)}")

if __name__ == "__main__":
    main()