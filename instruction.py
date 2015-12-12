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

    def parse(self):
        instructionString = format(int(self.instruction), "032b")

        if self.opcode == 0x00 or self.opcode == 0xFF:
            return
        if self.opcode | 1 == 0x43:
            numRegs = 1
        elif self.opcode | 1 in [0x23, 0x27, 0x29, 0x4D]:
            numRegs = 2
        else:
            numRegs = 3

        if self.opcode % 2 == 1:
            numRegs -= 1
            self.immediate = np.int32(int(instructionString[8 + 4 * numRegs:], 2))

        for i in range(numRegs):
            self.registers.append(np.uint8(int(instructionString[i*4 + 8: i*4 + 12], 2)))
        if self.immediate != None:
            self.immediate = np.int32(int(instructionString[numRegs*4 + 8:], 2))

    def __str__(self):
        string = instructionText[self.opcode].ljust(4) + " "
        for i in self.registers:
            string += ("R" + str(i)).ljust(4)
        if self.immediate != None:
            string += hex(self.immediate)
        return string

