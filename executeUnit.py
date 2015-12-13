import numpy as np
from instruction import Instruction
from state       import State
from functools   import partial
from operator    import *

class ExecuteUnit():
    def __init__(self, state, index):
        self.state = state
        self.index = index      # Need to know which one we are

        self.lookup = { 0x00 : self.NOP,
                        0x02 : partial(self.arith, op=add),    0x03 : partial(self.arith, op=add),
                        0x04 : partial(self.arith, op=sub),    0x05 : partial(self.arith, op=sub),
                        0x06 : partial(self.arith, op=mul),    0x07 : partial(self.arith, op=mul),
                        0x08 : partial(self.arith, op=and_),   0x09 : partial(self.arith, op=and_),
                        0x0A : partial(self.arith, op=or_),    0x0B : partial(self.arith, op=or_),
                        0x0C : partial(self.arith, op=lshift), 0x0D : partial(self.arith, op=lshift),
                        0x0E : partial(self.arith, op=rshift), 0x0F : partial(self.arith, op=rshift),

                        0x22 : self.LD,  0x23 : self.LD,
                        0x24 : self.LD,  0x25 : self.LD,
                        0x26 : self.MV,  0x27 : self.MV,
                        0x28 : self.ST,  0x29 : self.ST,
                        0x2A : self.ST,  0x2B : self.ST,
    
                        0x42 : self.NOP, 0x43 : self.NOP,
                        0x44 : self.NOP, 0x45 : self.NOP,
                        0x46 : self.NOP, 0x47 : self.NOP,
                        0x48 : self.NOP, 0x49 : self.NOP,
                        0x4A : self.NOP, 0x4B : self.NOP,
                        0x4C : self.NOP, 0x4D : self.NOP,
    
                        0xFF : self.NOP}
        return

    def execute(self, instruction):
        self.lookup[instruction.opcode](instruction)
        return

    def arith(self, instr, op=None):
        if instr.immediate != None:
            self.state.resultRegs[self.index] = op(self.state.reg[instr.registers[1]], instr.immediate)
        else:
            self.state.resultRegs[self.index] = op(self.state.reg[instr.registers[1]], self.state.reg[instr.registers[2]])
        return
        
    def NOP(*args):
        return
    
    def LD(self, instr):
        self.state.resultRegs[self.index] = self.state.loadDataReg
        return
    
    def ST(self, instr):
        self.state.memory[self.state.storeAddressReg] = self.state.storeDataReg
        return

    def MV(self, instr):
        if instr.immediate != None:
            self.state.resultRegs[self.index] = instr.immediate
        else:
            self.state.resultRegs[self.index] = self.state.reg[instr.registers[1]]
        return
