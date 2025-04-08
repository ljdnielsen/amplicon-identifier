#!/bin/bash

# Input arguments
MITOGENOME_FASTA="$1"  # Directory containing the mitogenome FASTA files

# Format the effective primer pairs for use with in_silico_PCR
python3 src/format-effective-primer-pairs-for-in_silico_PCR.py results/in_silico_PCR/amplifications.tsv results/in_silico_PCR/primer_pairs.tsv results/in_silico_PCR/effective_primer_pairs.tsv

# Run in_silico_PCR with the effective set of primers on the full set of mitogenomes
in_silico_PCR.pl -s "$MITOGENOME_FASTA" -p results/in_silico_PCR/effective_primer_pairs.tsv -l 500 > results/in_silico_PCR/amplicons_full.tsv 2> results/in_silico_PCR/amplicons_full.fasta

# Split amplicons by primer pair
python3 src/split-amplicons-by-primer-pair.py results/in_silico_PCR/amplicons_full.tsv results/in_silico_PCR/amplicons_full.fasta results/fasttree/amplicons