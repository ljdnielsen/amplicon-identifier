#!/bin/bash

# Check input arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <mitogenome_fasta> <amplicon_folder> <output_folder>"
    exit 1
fi

# Assign input variables
MITOGENOME_FASTA="$1"
AMPLICON_FOLDER="$2"
OUTPUT_FOLDER="$3"

# Create required directories after assigning $OUTPUT_FOLDER
mkdir -p "$OUTPUT_FOLDER/alignments"
mkdir -p "$OUTPUT_FOLDER/amplicon_trees"

# Generate aligned mitogenome sequences
mitogenome_aligned="$OUTPUT_FOLDER/alignments/mitogenome_aligned.fasta"
mafft --auto "$MITOGENOME_FASTA" > "$mitogenome_aligned"
echo "Aligned mitogenome sequences: $mitogenome_aligned"

# Generate full mitogenome tree
fasttree -nt "$mitogenome_aligned" > "$OUTPUT_FOLDER/mitogenome_tree.nwk"
echo "Generated tree: $OUTPUT_FOLDER/mitogenome_tree.nwk"

# Process each amplicon file
for file in "$AMPLICON_FOLDER"/*.fasta; do
    if [ -f "$file" ]; then
        # Align the amplicon sequences
        aligned_amplicon="$OUTPUT_FOLDER/alignments/$(basename "${file%.fasta}_aligned.fasta")"
        mafft --auto "$file" > "$aligned_amplicon"
        echo "Aligned amplicon: $aligned_amplicon"

        # Generate the tree
        output_tree="$OUTPUT_FOLDER/amplicon_trees/$(basename "${file%.fasta}_tree.nwk")"
        fasttree -nt "$aligned_amplicon" > "$output_tree"
        echo "Generated tree: $output_tree"
    fi
done
