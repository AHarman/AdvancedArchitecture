import sys
import numpy as np
from state import *
from processor import Processor

def memToString():
    global memory
    string = "Memory:\n"
    for i in range(5):
        string += str(i).rjust(3) + ": " + format(int(memory[i]), "#010x") + "\n"
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
    proc = Processor()
    procFinished = False
    cycleCount = 0
    while not procFinished and cycleCount < 200:
        logString += proc.pipelineToString() + "\n\n"
        logString += proc.specRegToString() + "\n\n"
        logString += memToString() + "\n\n" + proc.regToString() + "\n**********\n"
        cycleCount += 1 
        unit1Finished = proc.run() 

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
