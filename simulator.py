import sys
import numpy as np
from optparse  import OptionParser
from state     import State
from processor import Processor
import assembler


def executeProgram(state, debug):
    logString = ""
    proc = Processor(state)
    cycleCount = 0
    while not state.finished and cycleCount < 300:
        thisLogString  = state.pipelineToString() + "\n\n"
        thisLogString += state.specRegToString()  + "\n\n"
        thisLogString += state.memToString()      + "\n\n" 
        thisLogString += state.regToString()      + "\n**********\n"
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

def getOptions():
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", type="string", dest="input",
                        help="use as input file", metavar="FILE")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                        help="print state to stdout")
    parser.add_option("-a", "--assemble", action="store_true", dest="assemble", default=False,
                        help="assemble program before running")
    parser.add_option("-e", "--executeUnits", action="store", type="int", dest="numExecuteUnits", default=1,
                        help="number of execute units used")
    (options, args) = parser.parse_args()
    return options

def main():
    options = getOptions()
    print options
    
    state = State(options.numExecuteUnits)
    if options.assemble:
        with open(options.input) as f:
            program = f.read()
        program = assembler.assemble(program)
    else:
        with open(options.input) as f:
            program = f.read()

    state.loadProgram(program)
    executeProgram(state, options.debug)

    return

if __name__ == "__main__":
    main()
