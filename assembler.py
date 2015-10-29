import sys

instructionSet = {  "NOP"  : 0b00000000,

                    # Arithmetic and logic
                    "ADD"  : 0b00000010, "ADDI" : 0b00000011,
                    "SUB"  : 0b00000100, "SUBI" : 0b00000101,
                    "MUL"  : 0b00000110, "MULI" : 0b00000111,
                    "AND"  : 0b00001000, "ANDI" : 0b00001001,
                    "OR"   : 0b00001010, "ORI"  : 0b00001011,
                    "LS"   : 0b00001100, "LSI"  : 0b00001101,
                    "RS"   : 0b00001110, "RSI"  : 0b00001111,

                    # Memory operations
                    "LD"   : 0b00100010, "LDI"  : 0b00100011,
                    "LDR"  : 0b00100100, "LDRI" : 0b00100101,
                    "STR"  : 0b00101010, "STRI" : 0b00101011,

                    # Control flow
                    "BR"   : 0b01000010, "BRI"  : 0b01000011,
                    "BRE"  : 0b01000100, "BREI" : 0b01000101,
                    "BRN"  : 0b01000110, "BRNI" : 0b01000111,
                    "BRL"  : 0b01001000, "BRLI" : 0b01001001,
                    "BRG"  : 0b01001010, "BRGI" : 0b01001011,
                    "BRZ"  : 0b01001100}

def main():
    filename = sys.argv[1]
    print "Assembling code held in " + filename
    with open(filename, 'r') as instructionFile:
       assembly = instructionFile.read()
    assembly = [x.split() for x in assembly.split("\n") if x != ""]
    print assembly

if __name__ == "__main__":
    main()
