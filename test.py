import random
from utilis import *
from BloomFilter import *
from bit_array import *
from fasta import Fasta
from kmer import Kmer

fasta = Fasta("tests/test1.fasta")
bf = BloomFilter(100, 5)
bf.import_fasta(fasta, 4)
bf.search_bifurcations("AACCGGTT", 8, 4)