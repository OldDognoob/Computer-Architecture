"""CPU functionality."""

# opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b10000111
MUL = 0b10100010

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        self.ram = [0] * 255 # bytes of memory
        self.reg = [0] * 8 # like variables
        self.halted = False

    def ram_read(self,mar):
        # accepts an address = mar and return its value
        return self.ram[mar] 

    def ram_write(self, mar, mdr):
        # takes a value = mdr writes it to the address = mar
        self.ram[mar] = mdr
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        try:
            address = 0

            with open(sys.argv[1]) as file: # use open() to open file
                for line in file: # read each line
                    comment_split = line.split('#') # remove comments
                    string_number = comment_split[0].strip() # convert to a number splitting and stripping

                    if string_number == '':
                        continue # ignore blank lines
                    val = int(string_number, 2)
                    print(string_number)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}:{sys.argv[1]} not found!")
            sys.exit(1)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def hlt(self):
        self.pc += 1
        self.running = False

    def run(self):
        """Run the CPU."""
        """
        running = True
        ir = self.ram[self.pc]
        while running:
            if ir == 0b10000010:
                print("0b10000010")
                ram = self.ram[self.pc + 1]
                num = self.ram[self.pc + 2]
                self.register[ram] = num
                self.pc += 1
            elif ir == 0b01000111:
                print("0b01000111")
                ram = self.ram[self.pc +1]
                self.pc += 3
            elif ir == 0b00000001:
                print("0b00000001")
                run = False
#            elif ir == HLT:
#                running = False
            else:
                print(f'Unknown instruction {ir} at address [{self.ram[self.pc]}]')
                run = False
                self.pc += 2
                ir = self.ram[self.pc]
        """
        instruction_length = 1 # bitshifted instruction
        while not self.halted:
            cmd = self.ram[self.pc]
            self.pc += instruction_length
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # halt
            if cmd == HLT:
                self.halted = True
                

            # LDI
            elif cmd == LDI:
                self.reg[operand_a] = operand_b
                instruction_length = 3

            # PRN
            elif cmd == PRN:
                print(self.reg[operand_a])
                instruction_length = 2

            # MUL
            elif cmd == MUL:
                self.alu(cmd,operand_a,operand_b)
                instruction_length = 3

            else:
                print(f"program failed to run")
                sys.exit(1)
            





