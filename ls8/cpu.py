"""CPU functionality."""

import sys
# Instructions
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8      # registers 
        self.ram = [0] * 256    # ram
        self.pc = 0             # program counter
        self.running = True     # CPU running
        self.branch_table = {}  # modularize code
        self.branch_table[HLT] = self.hlt
        self.branch_table[LDI] = self.ldi
        self.branch_table[PRN] = self.prn
        self.branch_table[MUL] = self.mul

    def ram_read(self, MAR):
        '''take in address and return value'''
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        '''take address and write value'''
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                # remove #, leading and trailing spaces
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
        # arithmetic logic unit 
        # AND clear (set to 0)
        # OR (set to 1)
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

    # Instruction methods
    def hlt(self, operand_a=None, operand_b=None): 
        self.running = False
        self.pc += 1
    def ldi(self, operand_a=None, operand_b=None):
        '''set specified register to a specified value''' 
        self.reg[operand_a] = operand_b
        self.pc += 3
    def prn(self, operand_a=None, operand_b=None): 
        '''read value at specified register'''
        print(self.reg[operand_a])
        self.pc += 2
    def mul(self, operand_a=None, operand_b=None):
        ''' multiply values in two registers and store at registerA.'''
        self.reg[operand_a] *= self.reg[operand_b]
        self.pc += 3

    def run(self):
        """Run the CPU."""
        while self.running == True:
            # first instruction
            IR = self.ram_read(self.pc)
            # next two lines
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR not in self.branch_table:
                print("ERROR")
            
            # call function
            self.branch_table[IR](operand_a, operand_b)     
        
