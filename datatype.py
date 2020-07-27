from abc import ABC, abstractclassmethod, abstractmethod
import numpy as np

class IntArray(ABC):
    """This class stores an ndarray of integers."""

    np_type = None # internal data type
    max = None # max representable value
    min = None # min representable value
    size = None # number of bytes per element

    def __init__(self, data):
        """Initialize a new array from a np.dnarray."""

        self.data = data
        self.shape = data.shape

    def reshape(self, shape):
        """Reshape this array."""

        self.shape = shape
        self.data = self.data.reshape(shape)
        return self

    @classmethod
    def zero(cls):
        """Return the the representation of the scalar 0."""

        data = np.zeros(1, dtype=cls.np_type)
        return cls(data)

    @classmethod
    def from_real(cls, real_data):
        """Convert an array of double into this integer type."""

        data = np.floor(real_data).astype(cls.np_type)
        mask = abs(data - real_data) >= 0.5
        data[mask] += 1
        data[data >= cls.max] = cls.max
        data[data <= cls.min] = cls.min
        return cls(data)

    def to_real(self):
        """Convert this array to double precision."""

        return self.data.astype(np.float64)

    @abstractclassmethod
    def from_uint8(cls, data):
        """Create an array of this type from bytes."""

    @abstractmethod
    def to_uint8(self):
        """Return the bytes of this array."""


class Int8(IntArray):
    """This class represent an array of int8 values."""

    max = 2 ** 7 - 1
    min = - 2 ** 7
    size = 1
    np_type = np.int8

    @classmethod
    def from_uint8(cls, data):
        return cls(data.astype(np.int8))

    def to_uint8(self):
        return self.data.astype(np.uint8)


class Int16(IntArray):
    """This class represent an array of int16 values."""

    max = 2 ** 15 - 1
    min = - 2 ** 15
    size = 2
    np_type = np.int16

    @classmethod
    def from_uint8(cls, data):
        data = data.tobytes()
        data = np.frombuffer(data, dtype=np.int16)
        return cls(data)

    def to_uint8(self):
        data = self.data.tobytes()
        data = np.frombuffer(data, dtype=np.uint8)
        return data
