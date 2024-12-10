from enum import Enum
from itertools import product

class Equation:
    def __init__(self, result: int, terms: list[int]):
        self.terms = terms
        self.result = result

    def evaluate(self, opperators: list[str]) -> bool:
        if len(opperators) != len(self.terms) - 1:
            return False
        total: int = self.terms[0]
        for i, opperator in enumerate(opperators):
            term = self.terms[i+1]
            match opperator:
                case '+': total += term
                case '*': total *= term
                case '|': total = int(str(total) + str(term))
                case _: raise ValueError(opperator)
        return total == self.result
    

def all_opp_combs(n: int, choises: str):
    return [list(operators) for operators in product(choises, repeat=n)]

def check_all(equations: list[Equation], operators) -> int:
    total = 0
    for equation in equations:
        for op_comb in all_opp_combs(len(equation.terms) - 1, operators):
            if not equation.evaluate(op_comb): continue
            total += equation.result
            break
    return total

def part1(equations: list[Equation]):
    return check_all(equations, '+*')

def part2(equations: list[Equation]):
    return check_all(equations, '+*|')

def main():
    with open("7. Bridge Repair/test.txt", 'r') as f:
        lines = f.readlines()
    equations = [Equation(int((parts := line.strip().split(': '))[0]), 
                [int(num) for num in parts[1].split(' ')]) 
                 for line in lines]
    for i, part in enumerate([part1, part2]):
        print(f"Part {i+1}: {part(equations)}")
    
if __name__ == "__main__":
    main()