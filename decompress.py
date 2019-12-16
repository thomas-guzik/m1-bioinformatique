
import argparse
import gzip
import pickle
from comp import Comp

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--comp-file", type=str, required=True,
                    help="File name of the input file with comp compression")
parser.add_argument("-g", "--graph", type=str, required=True,
                    help="File name of the input file with pgz compression")
parser.add_argument("-o", "--output", nargs="?", const=True,
                    help="File name of the fasta output file")

args = parser.parse_args()

output = ""
if (not args.output) or args.output is True:
    output = args.comp_file+".fasta" 
else:
    output = args.output

comp = Comp(args.comp_file)

with gzip.open(args.graph, "rb") as fichier:
    unpickler = pickle.Unpickler(fichier)
    bloom_filter = unpickler.load()
    bloom_filter.export_to_fasta(output, comp)
