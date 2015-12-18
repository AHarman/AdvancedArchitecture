import numpy as np
from collections import deque
from instruction import Instruction

class State():
    def __init__(self, numExecuteUnits):
        self.numExecuteUnits = numExecuteUnits
        self.instrBufferSize = max(5,  numExecuteUnits * 5);
        
        self.memory       = np.zeros( 256, dtype=np.uint32)
        self.instructions = np.zeros(4096, dtype=np.uint32)
        self.reg          = np.zeros( 16, dtype=np.uint32)
        self.instrBuffer  = deque([], self.instrBufferSize)
        self.pipeline     = deque([[], [], []], 3)  # Only used for Mem access, execute and writeback now.
        for i in range(len(self.pipeline)):
            self.pipeline[i] = []
            for j in range(numExecuteUnits):
                self.pipeline[i].append(Instruction(np.uint32(0)))
        
        # Special regs 
        self.loadDataReg     = np.uint32(0)                                     # When something comes in from memory, it goes here
        self.loadAddressReg  = np.uint32(0)                                     # What address in memory we're fetching from
        self.storeDataReg    = np.uint32(0)                                     # What to store in memory
        self.storeAddressReg = np.uint32(0)                                     # Where to store it in memory
        self.resultRegs      = np.zeros(self.numExecuteUnits, dtype=np.uint32)  # Where the result of an operation is held until writeback
        self.programCounter  = np.uint32(0)                                     # Next instruction to be fetched
        
        self.loadFromMemory  = False            # Whether we need to load from memory
        self.storeToMemory   = False            # Whether we need to store to memory

        self.finished = False
        return

    def instrBufferToString(self):
        string = "INSTR BUF:  " + str(self.instrBuffer[0]) + "\n"
        for instruction in list(self.instrBuffer)[1:]: 
            if instruction.opcode != 0x00:
                string += "            " + str(instruction) + "\n"
        return string

    def regToString(self, numRegs=5):
        string = "Registers:\n"
        for i in range(numRegs):
            string += ("R" + str(i) + ":").ljust(5)
            string += format(int(self.reg[i]), "#010x") + "\n"
        return string

    def specRegToString(self):
        string =  "Special Registers:\n"
        string += "Program Counter: " + format(int(self.programCounter),  "#010x") + "\n"
        string += "Result regs:     " + format(int(self.resultRegs[0]),    "#010x") + "\n"
        for i in range(1, self.numExecuteUnits):
            string += "                 " + format(int(self.resultRegs[i]),    "#010x") + "\n"
        string += "Load Address:    " + format(int(self.loadAddressReg),  "#010x") + "\n"
        string += "Load Data:       " + format(int(self.loadDataReg),     "#010x") + "\n"
        string += "Store Address:   " + format(int(self.storeAddressReg), "#010x") + "\n"
        string += "Store Data:      " + format(int(self.storeDataReg),    "#010x") + "\n"
        return string
    
    def memToString(self, numAdds=5):
        string = "Memory:\n"
        for i in range(numAdds):
            string += str(i).rjust(3) + ": " + format(int(self.memory[i]), "#010x") + "\n"
        return string

    def pipelineToString(self):
        #string =  "FETCH:      " + str(self.pipeline[4][0]) + "\n"
        #for instruction in self.pipeline[4][1:]:
        #    string += "            " + str(instruction) + "\n"
        
        #string += "DECODE:     " + str(self.pipeline[3][0]) + "\n"
        #for instruction in self.pipeline[3][1:]:
        #    string += "            " + str(instruction) + "\n"
        
        string  = "MEM ACCESS: " + str(self.pipeline[2][0]) + "\n"
        for instruction in self.pipeline[2][1:]:
            if instruction.opcode != 0x00:
                string += "            " + str(instruction) + "\n"
        
        string += "EXECUTE:    " + str(self.pipeline[1][0]) + "\n"
        for instruction in self.pipeline[1][1:]:
            if instruction.opcode != 0x00:
                string += "            " + str(instruction) + "\n"
        
        string += "WRITE BACK: " + str(self.pipeline[0][0]) + "\n"
        for instruction in self.pipeline[0][1:]:
            if instruction.opcode != 0x00:
                string += "            " + str(instruction) + "\n"
        return string

    def loadProgram(self, programIn):
    
        programIn = programIn.split("---\n")
        memoryIn = [x for x in programIn[0].split("\n") if x != ""]
        instructionsIn = [x for x in programIn[1].split("\n") if x != ""]

        for i in range(len(memoryIn)):
            self.memory[i] = np.uint32(int(memoryIn[i], 2))
        for i in range(len(instructionsIn)):
            self.instructions[i] = np.uint32(int(instructionsIn[i], 2))
        return
