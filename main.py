from numpy import binary_repr
from prettytable import PrettyTable
import random
import keyboard

'''
2 address
14 bits
add
'''


class Process:
    def __init__(self):
        self.r1 = random.randint(0, 2**14)
        self.r2 = random.randint(0, 2**14)
        self.pc = self.tc = 1
        self.ps = '-'
        self.length = 14

    def info(self, command):
        keyboard.wait('enter')
        pt = PrettyTable()
        col_names = ['elements', 'status']
        pt.add_column(col_names[0], ['IR: ', 'R1: ', 'R2: ', 'PS: ', 'PC: ', 'TC: '])
        pt.add_column(col_names[1], [' '.join(command), binary_repr(self.r1, width=self.length),
                                     binary_repr(self.r2, width=self.length),
                                     str(self.ps), str(self.pc), str(self.tc)])
        print(pt, end='\n\n')

    def mov(self, command):
        self.tc = 1
        self.info(command)
        if len(binary_repr(int(command[2]))) <= self.length:
            if command[1] == 'R1':
                self.r1 = int(command[2])
                self.ps = '+' if self.r1 < 0 else '+'
            else:
                self.r2 = int(command[2])
                self.ps = '+' if self.r2 < 0 else '+'
        else:
            raise ValueError('number is more than ' + str(self.length) + 'bits')
        self.tc = 2
        self.info(command)
        self.pc += 1

    def add(self, command):
        self.tc = 1
        self.info(command)
        self.r1 += self.r2
        if len(binary_repr(self.r1)) > self.length:
            raise ValueError('number is more than ' + str(self.length) + 'bits')
        self.ps = '+' if self.r1 < 0 else '-'
        self.tc = 2
        self.info(command)
        self.pc += 1

    def command(self, cmnd):
        if cmnd[0] == 'mov':
            self.mov(cmnd)
        elif cmnd[0] == 'add':
            self.add(cmnd)


with open('source_2_5_1.txt') as file:
    contents = file.readlines()

prc = Process()
for line in contents:
    prc.command(line.split())
