
import re
from typing import Dict, List

import enum


class Case:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def __hash__(self):
        return hash(self.symbol)

    def __str__(self):
        return self.symbol

class EmptyCase:
    def __init__(self):
        pass

    def __hash__(self):
        return hash(None)

    def __str__(self):
        return "Empty"


class Command(enum.Enum):
    still = 0
    left = 1
    right = 2


class Instruction():
    def __init__(self, case: Case, next_: str, sub: str, command: Command):
        self.case = case
        self.next_state = next_
        self.substitution = sub
        self.command = command

    def __repr__(self):
        return f"Instruction< Case: {self.case}, \
            Next State: {self.next_state}, Substitution: {self.substitution}, \
            Operation: {self.command}>"


class State():
    def __init__(self, instructions: "List[Instruction]" = []):
        self.instructions = { str(i.case) : i for i in instructions }

    def check_case(self, case: str):
        return self.instructions[case]

    def insert_instruction(self, new_: Case):
        self.instructions[str(new_.case)] = new_

    def __repr__(self):
        return f"State< {self.instructions} >"


class TuringProgram:
    def __init__(self):
        self.states: "Dict[str, State]" = {}

    def load_program(self, state_list: "Dict[str, State]"):
        self.states = state_list

    def get_state(self, state_name: str):
        return self.states[state_name]


class Tape():
    def __init__(self):
        self.state = []
        self.pos = 0

    def load_state(self, state: list):
        self.state = state.copy()

    def move_left(self):
        if self.pos >= len(self.state)-1:
            self._increase_state_size_right()
        self.pos += 1

    def move_right(self):
        if self.pos == 0:
            self._increase_state_size_left()
        self.pos -= 1

    def _increase_state_size_right(self):
        self.state += [None] * 5
        # self.pos += 5

    def _increase_state_size_left(self):
        self.state = [None] * 5 + self.state
        self.pos += 5

    def read(self):
        return self.state[self.pos]

    def write(self, value):
        self.state[self.pos] = value

    def __str__(self):
        res = '|'
        for el in self.state:
            if el is not None:
                res += f" {el} |"
        return res


class TuringMachine():
    def __init__(self, program: str):
        self.state = ''
        self.finish = None
        self._parse_program(program)
        self.tape = Tape()

    def load_tape(self, tape: list):
        self.tape.load_state(tape)

    def _parse_program(self, program_string: str):
        r = re.compile(r"#init\s+(\w+)")
        self.state = r.findall(program_string)[0]

        r = re.compile(r"#end\s+(\w+)")
        if len(end := r.findall(program_string)) > 0:
            self.finish = end[0]

        r = re.compile(r"\((\w+),\s*(\w+)\) > \((\w+),\s*(\w+),\s*([><-])\)")

        program: "Dict[str, State]" = {}

        for line in program_string.splitlines():
            move = r.findall(line)

            if len(move) == 0:
                continue

            state, case, next_, sub, op = move[0]

            # Create list if state is not present
            if state not in program:
                program[state] = State()

            if op == '>':
                op = Command.right
            elif op == '<':
                op = Command.left
            elif op == '-':
                op = Command.still

            # Python >3.10:
            # match op:
            #     case '>':
            #         op = Command.right
            #     case '<':
            #         op = Command.left
            #     case '-':
            #         op = Command.still

            case = Case(case) if case != "clc" else EmptyCase()
            # print(case)
            program[state].insert_instruction(Instruction(
                case=case,
                next_=next_,
                sub=sub,
                command=op
            ))

        self.program = TuringProgram()
        self.program.load_program(program)

    def execute_program(self):
        last_pos = 0
        last_val = ''
        diff_count = 0
        while True:
            if not self.execute_one():
                return

            # Check if machine is stalled
            curr_pos = self.tape.pos
            curr_val = self.tape.read()
            if curr_pos == last_pos and curr_val == last_val:
                diff_count += 1
            else:
                diff_count = 0
            last_pos = curr_pos
            last_val = curr_val

            # Exit the program
            if diff_count > 5:
                return

    def execute_one(self) -> bool:
        val = self.tape.read()
        if not val:
            val = 'Empty'

        if self.state == self.finish:
            return False

        try:
            state = self.program.get_state(self.state)
            instruction = state.check_case(val)
        except KeyError:
            return False

        if instruction:
            self.state = instruction.next_state

            self.tape.write(instruction.substitution)
            if instruction.command == Command.left:
                self.tape.move_left()
            elif instruction.command == Command.right:
                self.tape.move_right()
            
            # Python >3.10:

            # match instruction.command:
            #     case Command.left:
            #         self.tape.move_left()
            #     case Command.right:
            #         self.tape.move_right()
            #     case _:
            #         pass

            return True
        else:
            return False




import argparse


def main():
    parser = argparse.ArgumentParser(description="Simulatore di macchina di turing.")
    parser.add_argument('file', default='program.tur', nargs='?', type=str)
    parser.add_argument('--tape', '-t', nargs='*', default=[''], type=str)

    args = parser.parse_args()
    # print(args)

    try:
        with open(args.file, 'r') as f:
            program = f.read()
    except FileNotFoundError:
        print(f"Il file {args.file} non è stato trovato, ricontrollare l'input.")
        return

    tm = TuringMachine(program=program)

    tm.load_tape(args.tape)

    tm.execute_program()

    print("Stato finale del nastro:")
    print(tm.tape)
    # print(tm.tape.pos)


if __name__ == '__main__':
    main()