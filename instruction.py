import numpy as np

# Used for debugging
instructionText = {
    0x00 : "NOP", 0x01 : "MEM",
    0x02 : "ADD", 0x03 : "ADDI",
    0x04 : "SUB", 0x05 : "SUBI",
    0x06 : "MUL", 0x07 : "MULI",
    0x08 : "AND", 0x09 : "ANDI",
    0x0A : "OR",  0x0B : "ORI",
    0x0C : "LS",  0x0D : "LSI",
    0x0E : "RS",  0x0F : "RSI",
    0x22 : "LD",  0x23 : "LDI",
    0x24 : "LDA", 0x25 : "LDAI",
    0x26 : "MV",  0x27 : "MVI",
    0x28 : "ST",  0x29 : "STI",
    0x2A : "STA", 0x2B : "STAI",
    0x42 : "BR",  0x43 : "BRI",
    0x44 : "BRE", 0x45 : "BREI",
    0x46 : "BRN", 0x47 : "BRNI",
    0x48 : "BRL", 0x49 : "BRLI",
    0x4A : "BRG", 0x4B : "BRGI",
    0x4C : "BRZ", 0x4D : "BRZI",
    0xFF : "TRM"}

class Instruction():

    def __init__(self, instruction=None):
        self.instruction = instruction
        self.opcode = np.uint8(int(format(int(self.instruction), "032b")[:8], 2))
        self.registers = []
        self.immediate = None
        self.numRegs = None
        self.finished = False       # Has instruction finished executing
        self.waitingFor = []        # Any instructions that must be completed before this one is
        self.instrType = None       # Can be LOAD, STORE, ARITH, BRANCH. MV counts as arith

    def parse(self):
        instructionString = format(int(self.instruction), "032b")

        if self.opcode == 0x00 or self.opcode == 0xFF:      # NOP, TRM
            self.numRegs = 0
            return
        if self.opcode | 1 == 0x43:                         # BR, BRI
            self.numRegs = 1
        elif self.opcode | 1 in [0x23, 0x27, 0x29, 0x4D]:   # LD, LDI, MV, MVI, ST, STI
            self.numRegs = 2
        else:
            self.numRegs = 3

        if self.opcode % 2 == 1:
            self.numRegs -= 1
            self.immediate = np.int32(int(instructionString[8 + 4 * self.numRegs:], 2))

        for i in range(self.numRegs):
            self.registers.append(np.uint8(int(instructionString[i*4 + 8: i*4 + 12], 2)))
        if self.immediate != None:
            self.immediate = np.int32(int(instructionString[self.numRegs*4 + 8:], 2))
        
        if self.opcode < 0x20 or self.opcode | 1 == 0x27:
            self.instrType = "ARITH"
        elif self.opcode < 0x26:
            self.instrType = "LOAD"
        elif self.opcode < 0x40:
            self.instrType = "STORE"
        else:
            self.instrType = "BRANCH"

    def getDependencies(self):
        reads = []
        writes = []
        if self.opcode in [0x00, 0xFF, 0x43]:    # NOP, TRM, BRI
            return [[], []]
        elif self.opcode < 0x20:            # Arithmetic instructions
            writes.append("R" + str(self.registers[0]))
            for i in range(1, self.numRegs):
                reads.append("R" + str(self.registers[i]))
        elif self.opcode < 0x28:            # LD*, MV*
            writes.append("R" + str(self.registers[0]))
            for i in range(1, self.numRegs):
                reads.append("R" + str(self.registers[i]))
        elif self.opcode < 0x40:            # ST*
            for i in range(self.numRegs):
                reads.append("R" + str(self.registers[i]))
        else:                               # Branch
            for i in range(self.numRegs):
                reads.append("R" + str(self.registers[i]))
        return [reads, writes]
    
    def updateWaiting(self):
        self.waitingFor = [x for x in self.waitingFor if not x.finished]

    def __str__(self):
        string = instructionText[self.opcode].ljust(4) + " "
        for i in self.registers:
            string += ("R" + str(i)).ljust(4)
        if self.immediate != None:
            string += hex(self.immediate)
        return string

