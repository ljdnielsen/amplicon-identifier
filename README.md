# amplicon-identifier
A tool for finding primers for amplicon sequencing metataxonomics

## Creating a sample dataset of mitogenomes

The same list of mitogenomes that were used for the initial iteration of the fat-tailed dunnart eDNA assay were also used here. The genome, their species' of origin, and identifiers are listed in the table below.

### List of mitogenomes

__Table 1__: Mitochondrial genomes of common contaminants, as well as a marsupial species of the same and a different order, thylacine and swamp wallaby respectively, were downloaded from the NCBI RefSeq or Genbank database.
|Species                     |RefSeq            |Genbank   |
|----------------------------|------------------|----------|
|*Sminthopsis crassicaudata* |NC_007631.1       |          |
|*Homo sapiens*              |NC_012920.1       |          |
|*Sus scrofa*                |NC_000845.1       |          |
|*Gallus gallus*             |NC_053523.1       |          |
|*Bos taurus*                |NC_006853.1       |          |
|*Wallabia bicolor*          |                  |KY996500.1|
|*Thylacinus cynocephalus*    |NC_011944.1       |          |

The data is saved in data/mitogenomes/set_1 of the LANIEL home directory on WSL of Lasse's Lenovo Laptop.

## Identifying conserved kmers using Jellyfish

### Install jellyfish

Install jellyfish in a seperate conda environment:

~~~
conda create --name jellyfish
conda activate jellyfish
conda install -c bioconda jellyfish
~~~

### Identify conserved kmers across mitogenome set

__Obtain all kmers__

The script src/sort-kmers.sh takes as input the requested kmer size and mitogenome folder and writes all the kmers to individual files for each species

Run the script from the results/jellyfish folder with:

~~~
bash ../../src/sort-kmers.sh 15 ~/data/mitogenomes/set_1
~~~

__Identify conserved kmers__

The script src/conserved-kmers.sh isolates kmers found in all the species and saves them to the file conserved_kmers.txt. Run it from the results/jellyfish folder.

~~~
bash ../../src/conserved-kmers.sh
~~~



