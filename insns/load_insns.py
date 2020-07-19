from .insn import Insn, uint_field, all_defined


class LdIfmInsn(Insn):

    @classmethod
    def decode(cls, i):
        return (uint_field(i, 6, 22),)

    @classmethod
    def is_valid(cls, opu, addr):
        return all_defined([opu.reg.ifm_mem_w, opu.reg.ifm_h, opu.reg.ifm_c])

    @classmethod
    def apply(cls, opu, addr):
        addr = addr * 64 + opu.reg.ifm_addr
        size = opu.reg.ifm_mem_w * opu.reg.ifm_h * 64
        bytes_per_value = opu.itype.size

        data = opu.vmem[addr:addr+size*bytes_per_value]
        data = data.reshape([opu.reg.ifm_h, opu.reg.ifm_mem_w, 64, -1])
        data = data[:, :opu.reg.ifm_w, :opu.reg.ifm_c, :]
        data = opu.itype.from_uint8(data)
        data = data.reshape([opu.reg.ifm_h, opu.reg.ifm_mem_w, opu.reg.ifm_c])
        opu.ifm = data


class LdKerInsn(Insn):

    @classmethod
    def decode(cls, i):
        return (uint_field(i, 6, 22),)

    @classmethod
    def is_valid(cls, opu, addr):
        return all_defined([opu.reg.ofm_c, opu.reg.ifm_c, opu.reg.ker_n]) \
            and opu.reg.ker_n * max(opu.reg.ifm_c * opu.reg.ofm_c / 1024, 1) <= 36

    @classmethod
    def apply(cls, opu, addr):
        addr = addr * 64 + opu.reg.ker_addr
        size = opu.reg.ker_n * opu.reg.ifm_c * opu.reg.ofm_c
        bytes_per_value = opu.ktype.size

        data = opu.vmem[addr:addr+size*bytes_per_value]
        data = opu.ktype.from_uint8(data)
        data = data.reshape([opu.reg.ker_n, opu.reg.ofm_c, opu.reg.ifm_c])
        opu.ker = data


class LdBiasInsn(Insn):

    @classmethod
    def decode(cls, i):
        return (uint_field(i, 6, 22),)

    @classmethod
    def is_valid(cls, opu, addr):
        return opu.reg.ofm_c is not None

    @classmethod
    def apply(cls, opu, addr):
        addr = addr * 64 + opu.reg.ker_addr
        size = opu.reg.ofm_c
        bytes_per_value = opu.btype.size

        data = opu.vmem[addr:addr+size*bytes_per_value]
        data = opu.btype.from_uint8(data)
        data = data.reshape([opu.reg.ofm_c])
        opu.bias = data
