import math
import sys
CACHESIZE = int(sys.argv[1])
ASSOC = int(sys.argv[2])
REPLACEMENT = ""
if int(sys.argv[3]) == 0:
    REPLACEMENT = "LRU"
elif int(sys.argv[3]) == 1:
    REPLACEMENT = "FIFO"
WRITETYPE = ""
if int(sys.argv[4]) == 0:
    WRITETYPE = "WT"
elif int(sys.argv[4]) == 1:
    WRITETYPE = "WB"
TRACEFILE = sys.argv[5]
BLOCKSIZE = 64
VERBOSE = False
num_sets = int((CACHESIZE / BLOCKSIZE) / ASSOC)


def main():
    if VERBOSE:
        printParameters()
    f = open(TRACEFILE, "r")
    lines = f.readlines()
    cache = cacheStruct()
    hits = 0
    misses = 0
    writes = 0
    for i in range(len(lines)):
        num_set_bits = math.log(num_sets,2)
        op = lines[i][0]
        address = int(lines[i][2:], 16)
        set_num = int(address/BLOCKSIZE) % num_sets
        tag_address = int(address/BLOCKSIZE)
        hit,write = cache.index[set_num].lookup(tag_address, op)
        if hit == 1:
            hits += 1
        elif hit == 0:
            misses += 1
        writes += write

    print(misses/ (misses + hits))
    print(writes)
    print(misses)
    return (misses/ (misses + hits)), writes, misses



class cacheMember():
    def __init__(self):
        self.tags = []
        self.dirtys = []

    def lookup(self, add, op):
        hit = 0
        write = 0
        read = 0
        for tag in self.tags:
            if tag == add:
                hit = 1

        if REPLACEMENT == "FIFO":
            if hit == 0:
                self.tags.append(add)
                if len(self.tags) > ASSOC:
                    removed = self.tags[0]
                    self.tags.pop(0)
                    if removed in self.dirtys:
                        write = 1
                        self.dirtys.remove(removed)

        elif REPLACEMENT == "LRU":
            removed = -1
            if hit == 1:
                self.tags.remove(add)
            self.tags.append(add)
            if len(self.tags) > ASSOC:
                removed = self.tags[0]
                self.tags.pop(0)
                if removed in self.dirtys:
                    write = 1
                    self.dirtys.remove(removed)

        if op == 'W':
            if WRITETYPE == "WT":
                write = 1
            elif WRITETYPE == "WB":
                if not add in self.dirtys:
                    self.dirtys.append(add)

        return hit, write

class cacheStruct():
    def __init__(self):
        self.index = []
        for i in range(num_sets):
            self.index.append(cacheMember())
    def report(self):
        for tag in self.index:
            print(tag.tags)
            print("dirtys", tag.dirtys)
            print()
        return

def printParameters():
    print(CACHESIZE)
    print("\t", type(CACHESIZE))
    print(ASSOC)
    print("\t", type(ASSOC))
    print(REPLACEMENT)
    print("\t", type(REPLACEMENT))
    print(WRITETYPE)
    print("\t", type(WRITETYPE))
    print(TRACEFILE)
    print("\t", type(TRACEFILE))




if __name__ == '__main__':
    main()
