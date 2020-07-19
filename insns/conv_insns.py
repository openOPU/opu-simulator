import numpy as np
from .insn import Insn, uint_field, all_defined


class ConvInsn(Insn):

    @classmethod
    def decode(cls, i):
        return (
            uint_field(i, 6, 4),
            uint_field(i, 10, 4),
            uint_field(i, 14, 6),
        )

    @classmethod
    def is_valid(cls, opu, h, w, n):
        return all_defined([
            opu.ifm, opu.ker, opu.reg.ofm_c, opu.reg.ofm_h, opu.reg.ofm_w,
            opu.reg.stride_w, opu.reg.stride_h, opu.reg.ifm_shift, opu.reg.bias_shift
        ]) and h + (opu.reg.ofm_h - 1) * opu.reg.stride_h < opu.reg.ifm_h and \
            w + (opu.reg.ofm_w - 1) * opu.reg.stride_w < opu.reg.ifm_w

    @classmethod
    def conv(cls, opu, h, w, n):
        ifm = opu.ifm.to_real()
        ker = opu.ker.to_real()

        i_end = h + (opu.reg.ofm_h - 1) * opu.reg.stride_h + 1
        j_end = w + (opu.reg.ofm_w - 1) * opu.reg.stride_w + 1
        ifm = ifm[h:i_end:opu.reg.stride_h, w:j_end:opu.reg.stride_w, :]
        ker = ker[n, :, :]

        out = ifm.dot(ker.T)
        return out * (2. ** opu.reg.ifm_shift)

    @classmethod
    def apply(cls, opu, h, w, n):
        ofm = ConvInsn.conv(opu, h, w, n)
        opu.ofm = opu.otype.from_real(ofm)



class ConvBiasInsn(ConvInsn):

    @classmethod
    def is_valid(cls, opu, h, w, n):
        return ConvInsn.is_valid(opu, h, w, n) and all_defined([opu.bias])

    @classmethod
    def apply(cls, opu, h, w, n):
        ofm = ConvInsn.conv(opu, h, w, n)
        bias = opu.bias.to_real()
        ofm = ofm + bias[np.newaxis, np.newaxis, :] * (2. ** opu.reg.bias_shift)
        opu.ofm = opu.otype.from_real(ofm)


class ConvAccInsn(ConvInsn):

    @classmethod
    def is_valid(cls, opu, h, w, n):
        return ConvInsn.is_valid(opu, h, w, n) and all_defined([opu.ofm])

    @classmethod
    def apply(cls, opu, h, w, n):
        ofm = ConvInsn.conv(opu, h, w, n)
        ofm = opu.ofm.to_real() + ofm
        opu.ofm = opu.otype.from_real(ofm)
