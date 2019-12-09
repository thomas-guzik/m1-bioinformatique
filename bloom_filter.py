# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
BloomFilter is a probabilistic data structure which store information in an
array. To save data in an array, it uses a couple of hash functions which will
determine which bit must be set to True.
More information :
https://en.wikipedia.org/wiki/Bloom_filter
"""

import random
from utilis import kmer2hash
from bit_array import BitArray


class BloomFilter:
    
    def __init__(self, n_hash_fc, array_len):
        self.array_len = array_len
        self.array = BitArray(array_len)
        self.seeds = []
        for i in range(n_hash_fc):
            self.seeds.append(random.randint(0, 99999))
    
    def get_hash_values(self, kmer):
        """Return a list of hash values for a given kmer"""
        hash_values = []
        for s in self.seeds:
            hash_values.append(kmer2hash(kmer, s, self.array_len))
        return hash_values
    
    def add(self, kmer):
        """Save in the bloom filter a given kmer"""
        hash_values = self.get_hash_values(kmer)
        for h in hash_values:
            self.array.set_i(h, True)
    
    def exists(self, w):
        """Return True if the kmer is in the bloom filter, else False"""
        hash_values = self.get_hash_values(w)
        for h in hash_values:
            if not self.array.get_i(h):
                return False
        return True
