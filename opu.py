import traceback
import sys
from insns.opcodes import opcodes

IFM_SIZE = 64 * 2048
BIAS_SIZE = 64
KER_SIZE = 1024 * 36
OFM_SIZE = 64 * 2048

class OPU:
    """This class represents an OPU processor."""

    def __init__(self, itype, btype, ktype, otype):
        """Initialize the processor with specified data types."""

        self.itype = itype
        self.btype = btype
        self.ktype = ktype
        self.otype = otype
        self.ifm = None
        self.bias = None
        self.ker = None
        self.ofm = None
        self.reg = RegisterFile()
        self.vmem = None
        self.ended = False

    def attach_vmem(self, vmem):
        """Attach a virtual memory object to this instance.

        This method should be called before simulating any program.
        """
        self.vmem = vmem

    def run(self, prog):
        """Run a program given as a list of int values."""

        self.ended = False
        for i in prog:
            opcode = i & 0b111111
            if opcode == 0:
                self.ended = True
            else:
                try:
                    opcodes[opcode].do(self, i)
                except Exception:
                    print('Error at instruction: 0x%x (opcode: %d)' % (i, opcode), file=sys.stderr)
                    traceback.print_exc()
                    sys.exit(-1)

class RegisterFile:
    """This class stores the value of the registers of the OPU ISA."""

    def __init__(self):
        """Initialize the registers with None values."""

        self.ifm_h = None
        self.ifm_w = None
        self.ifm_c = None
        self.ofm_h = None
        self.ofm_w = None
        self.ofm_c = None
        self.ker_n = None
        self.stride_h = None
        self.stride_w = None
        self.ifm_addr = None
        self.ker_addr = None
        self.bias_addr = None
        self.ifm_mem_w = None
        self.ofm_mem_w = None
        self.ofm_mem_h = None
        self.ifm_shift = None
        self.bias_shift = None
        self.post_order = None
        self.add_ifm = None
        self.act = None
        self.pool_h = None
        self.pool_w = None
        self.pool_h_stride = None
        self.pool_w_stride = None
