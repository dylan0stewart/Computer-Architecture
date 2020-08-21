"""CPU functionality."""

import sys

program_file = "ls8/examples/mult.ls8"

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 
        self.running = True
        self.flag = [0] * 8

    def load(self, file):
        """
        Load an .ls8 file given the filename passed in as an argument
        """
        # print(f"SYS.ARGV: {sys.argv}")

        # if len(sys.argv) != 2:
        #     print("usage: 02_fileio2.py filename")
        # filename = sys.argv[1]
        address = 0
        try:
            with open(file) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == "":
                        continue

                    x = int(n, 2)
                    print(f"{x:08b}: {x:d}")
                    self.ram[address] = x
                    address += 1

        except:
            print(f"{sys.argv[0]} / {sys.argv[1]} not found")

    def alu(self, op, reg_a, reg_b):
        """Basic Arithmetic and Logic operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            # add CMP for sprint challenge
        # elif op == "CMP":
        #     if reg_a == reg_b:
        #         self.flag[EQ] = 0b00000001
        #     else:
        #         self.flag[EQ] = 0b00000000

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        
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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        ADD  = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        RET = 0b00010001
        CALL = 0b01010000
        #SPRINT ADDITIONS BELOW
        EQ = 0b00000111
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        SP = 7

        while self.running:
            IR = self.ram[self.pc]
            pc_flag = (IR & 0b00010000) >> 4
            #print(f"Bad input: {IR}")
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(operand_a)
            # print(operand_b)

            # check which instruction we're on, and run that instruction, printing the result
            if IR == HLT:
                self.running = False
                self.pc += 1
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                # print(operand_a)
                self.pc += 3   
            elif IR == PRN:
                # print(operand_a)
                self.pc += 2
            
            elif IR == MUL:
                res = self.reg[operand_a] * self.reg[operand_b]
                # print(res)
                self.pc += 3
            elif IR == ADD:
                res = self.reg[operand_a] + self.reg[operand_b]
                # print(res)

            elif IR == PUSH:
                #decrement Stack
                self.reg[7] -= 1
                #grab val from reg
                reg_num = self.ram[self.pc + 1] 
                value = self.reg[reg_num]

                # store on the top of stack
                top_of_stack_addr = self.reg[SP] 
                self.ram[top_of_stack_addr] = value

                self.pc += 2

            elif IR == POP:
                #increment stack
                value = self.ram_read(self.reg[SP])
                self.reg[operation_a] = value
                
                self.reg[SP] +=1
                self.pc +=2


            elif IR == CALL:
                self.reg[SP] -= 1
                stack_addr = self.reg[SP]
                returned_addr = pc + 2
                self.ram_write(stack_addr, returned_addr)
                reg_num = self.ram_read(pc + 1)
                self.pc = self.reg[reg_num]

            elif IR == RET:
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1  


##################################################################################################################
##########################################SPRINT STUFF############################################################
##################################################################################################################

            elif IR == CMP:
                reg_num1 = self.reg[operand_a]
                reg_num2 = self.reg[operand_b]

                if operand_a == operand_b:
                    self.flag[EQ] = 0b00000001
                else:
                    self.flag[EQ] = 0b00000000

            elif IR == JMP:
                self.pc = self.reg[operand_a]

            elif IR == JEQ:
                if self.flag[EQ] == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif IR == JNE:
                if self.flag[EQ] == 0b00000000:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            else:
                pass
            
        
