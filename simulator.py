import sys
import numpy as np
from optparse  import OptionParser
from state     import State
from processor import Processor
import assembler


def executeProgram(state, debug, interactive, numMemPrint, cycleLimit):
    logString = ""
    proc = Processor(state)
    cycleCount = 0
    instructionCount = 0
    while not state.finished and cycleCount < cycleLimit:
        thisLogString = ""
        if cycleCount > 0:
            if debug:
                thisLogString += state.instrBufferToString()
                thisLogString += state.pipelineToString()       + "\n"
                thisLogString += state.specRegToString()        + "\n"
                thisLogString += state.memToString(numMemPrint) + "\n" 
                thisLogString += state.regToString()            + "\n**********\n"
            if interactive:
                print thisLogString
                raw_input("Press to continue")
        instructionCount += proc.run()
        logString += thisLogString
        cycleCount += 1 
 
    print str(cycleCount) + " cycles run, with a limit of " + str(cycleLimit)
    print str(instructionCount) + " instructions executed (not including NOPs)"
    print str(float(instructionCount)/float(cycleCount)) + " instructions per cycle average"
    logString += "\n\nFinal Memory: " + state.memToString(numMemPrint)
    with open("log.out", 'w') as f:
        f.write(logString)
    return

def getOptions():
    parser = OptionParser()
    parser.add_option("-f", "--fileInput",          action="store",         type="string",  dest="input",
                        help="use as input file", metavar="FILE")
    parser.add_option("-d", "--debug",              action="store_true",                    dest="debug",           default=False,
                        help="Write state each iteration")
    parser.add_option("-i", "--interactive",        action="store_true",                    dest="interactive",     default=False,
                        help="Print the state and pause every cycle")
    parser.add_option("-a", "--assemble",           action="store_true",                    dest="assemble",        default=False,
                        help="assemble program before running")
    parser.add_option("-e", "--executeUnits",       action="store",         type="int",     dest="numExecuteUnits", default=1,
                        help="number of execute units used")
    parser.add_option("-b", "--instructionBuffer",  action="store",         type="int",     dest="instrBuffer",     default=0,
                        help="instruction buffer size. Minimum/default is executeUnits*6")
    parser.add_option("-m", "--memoryPrinting",     action="store",         type="int",     dest="numMemPrint",     default=5,
                        help="How much memory to print in logs/debug")
    parser.add_option("-c", "--cylceLimit",         action="store",         type="int",     dest="cycleLimit",      default=500000,
                        help="An upper limit on cycles")
    (options, args) = parser.parse_args()
    return options
 
def main(): 
    (options, args) = parser.parse_args()
    return options

def main():
    options = getOptions()
    
    state = State(options.numExecuteUnits)
    if options.assemble:
        with open(options.input) as f:
            program = f.read()
        program = assembler.assemble(program)
    else:
        with open(options.input) as f:
            program = f.read()

    state.loadProgram(program)
    executeProgram(state, options.debug, options.interactive, options.numMemPrint, options.cycleLimit)

    return

if __name__ == "__main__":
    main()
