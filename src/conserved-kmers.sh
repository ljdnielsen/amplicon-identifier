files=($(ls sorted-kmers/*.txt | sort))  # Store all sorted k-mer files in an array

cp "${files[0]}" conserved_kmers.txt  # Start with the first file

for file in "${files[@]:1}"; do
    comm -12 conserved_kmers.txt "$file" > temp.txt
    mv temp.txt conserved_kmers.txt
done