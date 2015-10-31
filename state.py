import numpy as np
memory = np.zeros(1024, dtype=np.int32)
instructions = np.zeros(1024, dtype=np.uint32)
registers = np.zeros(16, dtype=np.int32)
programCounter = np.uint32(0)

