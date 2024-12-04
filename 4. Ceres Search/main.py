from copy import deepcopy

def search1(lines: list[list[str]], origin: tuple[int, int]):
    letter = lines[origin[0]][origin[1]]
    occurence = 0
    if letter == 'X':
        sequence = ['M', 'A', 'S']
    elif letter == 'S':
        sequence = ['A', 'M', 'X']
    else:
        return 0

    for dir in [0,1], [1, 0], [1, -1], [1, 1]:
        point = origin
        for i in range(3):
            point = point[0] + dir[0], point[1] + dir[1]
            if not (0 <= point[0] < len(lines)) or not (0 <= point[1] < len(lines[1])):
                break
            if lines[point[0]][point[1]] != sequence[i]:
                break
        else:
            occurence += 1
    return occurence

def search2(lines: list[list[str]], origin: tuple[int, int]):
    letter = lines[origin[0]][origin[1]]
    sequences = {'M': ['A', 'S'],
                 'S': ['A', 'M']}
    if letter not in sequences:
        return 0
    sequence = sequences[letter]
    if (origin[1] >= (len(lines[0]) - 2) or (origin[0] >= (len(lines) - 2))):
        return 0 
    if not (lines[origin[0]+1][origin[1]+1] == sequence[0] and
        lines[origin[0]+2][origin[1]+2] == sequence[1]):
        return 0
    letter = lines[origin[0]][origin[1] + 2]
    if letter not in sequences:
        return 0
    sequence = sequences[letter]
    if not (lines[origin[0]+1][origin[1]+1] == sequence[0] and
        lines[origin[0]+2][origin[1]] == sequence[1]):
        return 0
    return 1
    
    

def part1(lines: list[list[str]]):
    occurenses = 0
    for i, line in enumerate(lines):
        for j, _ in enumerate(line):
            occurenses += search1(lines, (i, j))
    return occurenses
        


def part2(lines):
    occurenses = 0
    for i, line in enumerate(lines):
        for j, _ in enumerate(line):
            occurenses += search2(lines, (i, j))
    return occurenses

def main():
    with open("4. Ceres Search/input.txt", 'r') as f:
        lines = f.readlines()
    input = [list(line.strip()) for line in lines]
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(deepcopy(input))}")

if __name__ == "__main__":
    main()