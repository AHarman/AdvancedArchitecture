from functools import partial
from operator import *
from state import *

def noop(*args):
    return

def arithmetic(operands, immediate, operation=None, imm=False):
    global registers
    if imm:
        registers[operands[0]] = operation(registers[operands[1]], immediate)
    else:
        registers[operands[0]] = operation(registers[operands[1]], registers[operands[2]])
    return

def LD(operands, immediate):
    global registers
    global memory
    registers[operands[0]] = memory[registers[operands[1]]]
    return
def LDI(operands, immediate):
    global registers
    global memory
    registers[operands[0]] = memory[immediate]
    return
def LDA(operands, immediate):
    global registers
    global memory
    registers[operands[0]] = memory[registers[operands[1]] + registers[operands[2]]]
    return
def LDAI(operands, immediate):
    global registers
    global memory
    registers[operands[0]] = memory[registers[operands[1]] + immediate]
    return
def MV(operands, immediate):
    global registers
    global memory
    registers[operands[0]] = memory[registers[operands[1]]]
    return
def MVI(operands, immediate):
    global registers
    registers[operands[0]] = immediate
    return
def ST(operands, immediate):
    global registers
    global memory
    memory[registers[operands[1]]] = registers[operands[0]]
    return
def STI(operands, immediate):
    global registers
    global memory
    memory[immediate] = registers[operands[0]]
    return
def STA(operands, immediate):
    global registers
    global memory
    memory[registers[operands[1]] + registers[operands[2]]] = registers[operands[0]]
    return
def STAI(operands, immediate):
    global registers
    global memory
    memory[registers[operands[1]] + immediate] = registers[operands[0]]
    return

def branch(address):
    global programCounter
    programCounter = address
    return

def branchComp(operands, immediate, operation=None, imm=False):
    global registers
    if operation(registers[operands[0]], registers[operands[1]]):
        if imm:
            address = np.uint32(immediate)
        else:
            address = np.uint32(registers[operands[2]])
        branch(address)
    return

def BR(operands, immediate):
    global registers
    branch(registers[operands[0]])
    return
def BRI(operands, immediate):
    branch(immediate)
    return
def BRZ(operands, immediate):
    global registers
    if registers[operands[0]] == 0:
        branch(operands[1])
    return
def BRZI(operands, immediate):
    global registers
    if registers[operands[0]] == 0:
        branch(immediate)
    return

lookup = {  0x00 : noop,
            0x02 : partial(arithmetic, operation=add),    0x03 : partial(arithmetic, operation=add,    imm=True),   # OP1 = OP2 +  [OP3/IMM]
            0x04 : partial(arithmetic, operation=sub),    0x05 : partial(arithmetic, operation=sub,    imm=True),   # OP1 = OP2 -  [OP3/IMM]
            0x06 : partial(arithmetic, operation=mul),    0x07 : partial(arithmetic, operation=mul,    imm=True),   # OP1 = OP2 *  [OP3/IMM]
            0x08 : partial(arithmetic, operation=and_),   0x09 : partial(arithmetic, operation=and_,   imm=True),   # OP1 = OP2 &  [OP3/IMM]
            0x0A : partial(arithmetic, operation=or_),    0x0B : partial(arithmetic, operation=or_,    imm=True),   # OP1 = OP2 |  [OP3/IMM]
            0x0C : partial(arithmetic, operation=lshift), 0x0D : partial(arithmetic, operation=lshift, imm=True),   # OP1 = OP2 << [OP3/IMM]
            0x0E : partial(arithmetic, operation=rshift), 0x0F : partial(arithmetic, operation=rshift, imm=True),   # OP1 = OP2 >> [OP3/IMM]

            0x22 : LD,  0x23 : LDI,     # OP1 =  MEM([OP2/IMM])
            0x24 : LDA, 0x25 : LDAI,    # OP1 =  MEM(OP2 + [OP3/IMM])
            0x26 : MV,  0x27 : MVI,     # OP1 = [OP2/IMM]
            0x28 : ST,  0x29 : STI,     # MEM([OP2/IMM]) = OP1
            0x2A : STA, 0x2A : STAI,    # MEM(OP2 + [OP3/IMM]) = OP1

            0x42 : BR,                                0x43 : BRI,                                           # Branch to memory address [OP1/IMM]
            0x44 : partial(branchComp, operation=eq), 0x45 : partial(branchComp, operation=eq, imm=True),   # If OP1 == OP2 to address [OP3/IMM]
            0x46 : partial(branchComp, operation=ne), 0x47 : partial(branchComp, operation=ne, imm=True),   # If OP1 != OP2 to address [OP3/IMM]
            0x48 : partial(branchComp, operation=lt), 0x49 : partial(branchComp, operation=lt, imm=True),   # If OP1 <  OP2 to address [OP3/IMM]
            0x4A : partial(branchComp, operation=gt), 0x4B : partial(branchComp, operation=gt, imm=True),   # If OP1 >  OP2 to address [OP3/IMM]
            0x4C : BRZ,                               0x4D : BRZI,                                          # If OP1 == 0   to address [OP2/IMM]

            0xFF : noop}
