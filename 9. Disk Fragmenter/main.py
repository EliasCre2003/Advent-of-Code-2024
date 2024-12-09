class File:
    def __init__(self, id: int, size: int):
        self.id = id
        self.size = size

def part1(files: list[File]):
    ...

def main():
    with open("9. Disk Fragmenter/test.txt", 'r') as f:
        data = f.read.strip()
    files: list[File] = []
    for i in range(len(data)):
        id = len(files)
        files.append(File(id, int(data[i])))
if __name__ == "__main__":
    main()
