import numpy as np
from collections import deque
from instruction import Instruction

class State():
    def __init__(self):
        self.memory       = np.zeros(256, dtype=np.uint32)
        self.instructions = np.zeros(256, dtype=np.uint32)
        self.reg          = np.zeros(16, dtype=np.uint32)
        
        # Special regs 
        self.loadDataReg     = np.uint32(0)         # When something comes in from memory, it goes here
        self.loadAddressReg  = np.uint32(0)      # What address in memory we're fetching from
        self.storeDataReg    = np.uint32(0)        # What to store in memory
        self.storeAddressReg = np.uint32(0)     # Where to store it in memory
        self.resultReg       = np.uint32(0)           # Where the result of an operation is held until writeback
        self.programCounter  = np.uint32(0)      # Next instruction to be fetched
        
        self.loadFromMemory  = False             # Whether we need to load from memory
        self.storeToMemory   = False              # Whether we need to store to memory

        self.pipeline = deque([Instruction(np.uint32(0))]*5, 5)
        self.finished = False
        return

    def regToString(self, numRegs=5):
        string = "Registers:\n"
        for i in range(numRegs):
            string += ("R" + str(i) + ":").ljust(5)
            string += format(int(self.reg[i]), "#010x") + "\n"
        return string

    def specRegToString(self):
        string =  "Special Registers:\n"
        string += "Program Counter: " + format(int(self.programCounter),  "#010x") + "\n"
        string += "Result:          " + format(int(self.resultReg),       "#010x") + "\n"
        string += "Load Address:    " + format(int(self.loadAddressReg),  "#010x") + "\n"
        string += "Load Data:       " + format(int(self.loadDataReg),         "#010x") + "\n"
        string += "Store Address:   " + format(int(self.storeAddressReg), "#010x") + "\n"
        string += "Store Data:      " + format(int(self.storeDataReg),        "#010x") + "\n"
        return string
    
    def memToString(self, numAdds=5):
        string = "Memory:\n"
        for i in range(numAdds):
            string += str(i).rjust(3) + ": " + format(int(self.memory[i]), "#010x") + "\n"
        return string

    def pipelineToString(self):
        string =  "FETCH:      "
        string += str(self.pipeline[4]) + "\n"
        string += "DECODE:     "
        string += str(self.pipeline[3]) + "\n"
        string += "MEM ACCESS: "
        string += str(self.pipeline[2]) + "\n"
        string += "EXECUTE:    "
        string += str(self.pipeline[1]) + "\n"
        string += "WRITE BACK: "
        string += str(self.pipeline[0]) + "\n"
        return string

    def loadProgram(self, filename):
        with open(filename) as f:
            programIn = f.read()
    
        programIn = programIn.split("---\n")
        memoryIn = [x for x in programIn[0].split("\n") if x != ""]
        instructionsIn = [x for x in programIn[1].split("\n") if x != ""]

        for i in range(len(memoryIn)):
            self.memory[i] = np.uint32(int(memoryIn[i], 2))
        for i in range(len(instructionsIn)):
            self.instructions[i] = np.uint32(int(instructionsIn[i], 2))
        return
