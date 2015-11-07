import numpy as np
from state import instructionText

class Instruction():

    def __init__(self, instruction=None):
        self.instruction = instruction
        self.opcode = np.uint8(int(format(int(self.instruction), "032b")[:8], 2))
        self.registers = []
        self.immediate = None

    # TODO: Input/outputs?
    def decode(self):
        self.parse()

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
        string = instructionText[self.opcode] + " "
        for i in self.registers:
            string += hex(i) + " "
        if self.immediate:
            string += hex(self.immediate)
        return string
