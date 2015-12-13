import sys
import numpy as np
from state import State
from processor import Processor

debug = True

def executeProgram(state):
    global debug
    logString = ""
    proc = Processor(state)
    cycleCount = 0
    while not state.finished and cycleCount < 300:
        thisLogString = ""
        if cycleCount > 0:
            thisLogString += state.instrBufferToString()
            thisLogString += state.pipelineToString()    + "\n"
            thisLogString += state.specRegToString()     + "\n"
            thisLogString += state.memToString()         + "\n" 
            thisLogString += state.regToString()         + "\n**********\n"
            if debug:
                print thisLogString
                raw_input("Press to continue")
        proc.run()
        logString += thisLogString
        cycleCount += 1 
 
    print str(cycleCount) + " cycles run, with a limit of 300"
    logString += "\n\n\n\nFinal Memory: " + state.memToString(15)
    with open("log.out", 'w') as f:
        f.write(logString)
    return

def main():
    state = State()
    state.loadProgram(sys.argv[1])
    executeProgram(state)

    return

if __name__ == "__main__":
    main()
