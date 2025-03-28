input_dir=$1

files=($(ls $input_dir/sorted-kmers/*.txt | sort))  # Store all sorted k-mer files in an array

cp "${files[0]}" $input_dir/conserved_kmers_temp.txt  # Start with the first file

# Identify conserved kmers
for file in "${files[@]:1}"; do
    comm -12 $input_dir/conserved_kmers_temp.txt "$file" > $input_dir/temp.txt
    mv $input_dir/temp.txt $input_dir/conserved_kmers_temp.txt
done

# Remove the count column from the file

awk '!($2="")' $input_dir/conserved_kmers_temp.txt > $input_dir/conserved_kmers.txt
rm $input_dir/conserved_kmers_temp.txt