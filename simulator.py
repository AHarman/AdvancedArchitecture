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
    instructionCount = 0
    cycleLimit = 100000
    while not state.finished and cycleCount < cycleLimit:
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
        instructionCount += proc.run()
        logString += thisLogString
        cycleCount += 1
    
 
    print str(cycleCount) + " cycles run, with a limit of " + str(cycleLimit)
    print str(instructionCount) + " instructions executed (not including NOPs)"
    print str(float(instructionCount)/float(cycleCount)) + " instructions per cycle average"
    
    logString += "\n\n\n\nFinal State:\n"
    logString += state.memToString(15)   + "\n"
    logString += state.specRegToString() + "\n"
    logString += state.regToString(16)
    
    with open("log.out", 'w') as f:
        f.write(logString)
    return

def getOptions():
    parser = OptionParser()
    parser.add_option("-i", "--input",              action="store",     type="string",  dest="input",
                        help="use as input file", metavar="FILE")
    parser.add_option("-d", "--debug",              action="store_true",                dest="debug",           default=False,
                        help="print state to stdout")
    parser.add_option("-a", "--assemble",           action="store_true",                dest="assemble",        default=False,
                        help="assemble program before running")
    parser.add_option("-e", "--executeUnits",       action="store",     type="int",     dest="numExecuteUnits", default=1,
                        help="number of execute units used")
    parser.add_option("-b", "--instructionBuffer",  action ="store",    type="int",     dest="instrBuffer",     default=0,
                        help="instruction buffer size. Minimum/default is executeUnits*6")
    (options, args) = parser.parse_args()
    return options

def main():
    options = getOptions()
    
    state = State(options.numExecuteUnits, options.instrBuffer)
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
