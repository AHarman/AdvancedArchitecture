import numpy as np
class State():
    def __init__(self):
        self.memory = np.zeros(256, dtype=np.uint32)
        self.instructions = np.zeros(256, dtype=np.uint32)
        self.registers = np.zeros(16, dtype=np.uint32)

    def regToString(self):
        string = "Registers:\n"
        for i in range(len(self.registers[:5])):
            string += ("R" + str(i) + ":").ljust(5)
            string += format(int(self.registers[i]), "#010x") + "\n"
        return string

    def memToString(self):
        string = "Memory:\n"
        for i in range(5):
            string += str(i).rjust(3) + ": " + format(int(self.memory[i]), "#010x") + "\n"
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
