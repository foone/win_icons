#!/usr/bin/python
from redis import Redis
from glob import glob
import random

class ShuffledList(object):
    def __init__(self, name, glob):
        self.redis=Redis()
        self.name = name
        self.glob = glob
    def pop(self):
        r = self.redis.rpop(self.name)
        if r is None:
            self.refresh()
            return self.pop()
        else:
            return r
    def refresh(self):
        files = glob(self.glob)
        random.shuffle(files)
        self.redis.rpush(self.name, *files)



if __name__ == '__main__':
    sl = ShuffledList('winicons','source/*.png')
    while True:
        print sl.pop()
