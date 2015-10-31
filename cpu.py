import sys
import numpy as np

memory = np.zeros(1024, dtype=np.int32)
instructions = np.zeros(1024, dtype=np.uint32)
registers = np.zeros(16, dtype=np.int32)
programCounter = np.uint32(0)

def loadProgram(filename):
    with open(filename) as f:
        programIn = f.read()
    
    programIn = programIn.split("---\n")
    memoryIn = [x for x in programIn[0].split("\n") if x != ""]
    instructionsIn = [x for x in programIn[1].split("\n") if x != ""]

    for i in range(len(memoryIn)):
        memory[i] = np.int32(int(memoryIn[i], 2))
    for i in range(len(instructionsIn)):
        instructions[i] = np.int32(int(instructionsIn[i], 2))


def fetch():
    return instructions[programCounter]

def decode(instruction):
    instruction = format(int(instruction), "032b")
    opcode = np.uint8(int(instruction[:8], 2))
    operands = None
    immediate = None
    
    if opcode == 0x00:                              # No op
        return 0x00, None, None
    if opcode == 0xFF:                              # Terminate
        return 0xFF, None, None

    if ((opcode > 0x01 and opcode <= 0x0F) or 
        (opcode | 1 == 0x25) or 
        (opcode | 1 == 0x2B) or 
        (opcode > 0x43 and opcode <= 0x4C)):
        if opcode % 1 == 0:
            operands  = [np.uint8(int(instruction[ 8:12], 2)),
                         np.uint8(int(instruction[12:16], 2)),
                         np.uint8(int(instruction[16:20], 2))]
        else:
            operands  = [np.uint8(int(instruction[ 8:12], 2)),
                         np.uint8(int(instruction[12:16], 2))]
            immediate = np.uint32(int(instruction[16:  ], 2))
    elif (opcode < 0x42 or
          opcode | 1 == 0x4D):
        if opcode % 1 == 0:
            operands =  [np.uint8(int(instruction[ 8:12], 2)),
                         np.uint8(int(instruction[12:16], 2))]
        else:
            operands  = [np.uint8(int(instruction[ 8:12], 2))]
            immediate = np.uint32(int(instruction[12:  ], 2))
    elif opcode % 2 == 0:                           # Instruction with 1 register
        operands  = [np.uint8(int(instruction[ 8:12], 2))]
        immediate = np.uint32(int(instruction[12:  ], 2))
    else:                                           # Instruction with no registers
        immediate = np.uint32(int(instruction[ 8:  ], 2))
    
    return (opcode, operands, immediate)

def execute(opcode, operands, immediate):
    return

def executeProgram():
    currentInstruction = fetch()
    (opcode, operands, immediate) = decode(currentInstruction)
    print decode(currentInstruction)
    execute(opcode, operands, immediate)
    return

def main():
    loadProgram(sys.argv[1])
    executeProgram()
    return

if __name__ == "__main__":
    main()
