from .insn import Insn, int_field, uint_field

class ShapeIfmInsn(Insn):
    """@shape.ifm instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 7),
            uint_field(i, 13, 7),
            2 ** uint_field(i, 20, 7),
        )

    @classmethod
    def is_valid(cls, opu, h, w, c):
        return 1 <= h*w <= 2048 and 16 <= c <= 64

    @classmethod
    def apply(cls, opu, h, w, c):
        opu.ifm = None
        opu.ker = None
        opu.reg.ifm_h = h
        opu.reg.ifm_w = w
        opu.reg.ifm_c = c

class ShapeOfmInsn(Insn):
    """@shape.ofm instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 7),
            uint_field(i, 13, 7),
            2 ** uint_field(i, 20, 7),
        )

    @classmethod
    def is_valid(cls, opu, h, w, c):
        return 1 <= h*w <= 2048 and 2 <= c <= 64

    @classmethod
    def apply(cls, opu, h, w, c):
        opu.ofm = None
        opu.ker = None
        opu.reg.ofm_h = h
        opu.reg.ofm_w = w
        opu.reg.ofm_c = c


class ShapeKerInsn(Insn):
    """@shape.ker instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 6),
        )

    @classmethod
    def is_valid(cls, opu, n):
        return 1 <= n <= 36

    @classmethod
    def apply(cls, opu, n):
        opu.ker = None
        opu.reg.ker_n = n


class MemIfmInsn(Insn):
    """@mem.ifm instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 4) << 28,
            uint_field(i, 10, 10),
        )

    @classmethod
    def is_valid(cls, opu, addr, w):
        return True

    @classmethod
    def apply(cls, opu, addr, w):
        opu.reg.ifm_addr = addr
        opu.reg.ifm_mem_w = w


class MemKerInsn(Insn):
    """@mem.ker instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 4) << 28,
        )

    @classmethod
    def is_valid(cls, opu, addr):
        return True

    @classmethod
    def apply(cls, opu, addr):
        opu.reg.ker_addr = addr


class MemBiasInsn(Insn):
    """@mem.bias instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 4) << 28,
        )

    @classmethod
    def is_valid(cls, opu, addr):
        return True

    @classmethod
    def apply(cls, opu, addr):
        opu.reg.bias_addr = addr


class MemOfmInsn(Insn):
    """@mem.ofm instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 4) << 28,
            uint_field(i, 10, 10),
            uint_field(i, 20, 10),
        )

    @classmethod
    def is_valid(cls, opu, addr, h, w):
        return h >= 1 and w >= 1

    @classmethod
    def apply(cls, opu, addr, h, w):
        opu.reg.ofm_addr = addr
        opu.reg.ofm_mem_h = h
        opu.reg.ofm_mem_w = w


class StrideInsn(Insn):
    """@stride instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 3),
            uint_field(i, 9, 3),
        )

    @classmethod
    def is_valid(cls, opu, h, w):
        return h >= 1 and w >= 1

    @classmethod
    def apply(cls, opu, h, w):
        opu.reg.stride_h = h
        opu.reg.stride_w = w


class ShiftInsn(Insn):
    """@shift instruction"""

    @classmethod
    def decode(cls, i):
        return (
            int_field(i, 6, 8),
            int_field(i, 14, 8),
        )

    @classmethod
    def is_valid(cls, opu, f, b):
        return True

    @classmethod
    def apply(cls, opu, f, b):

        opu.reg.ifm_shift = f
        opu.reg.bias_shift = b


class PostInsn(Insn):
    """@post instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 2),
            uint_field(i, 8, 2),
            uint_field(i, 10, 1),
        )

    @classmethod
    def is_valid(cls, opu, act, order, res):
        return order == 0 or (order == 1 and act != 0 and res != 0) or (order == 2 and res != 0)

    @classmethod
    def apply(cls, opu, act, order, res):
        opu.reg.act = act
        opu.reg.post_order = order
        opu.reg.add_ifm = res


class PoolInsn(Insn):
    """@pool instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 4),
            uint_field(i, 10, 4),
            uint_field(i, 14, 3),
            uint_field(i, 17, 3),
        )

    @classmethod
    def is_valid(cls, opu, h, w, i, j):
        return h >= 1 and w >= 1 and i >= 1 and j >= 1

    @classmethod
    def apply(cls, opu, h, w, i, j):
        opu.reg.pool_h = h
        opu.reg.pool_w = w
        opu.reg.pool_h_stride = i
        opu.reg.pool_w_stride = j
