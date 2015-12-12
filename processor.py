from collections import deque
from instruction import Instruction
from state       import State
from executeUnit import ExecuteUnit
from functools   import partial
from operator    import *
import numpy as np

class Processor():
   
    def __init__(self, state):     
        self.state  = state
        self.executeUnit = ExecuteUnit(state)

        self.lookup = { 0x42 : self.BR,                         0x43 : self.BR,
                        0x44 : partial(self.branchComp, op=eq), 0x45 : partial(self.branchComp, op=eq),
                        0x46 : partial(self.branchComp, op=ne), 0x47 : partial(self.branchComp, op=ne),
                        0x48 : partial(self.branchComp, op=lt), 0x49 : partial(self.branchComp, op=lt),
                        0x4A : partial(self.branchComp, op=gt), 0x4B : partial(self.branchComp, op=gt),
                        0x4C : self.BR,                         0x4D : self.BRZ}
        return

    def run(self):
        self.writeBack()
        self.execute()
        self.memAccess()
        self.decode()
        self.fetch()

        self.state.programCounter += 1
        #print self.pipelineToString()
        return

    def fetch(self):
        instruction = Instruction(self.state.instructions[self.state.programCounter])
        try:
            self.state.pipeline.append(instruction)
        except e:
            print self.state.pipeline

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
            self.executeUnit.execute(self.state.pipeline[1])
        else:
            self.lookup[instruction.opcode](instruction)
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

    def branch(self, address):
        self.state.programCounter = address
        self.state.pipeline[4] = Instruction(np.int32(0))
        self.state.pipeline[3] = Instruction(np.int32(0))
        self.state.pipeline[2] = Instruction(np.int32(0))
        return
    
    # TODO: Expand, if op=None do BR
    def branchComp(self, instr, op=None):
        if op(self.state.reg[instr.registers[0]], self.state.reg[instr.registers[1]]):
            if instr.immediate != None:
                address = np.uint32(instr.immediate)
            else:
                address = np.uint32(self.state.reg[instr.registers[2]])
            self.branch(address)
        return
    
    def BR(self, instr):
        if instr.immediate != None:
            self.branch(instr.immediate)
        else:
            self.branch(self.state.reg[instr.registers[0]])
        return
    
    def BRZ(self, instr):
        if instr.immediate != None:
            address = instr.immediate
        else:
            address = self.state.reg(instr.registers[1])
        if self.state.reg[instr.registers[0]] == 0:
            self.state.branch(self, address)
        return
