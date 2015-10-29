MEM 0 0xDEAD

LD      R0 0
LDI     R1 0xBEEF 

LSI     R0 R0 1     "MyLabel"
ADD     R2 R0 R1

BRNI    R2 0xDEADBEEF >MyLabel
