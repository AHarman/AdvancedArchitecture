import sys
import numpy as np
from state import *
from executeFunctions import *

def memToString():
    global memory
    string = "Memory:\n"
    for i in range(10):
        string += str(i) + ": " + format(int(memory[i]), "#02x") + "\n"
    return string

def regToString():
    global registers
    string = "Registers:\n"
    for i in range(len(registers)):
        string += str(i) + ": " + format(int(registers[i]), "#02x") + "\n"
    return string

def loadProgram(filename):
    with open(filename) as f:
        programIn = f.read()
    
    programIn = programIn.split("---\n")
    memoryIn = [x for x in programIn[0].split("\n") if x != ""]
    instructionsIn = [x for x in programIn[1].split("\n") if x != ""]

    for i in range(len(memoryIn)):
        memory[i] = np.uint32(int(memoryIn[i], 2))
    for i in range(len(instructionsIn)):
        instructions[i] = np.uint32(int(instructionsIn[i], 2))


def fetch():
    global programCounter
    programCounter += 1
    return instructions[programCounter - 1]

def decode(instruction):
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

def execute(opcode, operands, immediate):
    lookup[opcode](operands, immediate)
    return

def executeProgram():
    logString = ""

    global programCounter
    opcode = 0
    while opcode != 0xFF:
        currentInstruction = fetch()
        (opcode, operands, immediate) = decode(currentInstruction)
        print (format(int(opcode), "#02X"), operands, format(int(immediate), "#02X"))
        execute(opcode, operands, immediate)

        logString += instructionText[opcode] + "\t" +  str(operands) + "\t\t" + format(int(immediate), "#02X") + "\n"
        logString += memToString() + "\n\n" + regToString() + "\n\n**********\n\n" 
    
    with open("log.out", 'w') as f:
        f.write(logString)
    return

def main():
    loadProgram(sys.argv[1])
    executeProgram()

    print "Number stored in memory address 255: "
    print hex(memory[255])
    return

if __name__ == "__main__":
    main()
