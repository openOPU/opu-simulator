
from .config_insns import *
from .load_insns import *
from .conv_insns import *
from .store_insns import *

opcodes = [
    None,           # 0
    LdIfmInsn,      # 1
    LdKerInsn,      # 2
    LdBiasInsn,     # 3
    ConvInsn,       # 4
    ConvBiasInsn,   # 5
    ConvAccInsn,    # 6
    StoreInsn,      # 7
    PadInsn,        # 8
    None,           # 9
    None,           # 10
    None,           # 11
    None,           # 12
    None,           # 13
    None,           # 14
    None,           # 15
    ShapeIfmInsn,   # 16
    ShapeOfmInsn,   # 17
    ShapeKerInsn,   # 18
    MemIfmInsn,     # 19
    MemKerInsn,     # 20
    MemBiasInsn,    # 21
    MemOfmInsn,     # 22
    StrideInsn,     # 23
    ShiftInsn,      # 24
    PostInsn,       # 25
    PoolInsn,       # 26
]
