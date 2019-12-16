# !/usr/bin/python
# -*- coding: utf-8 -*-
""" Provide some useful functions"""
import mmh3
import math


def canonical(kmer):
    """Return the canonical sequence for a given kmer"""
    kmer = list(kmer)
    for i in range(len(kmer)):
        if kmer[i] == "A":
            kmer[i] = "T"
        elif kmer[i] == "G":
            kmer[i] = "C"
        elif kmer[i] == "C":
            kmer[i] = "G"
        elif kmer[i] == "T":
            kmer[i] = "A"
    return ''.join(kmer)

def canonical_list(kmer_list):
    for i in range(len(kmer_list)):
        kmer_list[i] = canonical(kmer_list[i])
    return kmer_list

def kmer2hash(kmer, seed, limit):
    """Hash a given kmer between 0 and the limit"""
    return mmh3.hash(kmer, seed=seed, signed=False) % limit

def calc_optimal_bloom_filter(n_items, proba_false_positive):
    nb_bit = math.ceil((n_items * math.log(proba_false_positive)) / math.log(1 / pow(2, math.log(2))))
    nb_hash_fc = round((nb_bit / n_items) * math.log(2))
    return nb_bit, nb_hash_fc