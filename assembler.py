import sys
import re

instructionSet = {  "NOP"  : 0b00000000,                        # No operation
                                         "MEM"  : 0b00000001,   # Used by assembler for laying out data memory.

                    # Arithmetic and logic
                    "ADD"  : 0b00000010, "ADDI" : 0b00000011,   # OP1 = OP2 +  [OP3/IMM]
                    "SUB"  : 0b00000100, "SUBI" : 0b00000101,   # OP1 = OP2 -  [OP3/IMM]
                    "MUL"  : 0b00000110, "MULI" : 0b00000111,   # OP1 = OP2 *  [OP3/IMM]
                    "AND"  : 0b00001000, "ANDI" : 0b00001001,   # OP1 = OP2 &  [OP3/IMM]
                    "OR"   : 0b00001010, "ORI"  : 0b00001011,   # OP1 = OP2 |  [OP3/IMM]
                    "LS"   : 0b00001100, "LSI"  : 0b00001101,   # OP1 = OP2 << [OP3/IMM]
                    "RS"   : 0b00001110, "RSI"  : 0b00001111,   # OP1 = OP2 >> [OP3/IMM]

                    # Memory operations
                    "LD"   : 0b00100010, "LDI"  : 0b00100011,   # OP1 =  MEM([OP2/IMM])
                    "LDA"  : 0b00100100, "LDAI" : 0b00100101,   # OP1 =  MEM(OP2 + [OP3/IMM])
                    "MV"   : 0b00100110, "MVI"  : 0b00100111,   # OP1 = [OP2/IMM]
                    "ST"   : 0b00101000, "STI"  : 0b00101001,   # MEM([OP2/IMM]) = OP1
                    "STA"  : 0b00101010, "STAI" : 0b00101011,   # MEM(OP2 + [OP3/IMM]) = OP1

                    # Control flow
                    "BR"   : 0b01000010, "BRI"  : 0b01000011,   # Branch to memory address [OP1/IMM]
                    "BRE"  : 0b01000100, "BREI" : 0b01000101,   # Branch if OP1 == OP2 to memory address [OP3/IMM]
                    "BRN"  : 0b01000110, "BRNI" : 0b01000111,   # Branch if OP1 != OP2 to memory address [OP3/IMM]
                    "BRL"  : 0b01001000, "BRLI" : 0b01001001,   # Branch if OP1 <  OP2 to memory address [OP3/IMM]
                    "BRG"  : 0b01001010, "BRGI" : 0b01001011,   # Branch if OP1 >  OP2 to memory address [OP3/IMM]
                    "BRZ"  : 0b01001100, "BRZI" : 0b01001101,   # Branch if OP1 == 0   to memory address [OP2/IMM]

                    # Terminate program
                    "TERMINATE" : 0b11111111}                   # Terminates program

def findLabels(assembly):
    labels = {}

    for i in range(len(assembly)):
        instruction = assembly[i]
        if re.search(r'^"\w+"$', instruction[-1]) != None:
            labels[instruction[-1][1:-1]] = str(i)
            assembly[i] = instruction[:-1]
    return labels


def replaceLabels(assembly, labels):
    for i in range(len(assembly)):
        instruction = assembly[i]
        for j in range(len(instruction)):
            if re.search(r">.+", instruction[j]) != None:
                label = instruction[j][1:]
                assembly[i][j] = labels[label]
    return assembly

def segregateMemory(assembly):
    data = {}
    instructions = []
    for instruction in assembly:
        if instruction[0] == "MEM":
            data[int(instruction[1], 0)] = format(int(instruction[2], 0), "032b")
        else:
            instructions.append(instruction)

    return (data, instructions)

def removeComments(assembly):
    newAssembly = []
    for line in assembly:
        commentFound = False
        newLine = []
        for word in line:
            if word[0:2] == "//":
                commentFound = True
            if commentFound == False:
                newLine.append(word)
        if newLine:
            newAssembly.append(newLine)
    return newAssembly
    

def preprocessor(assembly):
    assembly = removeComments(assembly)
    (memory, assembly) = segregateMemory(assembly)
    labels = findLabels(assembly)
    assembly = replaceLabels(assembly, labels)

    return (memory, assembly)

def assembleArithmetic(instruction):
    opcode = instructionSet[instruction[0]]
    machineCode  = (format(opcode, "08b"))
    machineCode += format(int(instruction[1][1:]), "04b")
    machineCode += format(int(instruction[2][1:]), "04b")
    if opcode % 2 == 0:
        machineCode += format(int(instruction[3][1:]), "04b")
        machineCode += format(0, "012b")
    else:
        machineCode += format(int(instruction[3], 0), "016b")
    return machineCode

def assembleMemory(instruction):
    opcode = instructionSet[instruction[0]]
    machineCode  = (format(opcode, "08b"))
    instruction.pop(0)
    machineCode += format(int(instruction[0][1:]), "04b")
    instruction.pop(0)
    if opcode | 1 == 0x25 or opcode | 1 == 0x2B:    # LDA, LDAI, STA, STAI
        machineCode += format(int(instruction[0][1:]), "04b")
        if opcode % 2 == 0:                         # LDA, STA
            machineCode += format(int(instruction[1][1:]), "04b")
            machineCode += format(0, "012b")
        else:                                       # LDAI, STAI
            machineCode += format(int(instruction[1]), "016b")
    elif opcode % 2 == 0:                           # MV
        machineCode += format(int(instruction[0][1:]), "04b")
        machineCode += format(0, "016b")
    else:                                           # MVI
        machineCode += format(int(instruction[0], 0), "020b")
    return machineCode

def assembleFlowControl(instruction):
    opcode = instructionSet[instruction[0]]
    machineCode  = (format(opcode, "08b"))
    if   opcode == 0x42:    # BR
        machineCode += format(int(instruction[1][1:]), "04b")
        machineCode += format(0, "020b")
    elif opcode == 0x43:    # BRI
        machineCode += format(int(instruction[1], 0), "024b")
    elif opcode == 0x4C:    # BRZ
        machineCode += format(int(instruction[1][1:]), "04b")
        machineCode += format(int(instruction[2][1:]), "04b")
        machineCode += format(0, "020b")
    elif opcode == 0x4D:    # BRZI
        machineCode += format(int(instruction[1][1:]), "04b")
        machineCode += format(int(instruction[2], 0), "020b")
    else:                   # BRE, BREI, BRN, BRNI, BRL, BRLI, BRG, BRGI
        machineCode += format(int(instruction[1][1:]), "04b")
        machineCode += format(int(instruction[2][1:]), "04b")
        if opcode % 2 == 0: # BRE, BRN, BRL, BRG
            machineCode += format(int(instruction[3][1:]), "04b")
            machineCode += format(0, "012b")
        else:               # BREI, BRNI, BRLI. BRGI
            machineCode += format(int(instruction[3], 0), "016b")

    return machineCode    

def assemble(assembly):
    assembly = [x.split() for x in assembly.upper().split("\n") if x != ""]
    (memory, assembly) = preprocessor(assembly)

    machineCode = [] 
    for i in range(len(assembly)):
        instruction = assembly[i]
        opcode = instructionSet[instruction[0]]
        #print "Current instruction: "
        #print instruction
        
        if opcode == 0x00:
            machineCode.append(format(0, "032b"))
        elif opcode == 0xFF:
            machineCode.append(format(0xFFFFFFFF, "032b"))
        elif opcode < 0x20:
            machineCode.append(assembleArithmetic(instruction))
        elif opcode < 0x40:
            machineCode.append(assembleMemory(instruction))
        else:
            machineCode.append(assembleFlowControl(instruction))
         
    finalString = ""
    for i in range(len(memory)):
        finalString += memory[i] + "\n"
   
    finalString += "---" + "\n" 
    finalString += "\n".join(machineCode)

    return finalString + "\n"

def main():
    filename = sys.argv[1]
    print "Assembling code held in " + filename

    with open(filename, 'r') as instructionFile:
       assembly = instructionFile.read()

    machineCode = assemble(assembly)
    
    with open(filename.split('.')[0] + ".out", 'w') as outFile:
        outFile.write(machineCode)

if __name__ == "__main__":
    main()
