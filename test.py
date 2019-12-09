import random
from utilis import *
from bloom_filter import *
from bit_array import *
from compress import *

com = Compress(4, 25)
com.read_fasta("ecoli_sample_50Kb_reads_30x.fasta", 8)
print(com.bf.exists("AAAAAAAA"))