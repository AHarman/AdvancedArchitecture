import sys
import numpy as np
from state import *
from executeUnit import ExecuteUnit

def memToString():
    global memory
    string = "Memory:\n"
    for i in range(5):
        string += str(i) + ": " + format(int(memory[i]), "#010x") + "\n"
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
    unit1 = ExecuteUnit()
    unit1Finished = False
    cycleCount = 0
    while not unit1Finished and cycleCount < 200:
        logString += unit1.pipelineToString() + "\n\n"
        logString += unit1.specRegToString() + "\n\n"
        logString += memToString() + "\n\n" + unit1.regToString() + "\n**********\n"
        cycleCount += 1 
        unit1Finished = unit1.run() 

    print str(cycleCount) + " cycles"
    with open("log.out", 'w') as f:
        f.write(logString)
    return

def main():
    loadProgram(sys.argv[1])
    executeProgram()

    print "Number stored in memory address 255: "
    print format(int(memory[255]), "#010x")
    return

if __name__ == "__main__":
    main()
