"""CPU functionality."""

# opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
SUB = 0b10100001
DIV = 0b10100011
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111

SP = 7 # SP to be R7 

# FLAGS
Less_than = 0
Greater_than = 0
Equal = 0
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        self.ram = [0] * 255 # bytes of memory
        self.reg = [0] * 8 # like variables
        self.halted = False
        self.flags = [0] * 8 # bytes
        

    def ram_read(self,mar):
        # accepts an address = mar and return its value
        return self.ram[mar] 

    def ram_write(self, mar, mdr):
        # takes a value = mdr writes it to the address = mar
        self.ram[mar] = mdr
        

    def load(self, filename):
        """Load a program into memory."""
        # For now, we've just hardcoded a program:
        """
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        """
        try:
            address = 0

            with open(filename) as file: # use open() to open file
                for line in file: # read each line
                    comment_split = line.split('#') # remove comments
                    string_number = comment_split[0].strip() # convert to a number splitting and stripping

                    if string_number == '':
                        continue # ignore blank lines
                    val = int(string_number, 2)
                    # print(string_number)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)
        """
        for instruction in program:
            self.ram[address] = instruction
            address += 1
        """

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
            
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

    def run(self):
        """Run the CPU."""
  
        while not self.halted:
            command = self.ram[self.pc]
            # instruction_length =((command >> 6) & 0b11) + 1 # bitshifted instruction
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
             # set the instruction length here (extract)

            # halt
            if command == HLT:
                self.halted = True
                
            # LDI
            elif command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            # PRN
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2
               
            # MUL
            elif command == MUL:
                self.alu("MUL",operand_a,operand_b)
                self.pc += 3
               
            elif command == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            # PUSH system stack
            elif command == PUSH:
                # setup
                # get a register from the memory
                index_of_the_register = self.ram_read(self.pc + 1)
                # get the value out of the register
                val = self.reg[index_of_the_register]
                
                # do the push
                self.reg[SP] -= 1 # decrementing by 1
                self.ram[self.reg[SP]] = val

            # POP system stack
            elif command == POP:
                # setup
                index_of_the_register = self.ram_read(self.pc + 1)
                val = self.ram[self.reg[SP]]

                # do the pop
                self.reg[index_of_the_register] = val
                self.reg[SP] += 1 # increment by 1
                
            # CALL
            elif command == CALL:
                # push the address of the instruction direction
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                # set the pc to the address at the given register
                index_of_the_register = self.ram[self.pc + 1]
                self.pc = self.reg[index_of_the_register]
            # RET
            elif command == RET:
                # pop the stack on the pc
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1  

            # CMP
            elif command == CMP:
                if self.reg[operand_a] < self.reg[operand_b]:
                    Less_than = 1
                    Greater_than = 0
                    Equal = 0
                    self.flags = 0b00000100
                elif self.reg[operand_a] < self.reg[operand_b]:
                    Less_than = 0
                    Greater_than = 1
                    Equal = 0
                    self.flags = 0b00000010
                elif self.reg[operand_a] < self.reg[operand_b]:
                    Less_than = 0
                    Greater_than = 0
                    Equal = 1
                    self.flags = 0b00000001
                    self.pc += 3


            else:
                print(f"program failed to run", "{0:b}".format(command))
                sys.exit(1)

            # self.pc += instruction_length





