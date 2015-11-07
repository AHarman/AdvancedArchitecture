from functools import partial
from operator import *
from collections import deque
from state import *
from instruction import Instruction

class ExecuteUnit():
    def __init__(self):
        self.reg = np.zeros(16, dtype=np.uint32)
        self.loadReg = np.int32(0)
        self.storeReg = np.int32(0)
        self.programCounter = np.uint32(0)
        self.pipeline = deque([Instruction(np.int32(0))]*5, 5)
        self.finished = False
        self.logString = ""
        print instructions
        
        self.lookup = { 0x00 : self.noop,
                        0x02 : partial(self.arith, op=add),    0x03 : partial(self.arith, op=add),
                        0x04 : partial(self.arith, op=sub),    0x05 : partial(self.arith, op=sub),
                        0x06 : partial(self.arith, op=mul),    0x07 : partial(self.arith, op=mul),
                        0x08 : partial(self.arith, op=and_),   0x09 : partial(self.arith, op=and_),
                        0x0A : partial(self.arith, op=or_),    0x0B : partial(self.arith, op=or_),
                        0x0C : partial(self.arith, op=lshift), 0x0D : partial(self.arith, op=lshift),
                        0x0E : partial(self.arith, op=rshift), 0x0F : partial(self.arith, op=rshift),

                        0x22 : self.LD,  0x23 : self.LD,
                        0x24 : self.LDA, 0x25 : self.LDA,
                        0x26 : self.MV,  0x27 : self.MV,
                        0x28 : self.ST,  0x29 : self.ST,
                        0x2A : self.STA, 0x2A : self.STA,
    
                        0x42 : self.BR,                         0x43 : self.BR,
                        0x44 : partial(self.branchComp, op=eq), 0x45 : partial(self.branchComp, op=eq),
                        0x46 : partial(self.branchComp, op=ne), 0x47 : partial(self.branchComp, op=ne),
                        0x48 : partial(self.branchComp, op=lt), 0x49 : partial(self.branchComp, op=lt),
                        0x4A : partial(self.branchComp, op=gt), 0x4B : partial(self.branchComp, op=gt),
                        0x4C : self.BR,                         0x4D : self.BRZ,
    
                        0xFF : self.terminate}
    
    def regToString(self):
        string = "Registers:\n"
        for i in range(len(self.reg)):
            string += str(i) + ": " + format(int(self.reg[i]), "#02x") + "\n"
        return string

    def pipelineToString(self):
        string = ""
        for instruction in self.pipeline:
            string += str(instruction) + "\n"
        return string

    def run(self):
        print self.pipelineToString()
        self.fetch()
        self.decode()
        self.memAccess()
        self.execute()
        self.writeBack()

        self.programCounter += 1
    
    def progressQueue(self):
        return

    def fetch(self):
        instruction = Instruction(instructions[self.programCounter])
        self.pipeline.append(instruction)
        return

    def decode(self):
        self.pipeline[3].decode()
        return

    def memAccess(self):
        return

    def execute(self):
        instruction = self.pipeline[1]
        self.lookup[instruction.opcode](instruction)
        return

    def writeBack(self):
        return

    def noop(*args):
        return

    def arith(self, instr, op=None):
        if instr.immediate != None:
            self.reg[instr.registers[0]] = op(self.reg[instr.registers[1]], instr.immediate)
        else:
            self.reg[instr.registers[0]] = op(self.reg[instr.registers[1]], self.reg[instr.registers[2]])
        return
    
    def LD(self, instr):
        global memory
        if instr.immediate != None:
            self.reg[instr.registers[0]] = memory[instr.immediate]
        else:
            self.reg[instr.registers[0]] = memory[self.reg[instr.registers[1]]]
        return

    def LDA(self, instr):
        global memory
        if instr.immediate != None:
            self.reg[instr.registers[0]] = memory[self.reg[instr.registers[1]] + instr.immediate]
        else:
            self.reg[instr.registers[0]] = memory[self.reg[instr.registers[1]] + self.reg[instr.registers[2]]]
        return

    def MV(self, instr):
        global memory
        if instr.immediate != None:
            self.reg[instr.registers[0]] = instr.immediate
        else:
            self.reg[instr.registers[0]] = memory[self.reg[instr.registers[1]]]
        return
    
    def ST(self, instr):
        global memory
        if instr.immediate != None:
            memory[instr.immediate] = self.reg[instr.registers[0]]
        else:
            memory[self.reg[instr.registers[1]]] = self.reg[instr.registers[0]]
    
    def STA(self, instr):
        global memory
        if instr.immediate != None:
            memory[self.reg[instr.registers[1]] + instr.immediate] = self.reg[instr.registers[0]]
        else:
            memory[self.reg[instr.registers[1]] + self.reg[instr.registers[2]]] = self.reg[instr.registers[0]]
        return
    
    # TODO: Clear pipeline
    def branch(self, address):
        self.programCounter = address
        return
    
    # TODO: Expand, if op=None do BR
    def branchComp(self, instr, op=None):
        if op(self.reg[instr.registers[0]], self.reg[instr.registers[1]]):
            if instr.immediate != None:
                address = np.uint32(instr.immediate)
            else:
                address = np.uint32(self.reg[instr.registers[2]])
            self.branch(address)
        return
    
    def BR(self, instr):
        if instr.immediate != None:
            self.branch(self, instr.immediate)
        else:
            self.branch(self.reg[instr.registers[0]])
        return
    
    def BRZ(self, instr):
        if instr.immediate != None:
            address = instr.immediate
        else:
            address = self.reg(instr.registers[1])
        if self.reg[instr.registers[0]] == 0:
            self.branch(self, address)
        return

    def terminate(self, instr):
        self.finished = True
        return
        
