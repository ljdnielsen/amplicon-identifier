#!/bin/bash

# Input arguments
MITOGENOME_DIR="$1"  # Directory containing the mitogenome FASTA files
REFERENCE_GENOME="$2"       # Reference genome

# Initialize k-mer length
K=20

while [ $K -ge 1 ]; do
    echo "Trying k-mer length: $K"

    # Run sort_kmers.sh on the mitogenome FASTA files
    src/sort-kmers.sh "$K" "$MITOGENOME_DIR" results/jellyfish

    # Find conserved k-mers
    src/find-conserved-kmers.sh results/jellyfish

    # Run combine-primers.py
    python3 src/combine-primers.py results/jellyfish/conserved_kmers.txt > results/in_silico_PCR/primer_pairs.tsv

    # Run in_silico_PCR.pl
    { exec in_silico_PCR.pl -s "$REFERENCE_GENOME" -p results/in_silico_PCR/primer_pairs.tsv -l 500 | sed '/No amplification/d' | sed '/>/d' > results/in_silico_PCR/amplifications.tsv; } 2>/dev/null

    # Check if any of the amplification products is more than 200 bp
    if [ $(awk -F'\t' 'BEGIN {max = 0} $4 ~ /^[0-9]+$/ {if ($4 > max) max=$4} END {print max}' results/in_silico_PCR/amplifications.tsv) -gt 200 ]; then
        echo "Success! Found valid k-mer length: $K"
        break
    else
        # Decrement k-mer length
        ((K--))
    fi
    
done
