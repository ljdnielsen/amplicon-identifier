import pandas as pd
from Bio import SeqIO
import os
import argparse

def create_primer_pair_fastas(tsv_file, fasta_file, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the TSV file
    df = pd.read_csv(tsv_file, sep='\t')
    
    # Parse the FASTA file into a dictionary
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences[record.id] = str(record.seq)
    
    # Group sequences by primer pair (extracted from AmpId)
    df['PrimerPair'] = df['AmpId'].str.extract(r'(primer_pair\d+)')
    primer_groups = df.groupby('PrimerPair')
    
    # Create a FASTA file for each primer pair
    for primer_pair, group in primer_groups:
        output_file = os.path.join(output_dir, f"{primer_pair}.amplicons.fasta")
        
        with open(output_file, 'w') as f:
            for _, row in group.iterrows():
                amp_id = row['AmpId']
                seq_id = row['SequenceId']
                if amp_id in sequences:
                    f.write(f">{seq_id}\n")
                    f.write(f"{sequences[amp_id]}\n")
                else:
                    print(f"Warning: Sequence {amp_id} not found in FASTA file")
    
    print(f"Created {len(primer_groups)} FASTA files in {output_dir}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Split amplicon sequences into FASTA files by primer pair"
    )
    parser.add_argument(
        "tsv_file",
        help="Path to the amplicons_full.tsv file"
    )
    parser.add_argument(
        "fasta_file",
        help="Path to the amplicons_full.fasta file"
    )
    parser.add_argument(
        "output_dir",
        help="Directory where output FASTA files will be saved"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the function with provided arguments
    create_primer_pair_fastas(args.tsv_file, args.fasta_file, args.output_dir)

if __name__ == "__main__":
    main()