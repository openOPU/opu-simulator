import numpy as np
from .insn import Insn, uint_field, all_defined

# Constants as defined in the ISA manual
ORDER_ACT_RES_POOL = 0
ORDER_RES_ACT_POOL = 1
ORDER_ACT_POOL_RES = 2

class StoreInsn(Insn):
    """store instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 22),
        )

    @classmethod
    def is_valid(cls, opu, addr):
        return all_defined([
            opu.ofm, opu.reg.ofm_h, opu.reg.ofm_w, opu.reg.ofm_c,
            opu.reg.ofm_mem_w, opu.reg.ofm_addr, opu.reg.post_order, opu.reg.add_ifm,
            opu.reg.pool_h, opu.reg.pool_w, opu.reg.pool_h_stride, opu.reg.pool_w_stride,
            opu.reg.act
        ])

    @classmethod
    def activation(cls, opu, x):
        """Compute activations."""

        if opu.reg.act == 0:
            return x
        if opu.reg.act == 1:
            return opu.itype.from_real(np.maximum(x.to_real(), opu.itype.zero().to_real()))
        if opu.reg.act == 2:
            x = x.to_real()
            return opu.itype.from_real(np.maximum(x, x / 8))

    @classmethod
    def add_ifm(cls, opu, x):
        """Add the content of the ifm buffer (residuals)."""

        if opu.reg.add_ifm == 0:
            return x
        return opu.itype.from_real(x.to_real() + opu.ifm.to_real())

    @classmethod
    def pool(cls, opu, x):
        """Apply the max pooling filter."""

        x = x.to_real()
        h = (opu.reg.ofm_h - opu.reg.pool_h) // opu.reg.pool_h_stride + 1
        w = (opu.reg.ofm_w - opu.reg.pool_w) // opu.reg.pool_w_stride + 1
        out = np.empty([h, w, x.shape[-1]], dtype=x.dtype)

        for i in range(h):
            for j in range(w):
                f = x[i*opu.reg.pool_h_stride:i*opu.reg.pool_h_stride+opu.reg.pool_h, \
                        j*opu.reg.pool_w_stride:j*opu.reg.pool_w_stride+opu.reg.pool_w, :]
                out[i, j, :] = f.max(axis=(0, 1))

        return opu.itype.from_real(out)

    @classmethod
    def apply(cls, opu, addr):
        x = opu.itype.from_real(opu.ofm.to_real() * 2.0 ** -8)

        # use cases
        if opu.reg.post_order == ORDER_ACT_RES_POOL:
            x = StoreInsn.activation(opu, x)
            x = StoreInsn.add_ifm(opu, x)
            x = StoreInsn.pool(opu, x)
        elif opu.reg.post_order == ORDER_RES_ACT_POOL:
            x = StoreInsn.add_ifm(opu, x)
            x = StoreInsn.activation(opu, x)
            x = StoreInsn.pool(opu, x)
        elif opu.reg.post_order == ORDER_ACT_POOL_RES:
            x = StoreInsn.activation(opu, x)
            x = StoreInsn.pool(opu, x)
            x = StoreInsn.add_ifm(opu, x)
        else:
            raise ValueError('Invalid post_order')

        shape = x.shape
        n = x.size
        x = x.to_uint8().reshape([shape[0], shape[1], shape[2], n])

        addr_base = addr * 64 + opu.reg.ofm_addr
        bytes_per_element = opu.itype.size
        for i in range(shape[0]):
            for j in range(shape[1]):
                addr = addr_base + (j + i * opu.reg.ofm_mem_w) * 64 * bytes_per_element
                opu.vmem[addr:addr+x.shape[2]*bytes_per_element] = x[i, j, :, :].flatten()



class PadInsn(Insn):
    """pad instruction"""

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 22),
            uint_field(i, 28, 4),
        )

    @classmethod
    def is_valid(cls, opu, addr, p):
        return all_defined([
            opu.reg.ofm_addr, opu.reg.ofm_mem_h, opu.reg.ofm_mem_w
        ])

    @classmethod
    def apply(cls, opu, addr, p):
        ver = opu.itype.from_real(np.zeros([64 * p])).to_real()
        hor = opu.itype.from_real(np.zeros([opu.reg.ofm_mem_w * 64])).to_real()
        addr_base = opu.reg.ofm_addr + addr * 64
        for i in range(p):
            a = addr_base + i * 64 * opu.reg.ofm_mem_w
            opu.vmem[a:a+64*opu.reg.ofm_mem_w] = hor
            a += (opu.reg.ofm_mem_h - p) * 64 * opu.reg.ofm_mem_w
            opu.vmem[a:a+64*opu.reg.ofm_mem_w] = hor
        for i in range(opu.reg.ofm_mem_h):
            a = addr_base + i * 64 * opu.reg.ofm_mem_w
            opu.vmem[a:a+64*p] = ver
            a += (opu.reg.ofm_mem_w - p) * 64
            opu.vmem[a:a+64*p] = ver
