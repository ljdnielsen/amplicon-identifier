#!/usr/bin/env python3
import os
import argparse
from Bio import SeqIO

def rename_fasta_headers(reference_file, input_folder):
    # Load reference headers and species names
    ref_species_to_header = {}
    
    for record in SeqIO.parse(reference_file, "fasta"):
        # Extract species name from header (assuming lowercase for matching)
        for part in record.id.split('_'):
            if part.lower() not in ['nc', 'nr', 'xm', 'xr'] and not part[0].isdigit():
                ref_species_to_header[part.lower()] = record.id
    
    # Process all FASTA files in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.fasta', '.fa', '.fna')):
            filepath = os.path.join(input_folder, filename)
            
            # Create a list to store modified records
            modified_records = []
            modified_count = 0
            
            # Process sequences and rename headers based on species name
            for record in SeqIO.parse(filepath, "fasta"):
                old_id = record.id
                
                # Check if any reference species is in the header
                for species, ref_header in ref_species_to_header.items():
                    if species in record.id.lower():
                        record.id = ref_header
                        record.description = ref_header
                        modified_count += 1
                        break
                
                modified_records.append(record)
            
            # Write the modified records back to the same file
            SeqIO.write(modified_records, filepath, "fasta")
            print(f"Processed {filename}: renamed {modified_count} headers")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename FASTA headers using simple containment check")
    parser.add_argument("-r", "--reference", required=True, help="Reference FASTA file with correct headers")
    parser.add_argument("-i", "--input_folder", required=True, help="Folder containing FASTA files to rename")
    
    args = parser.parse_args()
    rename_fasta_headers(args.reference, args.input_folder)