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
        instructionsIssued = self.decode()
        self.fetch()

        return instructionsIssued

    def fetch(self):
        instrToFetch = self.state.instrBufferSize - len(self.state.instrBuffer)
        '''print "InstrBuffer has " + str(len(self.state.instrBuffer)) + " entries"
        print "There are " + str(self.state.instrBufferSize) + " total spaces"
        print "Need to fetch " + str(instrToFetch)'''
       
        for i in range(instrToFetch):
            instruction = Instruction(self.state.instructions[self.state.programCounter + i])
            instruction.parse()
            #print "Grabbed instruction " + str(instruction)
            self.state.instrBuffer.append(instruction)

        self.state.programCounter += instrToFetch
        return

    def decode(self):
        instructions = list(self.state.instrBuffer)
        toBeIssued = []
        noLoadStore = True

        for i in range(len(instructions)):
            instruction = instructions[i]
            instruction.getReadsWrites()
            instruction.updateWaiting()
        
        self.buildDependencies()

        for i in range(len(instructions)):
            instruction = instructions[i]
            if (sum(instruction.waitingFor.values()) == 0 and 
                instruction.opcode != 0x00 and
                (instruction.opcode | 1 not in [0x23, 0x25, 0x29, 0x2B] or noLoadStore)):

                if instruction.opcode | 1 in [0x23, 0x25, 0x29, 0x2B]:
                    #print "We have our loadStore for this round"
                    noLoadStore = False
                #print "Issuing " + str(instruction)
                toBeIssued.append(instruction)
                instruction.started = True
                self.state.instrBuffer.remove(instruction)
                if instruction.instrType in ["LOAD", "STORE"]:
                    self.setMemRegs(instruction)

            if len(toBeIssued) == self.state.numExecuteUnits:
                break;
                

        numToBeIssued = len(toBeIssued)
        #print "Gonna issue " + str(numToBeIssued)
        for i in range(numToBeIssued, self.state.numExecuteUnits):
            toBeIssued.append(Instruction(np.uint32(0)))
        self.state.pipeline.append(toBeIssued)
        
        return numToBeIssued 

    # For the time being, only do 1 memory access per cycle.
    def memAccess(self):
        for instruction in self.state.pipeline[2]:
            if instruction.instrType == "LOAD":
                self.state.loadDataReg = self.state.memory[self.state.loadAddressReg]
            if instruction.instrType == "STORE":
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
            if instruction.instrType == "ARITH" or instruction.instrType == "LOAD":
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
        
        if instruction.opcode == 0x00:
            return 0
        return 1

    # TODO: Some work is repeated every cycle here that doesn't need to be because we don't explicitly state "I don't depend on X"
    # This function is horrible. I *should* really re-write it from scratch
    def buildDependencies(self):
        instructions = self.state.instrBuffer
        for i in range(len(instructions)):
            secondInstr = instructions[i]
            #print "Considering: " + str(secondInstr)
            #print "Reads from:  " + str(secondInstr.reads)
            #print "Writes to:   " + str(secondInstr.writes)
            for j in range(i):
                firstInstr = instructions[j]
                if firstInstr not in secondInstr.waitingFor:
                    for reg in firstInstr.writes:    #If first instr writes what we read, wait
                        if reg in secondInstr.reads:
                            #print str(secondInstr) + " depends on " + str(firstInstr)
                            if   firstInstr.instrType in ["ARITH", "LOAD"] and secondInstr.instrType in ["ARITH", "BRANCH"]:
                                secondInstr.addWait(firstInstr, 2)      # 1st instr needs to WB before 2nd does EXE
                            elif firstInstr.instrType in ["ARITH", "LOAD"] and secondInstr.instrType in ["LOAD", "STORE"]:
                                secondInstr.addWait(firstInstr, 3)      # 1st instr needs to WB before 2nd does decode
                    for reg in firstInstr.writes:
                        if reg in secondInstr.writes:
                            #print str(secondInstr) + " depends on " + str(firstInstr)
                            secondInstr.addWait(firstInstr, 1)          # 1st instr needs to WB before 2nd does WB
                    
                    # If 1st instruction is branch, we depend on it
                    if  (firstInstr.instrType == "BRANCH") and (firstInstr.opcode != 0xFF):
                        secondInstr.addWait(firstInstr, 2)              # Branch needs to hit exe before we can do anything
                        #print str(secondInstr) + " depends on " + str(firstInstr)

                    # If 1st instruction is a store and second is a load, we depend on it
                    elif (firstInstr.instrType == "STORE") and (secondInstr.instrType in ["LOAD", "STORE"]):
                        secondInstr.addWait(firstInstr, 1)              # 1st instr needs to EXE before second EXE
                        #print str(secondInstr) + " depends on " + str(firstInstr)

                    # If terminate, we need to depend on EVERYTHING
                    elif secondInstr.opcode == 0xFF:
                        if firstInstr.instrType == "BRANCH":
                            secondInstr.addWait(firstInstr, 3)
                        else:
                            secondInstr.addWait(firstInstr, 1)
        return
