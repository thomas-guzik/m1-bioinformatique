#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Compress compresses fasta file in two way : blomm filter and textual"""

import argparse
from BloomFilter import BloomFilter
from utilis import calc_optimal_bloom_filter
from fasta import Fasta
from compress_exception import *

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fasta", type=str, required=True,
                    help="File name of the input file")
parser.add_argument("-o", "--output", nargs="?", const=True,
                    help="Name of the output file with comp compression")
parser.add_argument("-g", "--graph", nargs="?", const=True,
                    help="Name of the output file for pgz compression")

parser.add_argument("-k", "--kmer-size", type=int, required=True,
                    help="The length of kmer")
parser.add_argument("-p", "--proba-false-positive", type=float,
                    help="Probability of false positive")
parser.add_argument("-n", "--bloom-size", type=int,
                    help="Size of bloom filter")
parser.add_argument("-a", "--bloom-hash", type=int,
                    help="Number of hash function")

args = parser.parse_args()

try:
    if args.kmer_size > 31 or args.kmer_size < 1:
        raise KmerSizeError("Kmer size must be an integer between 1 and 32")
    
    if not (args.output or args.graph):
        raise ZeroOutputChoiceError("No output is specify")
    
    output = None
    if args.output is True:
        output = args.fasta+".comp"
    else:
        # Two choice, if the args is     set output = str
        #                         is not     output = None
        output = args.output
    
    graph = None
    if args.graph is True:
        graph = args.fasta+".graph.pgz"
    else:
        graph = args.graph
    
    f = Fasta(args.fasta)
    
    if(args.kmer_size > f.read_size):
        raise KmerSizeError("Kmer size can not be superior than the read size (currently {})".format(f.read_size))
    
    bloom_size, bloom_hash = None, None
    if (args.proba_false_positive and (args.bloom_size or args.bloom_hash)) \
    or (args.bloom_size and args.bloom_hash):
        raise ImpreciseBloomFilterError("Probability of false positive must " +
                                        "be specify or bloom size and bloom " +
                                        "must be specify")
    
    if args.proba_false_positive:
        if args.proba_false_positive < 0.0 or args.proba_false_positive > 1.0:
            raise ProbabilitySizeError("Probability must be between 0 and 1") 
        n_kmer = f.get_nb_kmer(args.kmer_size)
        bloom_size, bloom_hash = calc_optimal_bloom_filter(n_kmer,
                                        args.proba_false_positive)
        print(bloom_size)
    else:
        if args.bloom_size < 1:
            raise BloomFilterSizeError("Bloom filter size must be superior to 0")
        if args.bloom_hash < 1:
            raise BloomHashSizeError("Number of hash functions must be superior to 0")
        bloom_size = args.bloom_size
        bloom_hash = args.bloom_hash
    
    print(bloom_size)
    blomm_filter = BloomFilter(bloom_size, bloom_hash)
    blomm_filter.import_fasta(f, args.kmer_size)
    
    if args.output:
        blomm_filter.export_to_comp(f, output, args.kmer_size)
    
    if args.graph:
        blomm_filter.export_to_pgz(graph)
    
except CompressException as e:
    print(e)
