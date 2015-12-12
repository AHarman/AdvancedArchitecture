import sys
import numpy as np
from state import State
from processor import Processor

def executeProgram(state):
    logString = ""
    proc = Processor(state)
    procFinished = False
    cycleCount = 0
    while not procFinished and cycleCount < 200:
        logString += proc.pipelineToString() + "\n\n"
        logString += proc.specRegToString() + "\n\n"
        logString += state.memToString() + "\n\n" + state.regToString() + "\n**********\n"
        cycleCount += 1 
        unit1Finished = proc.run() 

    print str(cycleCount) + " cycles"
    with open("log.out", 'w') as f:
        f.write(logString)
    return

def main():
    state = State()
    state.loadProgram(sys.argv[1])
    executeProgram(state)

    print "Number stored in memory address 255: "
    print format(int(state.memory[255]), "#010x")
    return

if __name__ == "__main__":
    main()
