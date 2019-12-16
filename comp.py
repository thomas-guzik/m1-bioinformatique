import sys
import gzip


class Comp:
    
    def __init__(self, file_name):
        self.read_size = 0
        self.kmer_len = 0
        self.file_name = file_name
        try:
            with open(self.file_name, "r") as f:
                self.read_size = int(f.readline())
                line = f.readline()
                if " " in line:
                    self.kmer_len = f.readline().index(" ")
                else:
                    self.kmer_len = len(line)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(1)
    
    def readlines(self):
        with open(self.file_name, "r") as f:
            f.readline()
            for l in f.readlines():
                yield l.replace("\n", "").split(" ")