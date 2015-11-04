from functools import partial
from operator import *
from state import *

class ExecuteUnit():
    def __init__(self):
        self.reg = np.zeros(16, dtype=np.uint32)
        self.programCounter = np.uint32(0)
        self.pipeline = []
        self.finished = False
        self.logString = ""
        
        self.lookup = { 0x00 : self.noop,
                        0x02 : partial(self.arith, operation=add),    0x03 : partial(self.arith, operation=add,    imm=True),
                        0x04 : partial(self.arith, operation=sub),    0x05 : partial(self.arith, operation=sub,    imm=True),
                        0x06 : partial(self.arith, operation=mul),    0x07 : partial(self.arith, operation=mul,    imm=True),
                        0x08 : partial(self.arith, operation=and_),   0x09 : partial(self.arith, operation=and_,   imm=True),
                        0x0A : partial(self.arith, operation=or_),    0x0B : partial(self.arith, operation=or_,    imm=True),
                        0x0C : partial(self.arith, operation=lshift), 0x0D : partial(self.arith, operation=lshift, imm=True),
                        0x0E : partial(self.arith, operation=rshift), 0x0F : partial(self.arith, operation=rshift, imm=True),

                        0x22 : self.LD,  0x23 : self.LDI,
                        0x24 : self.LDA, 0x25 : self.LDAI,
                        0x26 : self.MV,  0x27 : self.MVI,
                        0x28 : self.ST,  0x29 : self.STI,
                        0x2A : self.STA, 0x2A : self.STAI,
    
                        0x42 : self.BR,                                0x43 : self.BRI,
                        0x44 : partial(self.branchComp, operation=eq), 0x45 : partial(self.branchComp, operation=eq, imm=True),
                        0x46 : partial(self.branchComp, operation=ne), 0x47 : partial(self.branchComp, operation=ne, imm=True),
                        0x48 : partial(self.branchComp, operation=lt), 0x49 : partial(self.branchComp, operation=lt, imm=True),
                        0x4A : partial(self.branchComp, operation=gt), 0x4B : partial(self.branchComp, operation=gt, imm=True),
                        0x4C : self.BRZ,                               0x4D : self.BRZI,
    
                        0xFF : self.terminate}
    
    def regToString(self):
        string = "Registers:\n"
        for i in range(len(self.reg)):
            string += str(i) + ": " + format(int(self.reg[i]), "#02x") + "\n"
        return string

    def run(self):
        instruction = self.fetch()
        (opcode, operands, immediate) = self.decode(instruction)
        self.execute(opcode, operands, immediate)
        
        

    def fetch(self):
        self.programCounter += 1
        return instructions[self.programCounter - 1]

    def decode(self, instruction):
        instruction = format(int(instruction), "032b")
        opcode = np.uint8(int(instruction[:8], 2))
        immediate = 0
    
        if opcode == 0x00:                                          # No op
            return 0x00, [], 0
        if opcode == 0xFF:                                          # Terminate
            return 0xFF, [], 0
        if ((opcode > 0x01 and opcode <= 0x0F) or                   # Instructions with 3 registers 
            (opcode | 1 == 0x25) or 
            (opcode | 1 == 0x2B) or 
            (opcode > 0x43 and opcode <= 0x4C)):
            if opcode % 2 == 0:
                operands  = [np.uint8(int(instruction[ 8:12], 2)),
                             np.uint8(int(instruction[12:16], 2)),
                             np.uint8(int(instruction[16:20], 2))]
            else:
                operands  = [np.uint8(int(instruction[ 8:12], 2)),
                             np.uint8(int(instruction[12:16], 2))]
                immediate = np.uint32(int(instruction[16:  ], 2))
        elif (opcode < 0x42 or  opcode | 1 == 0x4D):                # Instructions with 2 registers
            if opcode % 2 == 0:
                operands =  [np.uint8(int(instruction[ 8:12], 2)),
                             np.uint8(int(instruction[12:16], 2))]
            else:
                operands  = [np.uint8(int(instruction[ 8:12], 2))]
                immediate = np.uint32(int(instruction[12:  ], 2))
        elif opcode % 2 == 0:                                       # Instructions with 1 register
            operands  = [np.uint8(int(instruction[ 8:12], 2))]
            immediate = np.uint32(int(instruction[12:  ], 2))
        else:                                                       # Instructions with no registers
            immediate = np.uint32(int(instruction[ 8:  ], 2))
    
        return (opcode, operands, immediate)

    def execute(self, opcode, operands, immediate):
        self.lookup[opcode](operands, immediate)
        return

    def noop(*args):
        return

    def arith(self, operands, immediate, operation=None, imm=False):
        if imm:
            self.reg[operands[0]] = operation(self.reg[operands[1]], immediate)
        else:
            self.reg[operands[0]] = operation(self.reg[operands[1]], self.reg[operands[2]])
        return
    
    def LD(self, operands, immediate):
        global memory
        self.reg[operands[0]] = memory[self.reg[operands[1]]]
        return
    def LDI(self, operands, immediate):
        global memory
        self.reg[operands[0]] = memory[immediate]
        return
    def LDA(self, operands, immediate):
        global memory
        self.reg[operands[0]] = memory[self.reg[operands[1]] + self.reg[operands[2]]]
        return
    def LDAI(self, operands, immediate):
        global memory
        self.reg[operands[0]] = memory[self.reg[operands[1]] + immediate]
        return
    def MV(self, operands, immediate):
        global memory
        self.reg[operands[0]] = memory[self.reg[operands[1]]]
        return
    def MVI(self, operands, immediate):
        self.reg[operands[0]] = immediate
        return
    def ST(self, operands, immediate):
        global memory
        memory[self.reg[operands[1]]] = self.reg[operands[0]]
        return
    def STI(self, operands, immediate):
        global memory
        memory[immediate] = self.reg[operands[0]]
        return
    def STA(self, operands, immediate):
        global memory
        memory[self.reg[operands[1]] + self.reg[operands[2]]] = self.reg[operands[0]]
        return
    def STAI(self, operands, immediate):
        global memory
        memory[self.reg[operands[1]] + immediate] = self.reg[operands[0]]
        return
    
    def branch(self, address):
        self.programCounter = address
        return
    
    def branchComp(self, operands, immediate, operation=None, imm=False):
        if operation(self.reg[operands[0]], self.reg[operands[1]]):
            if imm:
                address = np.uint32(immediate)
            else:
                address = np.uint32(self.reg[operands[2]])
            self.branch(address)
        return
    
    def BR(self, operands, immediate):
        self.branch(self.reg[operands[0]])
        return
    def BRI(self, operands, immediate):
        self.branch(self, immediate)
        return
    def BRZ(self, operands, immediate):
        if self.reg[operands[0]] == 0:
            self.branch(self, self.reg(operands[1]))
        return
    def BRZI(self, operands, immediate):
        if self.reg[operands[0]] == 0:
            self.branch(self, immediate)
        return

    def terminate(self, operands, immediate):
        self.finished = True
        
