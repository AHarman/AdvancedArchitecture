import numpy as np
from instruction import Instruction
from state       import State
from functools   import partial
from operator    import *
from collections import deque

class BranchUnit():
    def __init__(self, state):
        self.state = state
        self.lookup = { 0x42 : self.BR,                         0x43 : self.BR,
                        0x44 : partial(self.branchComp, op=eq), 0x45 : partial(self.branchComp, op=eq),
                        0x46 : partial(self.branchComp, op=ne), 0x47 : partial(self.branchComp, op=ne),
                        0x48 : partial(self.branchComp, op=lt), 0x49 : partial(self.branchComp, op=lt),
                        0x4A : partial(self.branchComp, op=gt), 0x4B : partial(self.branchComp, op=gt),
                        0x4C : self.BR,                         0x4D : self.BRZ}
        return

    def execute(self, instruction):
        self.lookup[instruction.opcode](instruction)
        return

    def branch(self, address):
        self.state.programCounter = address
        self.state.pipeline[2] = [Instruction(np.uint32(0)), Instruction(np.uint32(0))]
        self.state.instrBuffer  = deque([], self.state.instrBufferSize)
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
