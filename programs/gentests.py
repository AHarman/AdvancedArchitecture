from optparse  import OptionParser

def getOptions():
    parser = OptionParser()
    parser.add_option("-o", "--output",         action="store",     type="string",  dest="output",      default="out.txt",
                        help="Name for output file", metavar="FILE")
    parser.add_option("-r", "--registers",      action="store",     type="int",     dest="numRegs",     default=15,
                        help="How many registers to use. If branching max is 15")
    parser.add_option("-i", "--iterations",     action="store",     type="int",     dest="iterations",  default=100,
                        help="How many instructions per register")
    parser.add_option("-u", "--unroll-all",     action="store_true",                dest="noBranch",    default=False,
                        help="Use no branches")
    parser.add_option("-b", "--branch-freq",    action="store",     type="int",     dest="branchFreq",  default=1,
                        help="How many instructions per register before branching back")
    parser.add_option("-g", "--grouping",       action="store",     type="int",     dest="grouping",    default=1,
                        help="How many instructions that depend on eachother to group")
    
    (options, args) = parser.parse_args()
    return options

def main():
    options = getOptions()
    prog = ""
    for k in range(options.iterations / options.grouping):
        for j in range(options.numRegs):
            instruction = "ADDI R" + format(j, " <2d") + " R" + format(j, " <2d") + " 1"
            for i in range(options.grouping):
                prog += instruction + "\n"



    prog += "TERMINATE\n"
    with open(options.output, 'w') as f:
        f.write(prog)
    return

if __name__ == "__main__":
    main()
