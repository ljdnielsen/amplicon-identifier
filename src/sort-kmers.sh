kmer_size=$1
mitogenome_dir=$2
output_dir=$3

# Index kmers of each mitogenome
for filename in $mitogenome_dir/*; do
    prefix=$(basename -- "${filename%.*}")
    echo indexing kmers of $prefix
    jellyfish count -m $kmer_size -s 100M -o $output_dir/kmers-by-species/$prefix.kmers.jf $mitogenome_dir/$prefix.fasta
    jellyfish dump -c $output_dir/kmers-by-species/$prefix.kmers.jf > $output_dir/kmers-by-species/$prefix.kmers.txt
done

# Sort the kmer lists
for filename in $mitogenome_dir/*; do
    prefix=$(basename -- "${filename%.*}")
    echo sorting kmers of $prefix
    sort $output_dir/kmers-by-species/$prefix.kmers.txt > $output_dir/sorted-kmers/sorted.$prefix.kmers.txt
done