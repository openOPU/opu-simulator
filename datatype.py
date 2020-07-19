from abc import ABC, abstractclassmethod, abstractmethod
import numpy as np

class IntArray(ABC):
    np_type = None
    max = None
    min = None
    size = None

    def __init__(self, data):
        self.data = data
        self.shape = data.shape

    def reshape(self, shape):
        self.shape = shape
        self.data = self.data.reshape(shape)
        return self

    @classmethod
    def zero(cls):
        data = np.zeros(1, dtype=cls.np_type)
        return cls(data)

    @classmethod
    def from_real(cls, real_data):
        data = np.floor(real_data).astype(cls.np_type)
        mask = abs(data - real_data) >= 0.5
        data[mask] += 1
        data[data >= cls.max] = cls.max
        data[data <= cls.min] = cls.min
        return cls(data)

    def to_real(self):
        return self.data.astype(np.float64)

    @abstractclassmethod
    def from_uint8(cls, data):
        pass

    @abstractmethod
    def to_uint8(self):
        pass


class Int8(IntArray):
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
