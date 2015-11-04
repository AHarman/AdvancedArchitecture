import numpy as np
memory = np.zeros(256, dtype=np.uint32)
instructions = np.zeros(256, dtype=np.uint32)

# Used for debugging
instructionText = {
    0x00 : "NOP", 0x01 : "MEM",
    0x02 : "ADD", 0x03 : "ADDI",
    0x04 : "SUB", 0x05 : "SUBI",
    0x06 : "MUL", 0x07 : "MULI",
    0x08 : "AND", 0x09 : "ANDI",
    0x0A : "OR",  0x0B : "ORI",
    0x0C : "LS",  0x0D : "LSI",
    0x0E : "RS",  0x0F : "RSI",
    0x22 : "LD",  0x23 : "LDI",
    0x24 : "LDA", 0x25 : "LDAI",
    0x26 : "MV",  0x27 : "MVI",
    0x28 : "ST",  0x29 : "STI",
    0x2A : "STA", 0x2B : "STAI",
    0x42 : "BR",  0x43 : "BRI",
    0x44 : "BRE", 0x45 : "BREI",
    0x46 : "BRN", 0x47 : "BRNI",
    0x48 : "BRL", 0x49 : "BRLI",
    0x4A : "BRG", 0x4B : "BRGI",
    0x4C : "BRZ", 0x4D : "BRZI",
    0xFF : "TRM"}
