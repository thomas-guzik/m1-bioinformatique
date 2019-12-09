# !/usr/bin/python
# -*- coding: utf-8 -*-
""" Provide some useful functions"""
import mmh3


def canonical(kmer):
    """Return the canonical sequence for a given kmer"""
    for i in range(kmer):
        if kmer[i] == "A":
            kmer[i] = "T"
        elif kmer[i] == "G":
            kmer[i] = "C"
        elif kmer[i] == "C":
            kmer[i] = "G"
        elif kmer[i] == "T":
            kmer[i] = "A"
    return kmer


def kmer2hash(kmer, seed, limit):
    """Hash a given kmer between 0 and the limit"""
    return mmh3.hash(kmer, seed=seed, signed=False) % limit
