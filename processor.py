import numpy as np
from collections import deque
from functools   import partial
from operator    import *

from instruction import Instruction
from state       import State
from executeUnit import ExecuteUnit
from branchUnit  import BranchUnit

class Processor():
    def __init__(self, state):     
        self.state  = state
        self.executeUnit = ExecuteUnit(state)
        self.branchUnit  = BranchUnit(state)
        return

    def run(self):
        self.writeBack()
        self.execute()
        self.memAccess()
        self.decode()
        self.fetch()

        self.state.programCounter += 1
        return

    def fetch(self):
        instruction = Instruction(self.state.instructions[self.state.programCounter])
        self.state.pipeline.append(instruction)

        return

    def decode(self):
        instruction = self.state.pipeline[3]
        instruction.parse()

        if   instruction.opcode == 0x22:
            self.state.loadAddressReg = self.state.reg[instruction.registers[1]]
        elif instruction.opcode == 0x23:
            self.state.loadAddressReg = instruction.immediate
        elif instruction.opcode == 0x24:
            self.state.loadAddressReg = self.state.reg[instruction.registers[1]] + self.state.reg[instruction.registers[2]]
        elif instruction.opcode == 0x25:
            self.state.loadAddressReg = self.state.reg[instruction.registers[1]] + instruction.immediate

        if   instruction.opcode == 0x28:
            self.state.storeAddressReg = self.state.reg[instruction.registers[1]]
        elif instruction.opcode == 0x29:
            self.state.storeAddressReg = instruction.immediate
        elif instruction.opcode == 0x2A:
            self.state.storeAddressReg = self.state.reg[instruction.registers[1]] + self.state.reg[instruction.registers[2]]
        elif instruction.opcode == 0x2B:
            self.state.storeAddressReg = self.state.reg[instruction.registers[1]] + instruction.immediate
        return

    def memAccess(self):
        instruction = self.state.pipeline[2]
        if instruction.opcode >= 0x22 and instruction.opcode <= 0x25:
            self.state.loadDataReg = self.state.memory[self.state.loadAddressReg]
        if instruction.opcode >= 0x28 and instruction.opcode <= 0x2B:
            self.state.storeDataReg = self.state.reg[instruction.registers[0]]
        return

    def execute(self):
        instruction = self.state.pipeline[1]
        if instruction.opcode < 0x40 or instruction.opcode == 0xFF:
            self.executeUnit.execute(instruction)
        else:
            self.branchUnit.execute(instruction)
        return
        

    def writeBack(self):
        instruction = self.state.pipeline[0]
        # Needed to end execution.
        if instruction.opcode == 0xFF:
            self.state.finished = True

        # All arithmetic, Loads, and Move operations.
        if instruction.opcode < 0x28 and instruction.opcode > 0x01: 
            self.state.reg[instruction.registers[0]] = self.state.resultReg
        return

