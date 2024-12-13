from re import findall

class ClawMachine:
    def __init__(self, a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]):
        self.a = a
        self.b = b
        self.prize = prize
    
    def tokens_required(self) -> int:
        b_clicks = -((-self.a[1]*self.prize[0] + self.a[0]*self.prize[1]) / 
                     (self.a[1]*self.b[0] - self.a[0]*self.b[1]))
        a_clicks = (self.prize[0] - self.b[0] * b_clicks) / self.a[0]
        n_tokens = a_clicks * 3 + b_clicks
        if int(n_tokens) == n_tokens: return int(n_tokens)
        else: return 0
   

def parse_input(lines: list[str], error: int = 0) -> list[ClawMachine]:
    machines: list[ClawMachine] = []
    for i in range(0, len(lines), 4):
        a_button = findall(r'Button A: X\+(\d+), Y\+(\d+)', lines[i])[0]
        b_button = findall(r'Button B: X\+(\d+), Y\+(\d+)', lines[i+1])[0]
        prize = findall(r'Prize: X=(\d+), Y=(\d+)', lines[i+2])[0]
        machines.append(ClawMachine(
            (int(a_button[0]), int(a_button[1])), 
            (int(b_button[0]), int(b_button[1])),
            (int(prize[0]) + error, int(prize[1]) + error)
        ))
    return machines

def main():
    with open("13. Claw Contraption/input.txt", 'r') as f:
        lines = f.readlines()

    for i, error in enumerate([0, 10000000000000]):
        machines = parse_input(lines, error)
        result = sum(machine.tokens_required() for machine in machines)
        print(f"Part {i+1}: {result}")

    
if __name__ == '__main__':
    main()