from functools import partial
from operator import *
from collections import deque
from state import *
from instruction import Instruction

class ExecuteUnit():
    def __init__(self):
        self.reg = np.zeros(16, dtype=np.uint32)
        
        # Special regs
        self.loadReg = np.uint32(0)              # When something comes in from memory, it goes here
        self.loadAddressReg = np.uint32(0)       # What address in memory we're fetching from
        self.storeReg = np.uint32(0)             # What to store in memory
        self.storeAddressReg = np.uint32(0)      # Where to store it in memory
        self.programCounter = np.uint32(0)      # Next instruction to be fetched
        
        self.loadFromMemory = False             # Whether we need to load from memory
        self.storeToMemory = False              # Whether we need to store to memory
        self.pipeline = deque([Instruction(np.uint32(0))]*5, 5)
        self.finished = False
        self.logString = ""
        
        self.lookup = { 0x00 : self.noop,
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
        for i in range(len(self.reg[:5])):
            string += str(i) + ": " + format(int(self.reg[i]), "#010x") + "\n"
        return string
    
    def specRegToString(self):
        string =  "Special Registers:\n"
        string += "Program Counter: " + format(int(self.programCounter),  "#010x") + "\n"
        string += "Load Address:    " + format(int(self.loadAddressReg),  "#010x") + "\n"
        string += "Load Data:       " + format(int(self.loadReg),         "#010x") + "\n"
        string += "Store Address:   " + format(int(self.storeAddressReg), "#010x") + "\n"
        string += "Store Data:      " + format(int(self.storeReg),        "#010x") + "\n"
        return string

    def pipelineToString(self):
        string =  "FETCH:      "
        string += str(self.pipeline[4]) + "\n"
        string += "DECODE:     "
        string += str(self.pipeline[3]) + "\n"
        string += "MEM ACCESS: "
        string += str(self.pipeline[2]) + "\n"
        string += "EXECUTE:    "
        string += str(self.pipeline[1]) + "\n"
        string += "WRITE BACK: "
        string += str(self.pipeline[0]) + "\n"

        if self.pipeline[1].opcode == 0x23:
            print "HERE FFS:"
            print str(self.pipeline[1])
            print self.pipeline[1].registers[0]
            print "Y?"
        return string

    def run(self):
        self.writeBack()
        self.execute()
        self.memAccess()
        self.decode()
        self.fetch()

        self.programCounter += 1
        print self.pipelineToString()

        return self.finished
    
    def fetch(self):
        instruction = Instruction(instructions[self.programCounter])
        self.pipeline.append(instruction)
        return

    def decode(self):
        instruction = self.pipeline[3]
        instruction.parse()
        self.loadFromMemory = True
        if   instruction.opcode == 0x22:
            self.loadAddressReg = self.reg[instruction.registers[1]]
        elif instruction.opcode == 0x23:
            self.loadAddressReg = instruction.immediate
        elif instruction.opcode == 0x24:
            self.loadAddressReg = self.reg[instruction.registers[1]] + self.reg[instruction.registers[2]]
        elif instruction.opcode == 0x25:
            self.loadAddressReg = self.reg[instruction.registers[1]] + instruction.immediate
        else:
            self.loadFromMemory = False
        print "load add reg " + str(self.loadAddressReg)
        return

    def memAccess(self):
        if self.loadFromMemory:
            self.loadReg = memory[self.loadAddressReg]
            print
            print "LOADED " + format(int(self.loadReg), "06x") + " from " + format(int(self.loadAddressReg), "06x")
            print
        return

    def execute(self):
        instruction = self.pipeline[1]
        self.lookup[instruction.opcode](instruction)
        return

    def writeBack(self):
        instruction = self.pipeline[0]
        if instruction.opcode == 0xFF:
            finished = True
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
        self.reg[instr.registers[0]] = self.loadReg
        return

    def MV(self, instr):
        if instr.immediate != None:
            self.reg[instr.registers[0]] = instr.immediate
        else:
            self.reg[instr.registers[0]] = self.reg[instr.registers[1]]
        return

    def ST(self, instr):
        global memory
        if instr.immediate != None:
            memory[instr.immediate] = self.reg[instr.registers[0]]
        else:
            memory[self.reg[instr.registers[1]]] = self.reg[instr.registers[0]]
            print
            print "STORED " + format(int(self.storeReg), "06x") + " into " + format(int(self.storeAddressReg), "06x")
            print
        return
    
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
        self.pipeline[4] = Instruction(np.int32(0))
        self.pipeline[3] = Instruction(np.int32(0))
        self.pipeline[2] = Instruction(np.int32(0))
        return
    
    # TODO: Expand, if op=None do BR
    def branchComp(self, instr, op=None):
        print "Branch check: "
        print format(int(self.reg[instr.registers[0]]), "06x")
        print format(int(self.reg[instr.registers[1]]), "06x")
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
        return
        
