class File:
    def __init__(self, id: int, size: int):
        self.id = id
        self.size = size
    
    def __str__(self) -> str:
        return str(self.id) * self.size

    def __repr__(self):
        return str(self)


def checksum(files: list[File]) -> int:
    index, total = 0, 0
    for file in files:
        if type(file) is not File:
            index += file
            continue
        for _ in range(file.size):
            total += file.id * index
            index += 1
    return total

def parse_data(data: str):
    return (
        [File(i // 2, int(data[i])) for i in range(0, len(data), 2)],
        [int(data[i]) for i in range(1, len(data), 2)]
    )

def part1(data: str):
    files, free_space = parse_data(data)
    index = 1
    while free_space:
        free_block = free_space.pop(0)
        if free_block == 0:
            index += 1
            continue
        last_file = files[-1]
        if free_block < last_file.size:
            files.insert(index, File(last_file.id, free_block))
            last_file.size -= free_block
            index += 1
        else:
            last_file = files.pop(-1)
            files.insert(index, File(last_file.id, last_file.size))
            if free_block == last_file.size:
                index += 1
            else:
                free_space.insert(0, free_block-last_file.size)
        index += 1
    return checksum(files)


def part2(data: str):
    files, free_space = parse_data(data)
    combined: list[File | int] = []
    for i in range(max(len(files), len(free_space))):
        combined.append(files[i])
        try: combined.append(free_space[i])
        except IndexError: break
    moved: set[File] = set()
    for i in range(len(combined) - 1, -1, -1):
        if type(file := combined[i]) is not File: continue
        if file in moved: continue
        if file.id == 4:
            pass
        for j in range(len(combined)):
            if i == j: break
            if type(free_block := combined[j]) is File: continue
            if free_block == file.size:
                combined[i], combined[j] = combined[j], combined[i]
            elif free_block > file.size:
                combined[j] = free_block - file.size

                if type(combined[i-1]) is not File:
                    combined[i-1] += file.size
                    if i+1 < len(combined) and type(combined[i+1]) is not File:
                        combined[i-1] += combined[i+1]
                        combined.pop(i+1)                             
                elif i+1 < len(combined) and  type(combined[i+1]) is not File:
                    combined[i+1] += file.size
                else:
                    combined.insert(i+1, file.size)

                combined.pop(i)
                combined.insert(j, file)
            else:
                continue
            moved.add(file)
            break
    return checksum(combined)

def main():
    with open("9. Disk Fragmenter/input.txt", 'r') as f:
        data = f.read().strip()
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(data)}")
if __name__ == "__main__":
    main()
