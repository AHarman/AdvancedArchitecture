import sys
import numpy as np
from state import *
from executeUnit import executeUnit

def memToString():
    global memory
    string = "Memory:\n"
    for i in range(10):
        string += str(i) + ": " + format(int(memory[i]), "#02x") + "\n"
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


def executeProgram():
    logString = ""
    unit1 = executeUnit()
    while unit1.finished == False:
        unit1.run() 
        logString += memToString() + "\n\n" + unit1.regToString() + "\n\n**********\n\n" 

    with open("log.out", 'w') as f:
        f.write(unit1.logString)
    return

def main():
    loadProgram(sys.argv[1])
    executeProgram()

    print "Number stored in memory address 255: "
    print hex(memory[255])
    return

if __name__ == "__main__":
    main()
