import sys
import numpy as np
from opu import OPU
from vmem import VirtualMemory
from datatype import Int8, Int16

class Simulator:

    def __init__(self, interactive=False):
        self.processor = OPU(
            itype=Int8,
            ktype=Int8,
            btype=Int16,
            otype=Int16,
        )
        self.vmem = VirtualMemory()
        self.processor.attach_vmem(self.vmem)
        self.interactive = interactive

    def exec_line(self, line):
        parts = line.split()

        if parts[0] == 'write':
            addr = int(parts[1])
            value = int(parts[2])
            self.vmem[addr] = value

        elif parts[0] == 'read':
            addr = int(parts[1])
            print(self.vmem[addr])

        elif parts[0] == 'run':
            path = parts[1]
            prog = np.fromfile(path, dtype=np.uint32).tolist()
            self.processor.run(prog)

        else:
            print('[!] : Unknown command')
            return

    @staticmethod
    def welcome():
        print('---------------------')
        print('| OPU ISA simulator |')
        print('---------------------')

    def run(self):
        if self.interactive:
            self.welcome()

        try:
            while True:
                if self.interactive:
                    line = input('> ')
                else:
                    line = input()

                self.exec_line(line)

        except EOFError:
            if self.interactive:
                print('\nBye!')


if __name__ == '__main__':
    Simulator(sys.stdout.isatty() and sys.stdin.isatty()).run()
