import numpy as np
from collections import deque
from functools   import partial
from operator    import *
from copy        import copy

from instruction import Instruction
from state       import State
from executeUnit import ExecuteUnit
from branchUnit  import BranchUnit

class Processor():
    def __init__(self, state):     
        self.state  = state
        self.executeUnits = []
        for i in range(state.numExecuteUnits):
            self.executeUnits.append(ExecuteUnit(state, i))
        #self.executeUnit = ExecuteUnit(state)
        self.branchUnit  = BranchUnit(state)
        return

    def run(self):
        self.writeBack()
        self.execute()
        self.memAccess()
        self.decode()
        self.fetch()

        return

    def fetch(self):
        instrToFetch = self.state.instrBufferSize - len(self.state.instrBuffer)
        
        print "InstrBuffer has " + str(len(self.state.instrBuffer)) + " entries"
        print "There are " + str(self.state.instrBufferSize) + " total spaces"
        print "Need to fetch " + str(instrToFetch)
       
        for i in range(instrToFetch):
            instruction = Instruction(self.state.instructions[self.state.programCounter + i])
            instruction.parse()
            print "Grabbed instruction " + str(instruction)
            self.state.instrBuffer.append(instruction)

        self.state.programCounter += instrToFetch
        return

    def decode(self):
        instructions = list(self.state.instrBuffer)
        toBeIssued = []
        self.buildDependencies()
        noLoadStore = True

        for i in range(len(instructions)):
            instruction = instructions[i]
            instruction.updateWaiting()

        for i in range(min(self.state.numExecuteUnits, len(instructions))):
            instruction = instructions[i]
            if (not instruction.waitingFor) and (instruction.opcode != 0x00) and (instruction.opcode | 1 not in [0x23, 0x25, 0x29, 0x2B] or noLoadStore):
                if instruction.opcode | 1 in [0x23, 0x25, 0x29, 0x2B]:
                    #print "We have our loadStore for this round"
                    noLoadStore = False
                print "Issuing " + str(instruction)
                toBeIssued.append(instruction)
                self.state.instrBuffer.popleft()
                if instruction.instrType in ["LOAD", "STORE"]:
                    self.setMemRegs(instruction)
            else:
                print "Not gonna issue this one: " + str(instruction) + " because: "
                if instruction.waitingFor:
                    print "uncompleted dependencies"
                if instruction.opcode == 0x00:
                    print "It's a NOP"
                if (instruction.opcode | 1 in [0x23, 0x25, 0x29, 0x2B]) and noLoadStore:
                    print "We've already got out load/store for this cycle."
                break;
        

        numToBeIssued = len(toBeIssued)
        for i in range(numToBeIssued, self.state.numExecuteUnits):
            toBeIssued.append(Instruction(np.uint32(0)))
        self.state.pipeline.append(toBeIssued)
        
        return numToBeIssued 

    # For the time being, only do 1 memory access per cycle.
    def memAccess(self):
        for instruction in self.state.pipeline[2]:
            if instruction.opcode >= 0x22 and instruction.opcode <= 0x25:
                self.state.loadDataReg = self.state.memory[self.state.loadAddressReg]
            if instruction.opcode >= 0x28 and instruction.opcode <= 0x2B:
                self.state.storeDataReg = self.state.reg[instruction.registers[0]]
        return

    def execute(self):
        instructions = self.state.pipeline[1]
        for i in range(len(instructions)):
            instruction = instructions[i]
            if instruction.opcode < 0x40 or instruction.opcode == 0xFF:
                self.executeUnits[i].execute(instruction)
            else:
                self.branchUnit.execute(instruction)
        return
        

    def writeBack(self):
        instructions = self.state.pipeline[0]
        for i in range(len(instructions)):
            instruction = instructions[i]
            # Needed to end execution.
            if instruction.opcode == 0xFF:
                self.state.finished = True

            # All arithmetic, Loads, and Move operations.
            if instruction.opcode < 0x28 and instruction.opcode > 0x01: 
                self.state.reg[instruction.registers[0]] = self.state.resultRegs[i]

            instruction.finished = True;
        return

    def setMemRegs(self, instruction):
        if   instruction.opcode == 0x22:    # LD
            self.state.loadAddressReg = self.state.reg[instruction.registers[1]]
        elif instruction.opcode == 0x23:    # LDI
            self.state.loadAddressReg = instruction.immediate
        elif instruction.opcode == 0x24:    # LDA
            self.state.loadAddressReg = self.state.reg[instruction.registers[1]] + self.state.reg[instruction.registers[2]]
        elif instruction.opcode == 0x25:    # LDAI
            self.state.loadAddressReg = self.state.reg[instruction.registers[1]] + instruction.immediate

        elif instruction.opcode == 0x28:    # ST
            self.state.storeAddressReg = self.state.reg[instruction.registers[1]]
        elif instruction.opcode == 0x29:    # STI
            self.state.storeAddressReg = instruction.immediate
        elif instruction.opcode == 0x2A:    # STA
            self.state.storeAddressReg = self.state.reg[instruction.registers[1]] + self.state.reg[instruction.registers[2]]
        elif instruction.opcode == 0x2B:    # STAI
            self.state.storeAddressReg = self.state.reg[instruction.registers[1]] + instruction.immediate
        return

    # TODO: Some work is repeated every cycle here that doesn't need to be.
    def buildDependencies(self):
        instructions = self.state.instrBuffer
        dependencies = []
        for i in range(len(instructions)):

            secondInstr = instructions[i]
            secondDeps = secondInstr.getDependencies()
            dependencies.append(secondInstr.getDependencies())
            for j in range(i):
                firstInstr = instructions[j]
                if firstInstr not in secondInstr.waitingFor:            # This gets redone as we don't say that one instr doesn't depend on another
                    firstDeps = dependencies[j]
                    # If 1st instruction is branch, we depend on it
                    if  (firstInstr.instrType == "BRANCH") and (firstInstr.opcode != 0xFF):
                        secondInstr.waitingFor.append(instructions[j])
                        print str(secondInstr) + " depends on " + str(firstInstr)
                    # If 1st instruction is a store and second is a load, we depend on it
                    elif (firstInstr.instrType == "STORE") and (secondInstr.instrType == "LOAD"): #TODO: This condition doesn't seem right.
                        secondInstr.waitingFor.append(instructions[j])
                        print str(secondInstr) + " depends on " + str(firstInstr)
                    # If 1st instruction writes to a reg the 2nd reads, 2nd depends on 1st
                    else:
                        for reg in firstDeps[1]:
                            if reg in secondDeps[0]:
                                secondInstr.waitingFor.append(instructions[j])
                                print str(secondInstr) + " depends on " + str(firstInstr)


