"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.current_address = 0
        self.running = False

        self.instruction_set = {
            0b10000010: self.ins_ldi,
            0b01000111: self.ins_prn,
            0b10100010: self.ins_mul,
            0b00000001: self.ins_hlt
        }

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []
        filename = sys.argv[1]
        with open(f"examples/{filename}") as f:
            for line in f:
                line = line.split('#')
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                program.append(v)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        if address > 256 or address < 0:
            print(
                f"Invalid memory address: {address} - Must be between 0 and 256.")
        else:
            return self.ram[address]

    def ram_write(self, address, value):
        if address > 256 or address < 0:
            print(
                f"Invalid memory address: {address} - Must be between 0 and 256.")
        else:
            self.ram[address] = value

    def ins_ldi(self):
        reg_address = self.ram_read(self.current_address + 1)
        value = self.ram_read(self.current_address + 2)
        self.reg[reg_address] = value
        self.current_address += 3

    def ins_prn(self):
        print(self.reg[0])
        self.current_address += 2

    def ins_mul(self):
        self.reg[0] *= self.reg[1]
        self.current_address += 3

    def ins_hlt(self):
        print("Halting CPU")
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            instruction = self.ram[self.current_address]

            if instruction in self.instruction_set:
                self.instruction_set[instruction]()
            else:
                print("That is not a valid instruction.")
