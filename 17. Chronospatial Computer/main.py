from re import findall, search
from dataclasses import dataclass
from copy import replace

@dataclass(frozen=True)
class CPU:
    ra: int
    rb: int
    rc: int
    program: list[int]
    ip: int
    output: list[int]


    def next(self) -> 'CPU':
        opcode = self.program[self.ip]
        operand = self.program[self.ip+1]
        match opcode:
            case 0:
                numerator = self.ra
                denominator = 2**self.combo(operand)
                cpu: CPU = replace(self, ra = numerator // denominator, ip = self.ip + 2)
            case 1:
                cpu: CPU = replace(self, rb = self.rb ^ operand, ip = self.ip + 2)
            case 2:
                cpu: CPU = replace(self, rb = self.combo(operand) % 8, ip = self.ip + 2)
            case 3:
                cpu: CPU = replace(self, ip = operand if self.ra != 0 else self.ip + 2)
            case 4:
                cpu: CPU = replace(self, rb = self.rb ^ self. rc, ip = self.ip + 2)
            case 5:
                cpu: CPU = replace(self, output = self.output + [self.combo(operand) % 8], ip = self.ip + 2)
            case 6:
                numerator = self.ra
                denominator = 2**self.combo(operand)
                cpu: CPU = replace(self, rb = numerator // denominator, ip = self.ip + 2)
            case 7:
                numerator = self.ra
                denominator = 2**self.combo(operand)
                cpu: CPU = replace(self, rc = numerator // denominator, ip = self.ip + 2)
        return cpu

    def combo(self, operand: int) -> int:
        if 0 <= operand <= 3: return operand
        if operand == 4: return self.ra
        if operand == 5: return self.rb
        if operand == 6: return self.rc
        raise ValueError(f"Invalid combo operand {operand}")
    
    def run(self) -> 'CPU':
        while self.ip < len(self.program):
            self = self.next()
        return self
    
    def current_output(self) -> str:
        return ','.join([str(n) for n in self.output])
        
    
def parse_input(string: str) -> CPU:
    ra, rb, rc = map(int, findall(r"Register .: (\d+)", string))
    program = [int(n) for n in search(r"Program:\s*([\d+,]+)", string)
               .group(1).split(',')]
    return CPU(ra, rb, rc, program, 0, [])
    

def part1(cpu: CPU) -> str:
    cpu = cpu.run()
    return cpu.current_output()

def part2(cpu: CPU) -> int:
    # a = 97653057
    a = 0
    while True:
        # print(a)
        new_cpu = replace(cpu, ra = a)
        new_cpu = new_cpu.run()
        if new_cpu.program == new_cpu.output:
            return a
        print(new_cpu.output)
        a += 1

def main():
    with open("17. Chronospatial Computer/input.txt", 'r') as f:
        data = f.read()
    cpu = parse_input(data)
    print(part2(cpu))


if __name__ == '__main__':
    main()