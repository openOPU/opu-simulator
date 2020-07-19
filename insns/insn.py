from abc import ABC, abstractmethod

def uint_field(i, offset, width):
    return (i >> offset) % (1 << width)

def int_field(i, offset, width):
    tmp = (i >> offset) % (1 << (width - 1))
    if (i >> (offset + width - 1)) % 2 != 0:
        tmp -= 2 ** (width - 1)
    return tmp

def all_defined(lst):
    return all([x is not None for x in lst])

class Insn(ABC):

    @classmethod
    @abstractmethod
    def decode(cls, i):
        pass

    @classmethod
    def is_valid(cls, opu, *args):
        pass

    @classmethod
    def apply(cls, opu):
        pass

    @classmethod
    def do(cls, opu, i):
        decoded = cls.decode(i)
        if not cls.is_valid(opu, *decoded):
            raise ValueError('Invalid instruction: ' + hex(i))
        cls.apply(opu, *decoded)
