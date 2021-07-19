#!/usr/bin/python
from glob import glob
import random

class ShuffledList(object):
    def __init__(self, name, glob):
        self.glob = glob
    def pop(self):
        files = glob(self.glob)
        return random.choice(files)



if __name__ == '__main__':
    sl = ShuffledList('winicons','source/*.png')
    while True:
        print sl.pop()
