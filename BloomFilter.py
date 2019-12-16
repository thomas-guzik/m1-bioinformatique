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
import pickle
import gzip
import sys
from utilis import kmer2hash, canonical, canonical_list
from bit_array import BitArray
from bloom_filter_execption import UnexpectedKmerError, UnexpectedReadError


class BloomFilter:
    
    def __init__(self, array_len, n_hash_fc):
        self.array_len = array_len
        self.array = BitArray(array_len)
        self.seeds = []
        for i in range(n_hash_fc):
            self.seeds.append(random.randint(0, 99999))
    
    def __contains__(self, kmer):
        return self.exists(kmer)
    
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
    
    def import_fasta(self, fasta, kmer_len):
        """Import a fasta object in a bloom filter"""
        for k in fasta.readkmer(kmer_len):
            if not (self.exists(k) or self.exists(canonical(k))):
                print(k)
                self.add(k)
    
    def search_bifurcations(self, read, read_size, kmer_len):
        """Return the bifurcations from the original read"""
        bifurcations = []
        for i in range(1, read_size-kmer_len+1):
            bifurcation = ""
            for l in "ACGT":
                if l != read[i+kmer_len-1]:
                    if(self.exists(read[i:i+kmer_len-1]+l)):
                        bifurcation += l
            if bifurcation != "":
                bifurcations.append(bifurcation)
        return bifurcations
    
    def find_read(self, kmer, read_size, bifurcations):
        """Find a read to complete fasta file"""
        kmer_len = len(kmer)
        read = kmer
        kmer = kmer[1:]
        for i in range(read_size-kmer_len):
            print(i)
            bifurcation = ""
            for l in "ACGT":
                if self.exists(kmer+l):
                    bifurcation += l
                    print(kmer+l)
                    print(l)
            print(bifurcation)
            if len(bifurcation) == 1:
                read += bifurcation
                kmer = kmer[1:]+ bifurcation
            elif len(bifurcation) > 1:
                bifurcation.replace(bifurcations[0], "")
                bifurcations = bifurcations[1:]
                read += bifurcation
                kmer = kmer[1:]+ bifurcation
            else:
                print(read, file=sys.stderr)
                print(bifurcation)
                raise UnexpectedReadError("Can not recreate the read")
        return read
        
    
    def export_to_comp(self, fasta, output, kmer_len):
        """Export to comp file"""
        with open(output, "w") as f:
            f.write(str(fasta.read_size)+"\n")
            for l in fasta.readlines():
                f.write(l[0:kmer_len])
                if(self.exists(l[0:kmer_len])):
                    bifurcations = self.search_bifurcations(l, fasta.read_size, kmer_len)
                    if bifurcations:
                        f.write(" "+' '.join(bifurcations))
                elif(self.exists(canonical(l[0:kmer_len]))):
                    bifurcations = self.search_bifurcations(canonical(l), fasta.read_size, kmer_len)
                    if bifurcations:
                        f.write(" "+' '.join(canonical_list(bifurcations)))
                f.write("\n")
    
    def export_to_pgz(self, output):
        """Pickle the bloom filter"""
        with gzip.open(output, 'wb') as f:
            pickler = pickle.Pickler(f)
            pickler.dump(self)
    
    def export_to_fasta(self, output, comp):
        """Export to fasta file"""
        with open(output, "w") as f:
            for i, l in enumerate(comp.readlines()):
                f.write(">read "+str(i)+"\n")
                if len(l) > 1:
                    bifurcations = l[1:]
                else:
                    bifurcations = []
                
                if self.exists(l[0]):
                    f.write(self.find_read(l[0], comp.read_size, bifurcations))
                elif self.exists(canonical(l[0])):
                    f.write(canonical(self.find_read(l[0], comp.read_size, bifurcations)))
                else:
                    raise UnexpectedKmerError("The kmer {} from the comp file can not be found in bloom filter".format(l[0]))
                f.write("\n")
                
