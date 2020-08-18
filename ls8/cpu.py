"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # 8 registers 
        self.ram = [0] * 256 # ram
        self.pc = 0
        self.running = True

    # Memory address register
    def ram_read(self, MAR):
        '''
        take in address and return value
        '''
        MDR = self.ram[MAR]
        return MDR

    # Memory data register
    def ram_write(self, MAR, MDR):
        '''
        take address and write value
        '''
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        # #program counter
        # address = 0
        # # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        # Load a program
        # program counter
        address = 0
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                # take out comment
                # remove leading and trailing spaces
                line = line.split("#")[0].strip()
                # skip empty lines
                if line == "":
                    continue
                # store in memory
                else:
                    # base 2 (binary)
                    self.ram[address] = int(line, 2)
                    address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        # Instructions
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while self.running == True:
            # first instruction
            IR = self.ram_read(self.pc)
            # next two lines
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                # sets a specified register to a specified value
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:
                # read
                print(self.reg[operand_a])
                self.pc += 2
            
            elif IR == HLT:
                self.running = False
                self.pc += 1
            
            elif IR == MUL:
                # multiply the values in two registers together 
                # and store the result in registerA.
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            
        
# cpu = CPU()

# cpu.load() 
# #cpu.run()
#print("ARG 1", sys.argv[0])
#print("ARG 2", sys.argv[1]) # file to loadexcept NameError:

