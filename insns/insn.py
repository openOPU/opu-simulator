from abc import ABC, abstractmethod

def uint_field(i, offset, width):
    """Extract an uint field from an encoded instruction."""

    return (i >> offset) % (1 << width)

def int_field(i, offset, width):
    """Extract an int field from an encoded instruction."""

    tmp = (i >> offset) % (1 << (width - 1))
    if (i >> (offset + width - 1)) % 2 != 0:
        tmp -= 2 ** (width - 1)

    return tmp

def all_defined(lst):
    """Returns True iff all are different from None."""

    return all([x is not None for x in lst])

class Insn(ABC):
    """This class represents an instruction of the OPU ISA."""

    @classmethod
    @abstractmethod
    def decode(cls, i):
        """Return a tuple of decoded fields."""

    @classmethod
    def is_valid(cls, opu, *args):
        """Return True iff the fields form a valid instruction."""

    @classmethod
    def apply(cls, opu, *args):
        """Run the decoded instruction on the processor."""

    @classmethod
    def do(cls, opu, i):
        """Run the encoded instruction on the processor."""

        decoded = cls.decode(i)
        if not cls.is_valid(opu, *decoded):
            raise ValueError('Invalid instruction: ' + hex(i))
        cls.apply(opu, *decoded)
