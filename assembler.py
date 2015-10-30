import sys
import re

instructionSet = {  "NOP"  : 0b00000000,                        # No operation
                                         "MEM"  : 0b00000001,   # Used by assembler for laying out data memory. Not actual instruction.

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
                    "BRZ"  : 0b01001100, "BRZI" : 0b01001101}   # Branch if OP1 == 0   to memory address [OP2/IMM]

def findLabels(assembly):
    labels = {}

    for i in range(len(assembly)):
        instruction = assembly[i]
        if re.search(r'^"\w+"$', instruction[-1]) != None:
            labels[instruction[-1][1:-1]] = i
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

# TODO: Divide this into multiple functions, one for each type of instruction
def assemble(assembly):
    labels = findLabels(assembly)
    assembly = replaceLabels(assembly, labels)
    machineCode = [] 
    for i in range(len(assembly)):
        instruction = assembly[i]
        opcode = instructionSet[instruction[0]]
        
        print "Current instruction: "
        print instruction
        machineCode.append(format(opcode, "08b"))
        
        if opcode == 0x00:          # No operation
            machineCode[i] = format(0, "032b")
        #elif opcode == 0x01:        # Memory psuedo-instruction
        
        elif opcode < 0x20:         # Arithmetic and logic
            machineCode[i] += format(int(instruction[1][1:]), "04b")
            machineCode[i] += format(int(instruction[2][1:]), "04b")
            if opcode % 2 == 0:
                machineCode[i] += format(int(instruction[3][1:]), "04b")
                machineCode[i] += format(0, "012b")
            else:
                machineCode[i] += format(int(instruction[3], 0), "016b")

        elif opcode < 0x40:         # Memory operations
            instruction.pop(0)
            machineCode[i] += format(int(instruction[0][1:]), "04b")
            instruction.pop(0)

            if opcode | 1 == 0x25 or opcode | 1 == 0x2B:
                machineCode[i] += format(int(instruction[0][1:]), "04b")
                instruction.pop(0)
            if opcode % 2 == 0:
                machineCode[i] += format(int(instruction[0][1:]), "04b")
            elif opcode | 1 == 0x25 or opcode | 1 == 0x2B:
                machineCode[i] += format(int(instruction[0], 0), "016b")
            else:
                machineCode[i] += format(int(instruction[0], 0), "020b")
                    
        else:                       # Flow control operations
            if   opcode == 0x42:    # BR
                machineCode[i] += format(int(instruction[1][1:]), "04b")
            elif opcode == 0x43:    # BRI
                machineCode[i] += format(int(instruction[1], 0), "024b")
            elif opcode == 0x4C:    # BRZ
                machineCode[i] += format(int(instruction[1][1:]), "04b")
                machineCode[i] += format(int(instruction[2][1:]), "04b")
            elif opcode == 0x4D:    # BRZI
                machineCode[i] += format(int(instruction[1][1:]), "04b")
                machineCode[i] += format(int(instruction[2], 0), "020b")
            else:
                machineCode[i] += format(int(instruction[1][1:]), "04b")
                machineCode[i] += format(int(instruction[2][1:]), "04b")
                if opcode % 2 == 0:
                    machineCode[i] += format(int(instruction[3][1:]), "04b")
                else:
                    machineCode[i] += format(int(instruction[3], 0), "016b")

    return machineCode

def main():
    filename = sys.argv[1]
    print "Assembling code held in " + filename

    with open(filename, 'r') as instructionFile:
       assembly = instructionFile.read()
    assembly = [x.split() for x in assembly.upper().split("\n") if x != ""]

    assemble(assembly)

if __name__ == "__main__":
    main()
