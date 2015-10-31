import numpy as np
memory = np.zeros(256, dtype=np.uint32)
instructions = np.zeros(256, dtype=np.uint32)
registers = np.zeros(16, dtype=np.uint32)
programCounter = np.uint32(0)

# Used for debugging
instructionText = {
    0b00000000 : "NOP", 0b00000001 : "MEM",
    0b00000010 : "ADD", 0b00000011 : "ADDI",
    0b00000100 : "SUB", 0b00000101 : "SUBI",
    0b00000110 : "MUL", 0b00000111 : "MULI",
    0b00001000 : "AND", 0b00001001 : "ANDI",
    0b00001010 : "OR",  0b00001011 : "ORI",
    0b00001100 : "LS",  0b00001101 : "LSI",
    0b00001110 : "RS",  0b00001111 : "RSI",
    0b00100010 : "LD",  0b00100011 : "LDI",
    0b00100100 : "LDA", 0b00100101 : "LDAI",
    0b00100110 : "MV",  0b00100111 : "MVI",
    0b00101000 : "ST",  0b00101001 : "STI",
    0b00101010 : "STA", 0b00101011 : "STAI",
    0b01000010 : "BR",  0b01000011 : "BRI",
    0b01000100 : "BRE", 0b01000101 : "BREI",
    0b01000110 : "BRN", 0b01000111 : "BRNI",
    0b01001000 : "BRL", 0b01001001 : "BRLI",
    0b01001010 : "BRG", 0b01001011 : "BRGI",
    0b01001100 : "BRZ", 0b01001101 : "BRZI",
    0b11111111 : "TRM"}
