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
                cpu: CPU = replace(self, rb = self.rb ^ self.rc, ip = self.ip + 2)
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


def reverse_engineer(output: list[int]) -> int:
    a = 0
    for out in reversed(output):
        for i in range(0, 8):
            temp_a = a * 8 + i
            if decompiled_iteration(temp_a) == out:
                a = temp_a
                break  
    return a

def decompiled_iteration(a: int) -> int:
    b = (a % 8) ^ 0b010
    c = a // (2**b)
    b = (b ^ c) ^ 0b111
    return b % 8

def parse_input(string: str) -> CPU:
    ra, rb, rc = map(int, findall(r"Register .: (\d+)", string))
    program = [int(n) for n in search(r"Program:\s*([\d+,]+)", string)
               .group(1).split(',')]
    return CPU(ra, rb, rc, program, 0, [])


def part1(cpu: CPU) -> str:
    cpu = cpu.run()
    return cpu.current_output()


def part2() -> int:
    data = [2,4,1,2,7,5,4,5,0,3,1,7,5,5,3,0]
    return reverse_engineer(data)


def main():
    with open("17. Chronospatial Computer/input.txt", 'r') as f:
        data = f.read()
    cpu = parse_input(data)
    for i, result in enumerate([part1(cpu), part2()]):
        print(f'Part {i+1}: {result}')


if __name__ == '__main__':
    main()


# def dissasemble(program: list[int]) -> str:
    
#     def combo(operand: int) -> str:
#         if 0 <= operand <= 3: return str(operand)
#         if operand == 4: return 'A'
#         if operand == 5: return 'B'
#         if operand == 6: return 'C'

#     code = ''
#     for ip in range(0, len(program), 2):
#         opcode = program[ip]
#         operand = program[ip + 1]
#         match opcode:
#             case 0: code += f'adv {combo(operand)}\n'
#             case 1: code += f'bxl {operand}\n'
#             case 2: code += f'bst {combo(operand)}\n'
#             case 3: code += f'jnz {operand}\n'
#             case 4: code += f'bxc\n'
#             case 5: code += f'out {combo(operand)}\n'
#             case 6: code += f'bdv {combo(operand)}\n'
#             case 7: code += f'cdv {combo(operand)}\n'
#     return code