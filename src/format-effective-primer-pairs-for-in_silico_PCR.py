import argparse

def process_primers(amplifications_file, primer_pairs_file, output_file):
    # Load the amplifications file into a dictionary
    amplifications = {}
    with open(amplifications_file, "r") as amp_file:
        next(amp_file)  # Skip header
        for line in amp_file:
            parts = line.strip().split("\t")
            if len(parts) < 4:
                continue
            amp_id = parts[0].replace("_amp_1", "")  # Remove "_amp_1" from AmpId
            length = parts[3]  # Amplification product length
            amplifications[amp_id] = length

    # Load the primer pairs into a dictionary
    primer_pairs = {}
    with open(primer_pairs_file, "r") as primer_file:
        for line in primer_file:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            forward_primer = parts[0]
            reverse_primer = parts[1]
            primer_pair_id = parts[2]
            primer_pairs[primer_pair_id] = (forward_primer, reverse_primer)

    # Generate the output based on matched primer pairs
    output_lines = []
    for primer_id, length in amplifications.items():
        if primer_id in primer_pairs:
            forward, reverse = primer_pairs[primer_id]
            output_lines.append(f"{forward}\t{reverse}\t{primer_id}")

    # Save the output to a new file
    with open(output_file, "w") as out_file:
        out_file.write("\n".join(output_lines))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process primer pair files.")
    parser.add_argument("amplifications_file", help="Path to amplifications.tsv")
    parser.add_argument("primer_pairs_file", help="Path to primer_pairs.tsv")
    parser.add_argument("output_file", help="Path to output file")
    
    args = parser.parse_args()
    process_primers(args.amplifications_file, args.primer_pairs_file, args.output_file)
