import argparse

# DNA complement mapping
complement = str.maketrans("ATCGatcg", "TAGCtagc")

def reverse_complement(sequence):
    """Returns the reverse complement of a DNA sequence."""
    return sequence.translate(complement)[::-1]

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate unique pairings and compute the reverse complement of the second sequence.")
parser.add_argument("filename", help="Path to the text file containing sequences")
args = parser.parse_args()

# Read sequences from the specified file
with open(args.filename, "r") as file:
    sequences = [line.strip() for line in file if line.strip()]  # Remove empty lines

# Generate all unique pairings and compute reverse complement for seq2
pairs = [(seq1, reverse_complement(seq2)) for seq1 in sequences for seq2 in sequences if seq1 != seq2]

for i, (seq1, rev_comp_seq2) in enumerate(pairs, start=1):
    print(f"{seq1}\t{rev_comp_seq2}\tprimer_pair{i}")