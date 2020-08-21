"""CPU functionality."""
LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
CMP = 0b10100111
EQ = 0b00000111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


"""
I was struggling through to make each day work all week, and finally had it start to click yesterday. 
Was having so many issues trying to use my original CA repo to build on top of, that I decided to 
refactor entirely since there aren't any other pieces to the Sprint, so there is ample time. Will try and flesh it back out to 
all of the week's functions, but as it stands my old repo works for all the week's assignments, but not 
for the SC, and this new version only works for SC(currently).
"""


import sys

class CPU: # this part stayed basically exactly the same until we hit the alu function
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.flag = [0] * 8
        # table for the run function to match
        self.table = {
            HLT : self.HLT,
            PRN : self.PRN,
            LDI : self.LDI,
            CMP : self.CMP,
            JMP : self.JMP,
            JEQ : self.JEQ,
            JNE : self.JNE,

        }
        

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                line = line.split('#')[0].strip()
                if line == '':
                    continue
                try:
                    v = int(line, 2)
                except ValueError:
                    continue
                self.ram_write(address, v)
                address += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def alu(self, op, reg_a, reg_b):
        # After putting functions in here instead of hardcoding with if IR == xx, 
        # realized I could do the same with every function, and it would be wayyyy cleaner looking
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:
                self.flag[EQ] = 0b00000001
            else:
                self.flag[EQ] = 0b00000000

        else:
            raise Exception("Unsupported ALU operation")

    def LDI(self, reg_a, reg_b):
        """
        Set the value of a register to an integer.
        """
        self.reg[reg_a] = reg_b
        

    def HLT(self, reg_a, reg_b):
        '''
        Halt the CPU (and exit the emulator)
        '''
        self.running = False
        
    def PRN(self, reg_a, reg_b):
        """
        Print to the console the decimal integer value that 
        is stored in the given register.
        """
        print(self.reg[reg_a])

    def CMP(self, reg_a, reg_b):
        '''
        Compare the values in two registers.
        * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
        * If registerA is less than registerB, set the Less-than `L` flag to 1,
        otherwise set it to 0.
        * If registerA is greater than registerB, set the Greater-than `G` flag
        to 1, otherwise set it to 0.

        Added the ifs and everything to ALU, trying to keep functions as clean as possible.
        '''
        reg_num1 = self.reg[reg_a]
        reg_num2 = self.reg[reg_b]
        self.alu("CMP", reg_num1, reg_num2)

    def JMP(self, reg_a, reg_b):
        '''
        Set the `PC` to the address stored in the given register.
        '''
        self.pc = self.reg[reg_a]

    def JEQ(self, reg_a, reg_b):
        '''
        If `equal` flag is set (true), jump to the address stored in the given register.
        '''
        if self.flag[EQ] == 0b00000001:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def JNE(self, reg_a, reg_b):
        '''
        If `E` flag is clear (false, 0), jump to the address stored in the given
        register.
        '''
        if self.flag[EQ] == 0b00000000:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def run(self):
        '''
        Stole the first few lines from the original.
        '''
        while self.running:
            IR = self.ram_read(self.pc) # set current instruction
            pc_flag = (IR & 0b00010000) >> 4 # bitwise op to shift 4 to the right. Instruction + Does change count, doesnt use alu, no operands
            operand_a = self.ram[self.pc +1]
            operand_b = self.ram[self.pc + 2]


            # take the IR and find its corresponding function using 
            # the table created earlier, and run it on op_a and op_b
            self.table[IR](operand_a, operand_b) 
            if pc_flag == 0: # if flag is 0
                move = int((IR & 0b11000000) >>6) # instantiate move for bitwise op to shift 6 right. (IR + 2 operands, doesnt use ALU, doesnt change count)
                self.pc += move + 1 # move that amount, +1; then  while still running should repeat with new IR