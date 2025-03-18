kmer_size=$1

# Index kmers of each mitogenome
for filename in $2/*; do
    prefix=$(basename -- "${filename%.*}")
    echo indexing kmers of $prefix
    jellyfish count -m $kmer_size -s 100M -o kmers-by-species/$prefix.kmers.jf ~/data/mitogenomes/set_1/$prefix.fasta
    jellyfish dump -c kmers-by-species/$prefix.kmers.jf > kmers-by-species/$prefix.kmers.txt
done

# Sort the kmer lists
for filename in $2/*; do
    prefix=$(basename -- "${filename%.*}")
    echo sorting kmers of $prefix
    sort kmers-by-species/$prefix.kmers.txt > sorted-kmers/sorted.$prefix.kmers.txt
done