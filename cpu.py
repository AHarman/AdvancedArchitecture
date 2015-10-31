import sys
import numpy as np

memory = np.zeros(1024, dtype=np.int32)
instructions = np.zeros(1024, dtype=np.uint32)
registers = np.zeros(16, dtype=np.int32)
programCounter = np.uint32(0)

def loadProgram(filename):
    with open(filename) as f:
        programIn = f.read()
    
    programIn = programIn.split("---\n")
    memoryIn = [x for x in programIn[0].split("\n") if x != ""]
    instructionsIn = [x for x in programIn[1].split("\n") if x != ""]

    for i in range(len(memoryIn)):
        memory[i] = np.int32(int(memoryIn[i], 2))
    for i in range(len(instructionsIn)):
        instructions[i] = np.int32(int(instructionsIn[i], 2))


def executeProgram():
    return

def main():
    loadProgram(sys.argv[1])
    return

if __name__ == "__main__":
    main()
