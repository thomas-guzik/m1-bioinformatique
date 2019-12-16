from BloomFilter import BloomFilter

if __name__ == '__main__': #Some tests
    import random
    import time

    N = 10000000
    BF = BloomFilter(N, 7)

    kmers = [''.join([random.choice('ACGT') for _ in range(15)]) for _ in range(500000)]
    kmers_to_add = kmers[:len(kmers)-1000]
    kmers_to_test = kmers[len(kmers_to_add):]

    for kmer in kmers_to_add:
        BF.add(kmer)

    false_neg = 0
    for kmer in kmers_to_add:
        if not kmer in BF: false_neg += 1
    assert false_neg == 0

    false_pos = 0
    for kmer in kmers_to_test:
        if kmer in BF: false_pos += 1
    print(f'FP = {false_pos}')
