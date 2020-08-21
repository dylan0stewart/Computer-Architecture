"""
I was struggling through to make each day work all week, and finally had it start to click yesterday. 
Was having so many issues trying to use my original CA repo to build on top of, that I decided to 
refactor entirely since there aren't any other pieces to the Sprint, so there is ample time.

One of my TLs showed me how they had structured theirs, and it just made soooo much more sense, so i'm trying that way as well now.

Will try and flesh it back out to all of the week's functions, but as it stands my old repo works for all the week's
assignments, but not for the SC, and this new version only works for SC(currently).
^ update: most working, havent tested all
"""


import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
CMP = 0b10100111
E = 0b00000111
JMP = 0b01010100
JE = 0b01010101
JNE = 0b01010110
MUL = 0b10100010
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000
PUSH = 0b01000101
SP = 0b00000111
ADD = 0b10100000


class CPU: # this part stayed basically exactly the same until we hit the alu function
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.flag = [0] * 8
        # table for the run function to match up with
        self.table = {
            HLT : self.HLT,
            PRN : self.PRN,
            LDI : self.LDI,
            CMP : self.CMP,
            JMP : self.JMP,
            JE : self.JE,
            JNE : self.JNE,
            MUL : self.MUL, # adding the other ir's to the table
            ADD : self.ADD,
            PUSH : self.PUSH,
            POP : self.POP,
            CALL : self.CALL,
            RET : self.RET,

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

####################### HERES WHERE IT CHANGES BIG TIME #################################

    def alu(self, op, operand_a, operand_b):
        # After putting functions in here instead of hardcoding with if IR == xx, 
        # realized I could do the same with every function, and it would be wayyyy cleaner looking
        """ALU operations."""

        if op == "ADD":
            self.reg[operand_a] += self.reg[operand_b]
        elif op == "MUL":
            self.reg[operand_a] *= self.reg[operand_b]
        elif op == "SUB":
            self.reg[operand_a] -= self.reg[operand_b]
        elif op == "CMP":
            if operand_a == operand_b:
                self.flag[E] = 0b00000001 # set 1, basically yes/true
            else:
                self.flag[E] = 0b00000000 # set 0, no/false

        else:
            raise Exception("Unsupported ALU operation")

    def LDI(self, operand_a, operand_b):
        """
        Set the value of a register to an integer.
        """
        self.reg[operand_a] = operand_b
        

    def HLT(self, operand_a, operand_b):
        '''
        Halt the CPU (and exit the emulator)
        '''
        self.running = False
        
    def PRN(self, operand_a, operand_b):
        """
        Print to the console the decimal integer value that 
        is stored in the given register.
        """
        print(self.reg[operand_a])

    def CMP(self, operand_a, operand_b):
        '''
        Compare the values in two registers.
        * If they are Eual, set the Eual `E` flag to 1, otherwise set it to 0.
        * If registerA is less than registerB, set the Less-than `L` flag to 1,
        otherwise set it to 0.
        * If registerA is greater than registerB, set the Greater-than `G` flag
        to 1, otherwise set it to 0.

        Added the ifs and everything to ALU, trying to keep functions as clean as possible.
        '''
        reg_num1 = self.reg[operand_a]
        reg_num2 = self.reg[operand_b]
        self.alu("CMP", reg_num1, reg_num2)

    def JMP(self, operand_a, operand_b):
        '''
        Set the `PC` to the address stored in the given register.
        '''
        self.pc = self.reg[operand_a]

    def JE(self, operand_a, operand_b):
        '''
        If `Equal` flag is set (true), jump to the address stored in the given register.
        '''
        if self.flag[E] == 0b00000001:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def JNE(self, operand_a, operand_b):
        '''
        If `E` flag is clear (false, 0), jump to the address stored in the given
        register.
        '''
        if self.flag[E] == 0b00000000:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

####### adding back originals from throuhgout the week, in new form #######
    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)


    def PUSH(self, operand_a, operand_b):
        #decrement Stack
        self.reg[7] -= 1
        #grab val from reg
        reg_num = self.ram[self.pc + 1] 
        value = self.reg[reg_num]

        # store on the top of stack
        top_of_stack_addr = self.reg[SP] 
        self.ram[top_of_stack_addr] = value

        self.pc += 2

    def POP(self, operand_a, operand_b):
        #increment stack
        value = self.ram_read(self.reg[SP])
        self.reg[operation_a] = value
        
        self.reg[SP] +=1
        self.pc +=2


    def CALL(self, operand_a, operand_b):
        return_addr = operand_b
        self.reg[SP] -= 1
        stack_addr = self.reg[SP]
        returned_addr = pc + 2
        self.ram_write(stack_addr, returned_addr)
        reg_num = self.ram_read(pc + 1)
        self.pc = self.reg[reg_num]

    def RET(self, operand_a, operand_b):
        self.pc = self.ram_read(self.reg[SP])
        self.reg[SP] += 1  


    def run(self):
        '''
        Stole the first few lines from the original. map-out will be;
        find the current instruction, do bitwise op to shift over, 
        re-instantiate operands like in the original, then take the current IR 
        and run it, by using the table above to match things up.
        Lastly, if/when the flag is 0, get my move and make the proper change to counter.
        '''
        while self.running:
            IR = self.ram_read(self.pc) # set current instruction
            pc_flag = (IR & 0b00010000) >> 4 # bitwise op to shift 4 to the right. Instruction + Does change count, doesnt use alu, no operands
            
            # instantiate operands, same as before
            operand_a = self.ram[self.pc +1] 
            operand_b = self.ram[self.pc + 2]

            # take the IR and find its corresponding function using 
            # the table created earlier, and run it on op_a and op_b
            self.table[IR](operand_a, operand_b) 
            if pc_flag == 0: # if flag is 0
                move = int((IR & 0b11000000) >>6) # instantiate move for bitwise op to shift 6 right. (IR + 2 operands, doesnt use ALU, doesnt change count)
                self.pc += move + 1 # move that amount, +1; then  while still running should repeat with new IR