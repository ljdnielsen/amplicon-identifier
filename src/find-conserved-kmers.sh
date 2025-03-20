files=($(ls sorted-kmers/*.txt | sort))  # Store all sorted k-mer files in an array

cp "${files[0]}" conserved_kmers_temp.txt  # Start with the first file

# Identify conserved kmers
for file in "${files[@]:1}"; do
    comm -12 conserved_kmers_temp.txt "$file" > temp.txt
    mv temp.txt conserved_kmers_temp.txt
done

# Remove the count column from the file

awk '!($2="")' conserved_kmers_temp.txt > conserved_kmers.txt
rm conserved_kmers_temp.txt