class File:
    def __init__(self, id: int, size: int):
        self.id = id
        self.size = size
    
    def __str__(self) -> str:
        return str(self.id) * self.size

    def __repr__(self):
        return str(self)
    
def pretty_print(data):
    empty = False
    id = 0
    for num in data:
        num = int(num)
        if empty:
            print('.' * num, end='')
        else:
            print(str(id) * num, end='')
            id += 1
        empty = not empty
    print()

def checksum(files: list[File]) -> int:
    index = 0
    total = 0
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

    def pretty_print():
        for element in combined:
            if type(element) is File:
                print(element, end='')
            else:
                print('.' * element, end='')
        print()
    moved: set[File] = set()
    for i in range(len(combined) - 1, -1, -1):
        pretty_print()
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

                combined.pop(i)
                combined.insert(j, file)
            else:
                continue
            moved.add(file)
            break
    # files = [file for file in files if type(file) if File]
    return checksum(combined)
        
def part3(data: str):
    memory: list[int | str] = []
    empty = False
    id = 0
    for file in data:
        for _ in range(int(file)):
            if empty: memory.append('.')
            else: memory.append(id)
        id += not empty
        empty = not empty

    
    print(''.join(str(mem) if type(mem) is int else mem for mem in memory))


def main():
    with open("9. Disk Fragmenter/test.txt", 'r') as f:
        data = f.read().strip()
    print(part3(data))
if __name__ == "__main__":
    main()
