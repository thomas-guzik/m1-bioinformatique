#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Compress compresses fasta file in a bloom filter"""

from bloom_filter import BloomFilter
from utilis import canonical


class Compress:
    
    def __init__(self, n_hash_fc, array_len):
        self.n_hash_fc = n_hash_fc
        self.array_len = array_len
        self.bloom_filter = BloomFilter(self.n_hash_fc, self.array_len)
    
    def read_fasta(self, file_name, kmer_len):
        with open(file_name, "r") as f:
            for l in f.readlines():
                if l[0] in "ACGT":
                    for i in range(0, len(l)-kmer_len):
                        self.bloom_filter.add(canonical(l[i:i+kmer_len]))
