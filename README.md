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

The script src/find-conserved-kmers.sh isolates kmers found in all the species and saves them to the file conserved_kmers.txt. Run it from the results/jellyfish folder.

~~~
bash ../../src/find-conserved-kmers.sh
~~~

The conserved sequences were saved to the file [results/jellyfish/conserved_kmers.txt](results/jellyfish/conserved_kmers.txt).

## Filtering for effective primer pairs

### Isolating effective primer pairs with in_silico_PCR

Next, we identified potential amplification products from using the conserved sequences as primer binding sites.

This was done using [in_silico_pcr](https://github.com/egonozer/in_silico_pcr) which simply extracts sequences surounded by the primer binding sites, and setting the maximum length of the product to 500 bp.

__Installing in_silico_PCR__

To make in_silico_pcr executable from the command line the folder it was cloned to was added to PATH in the ~/.bashrc script,

~~~
export PATH=/home/laniel/tools:${PATH}
~~~

and the following command was run,

~~~
chmod +x ~/tools/bioinformatics/in_silico_pcr/in_silico_PCR.pl
~~~

__Test run of in_silico_PCR__

The program was run from the results/in_silico_PCR folder.

As an initial test conserved sequence 5 was run with the reverse complement of conserved sequence 3.

~~~
in_silico_PCR.pl -s ~/data/mitogenomes/set_1/sminthopsis-crassicaudata.fasta -a CAAACTGGGATTAGA -b AGGGTGACGGGCGGT -l 500
~~~

This resulted in a 433 bp in silico amplification product.

__Python script for combining all primers__

The script [combine-primers.py](src/combine-primers.py) was written to create a table of two columns pairing every conserved kmer with the reverse complement of every other kmer.

A tsv file with all primer pairs were generated with the following command:

~~~
python3 src/combine-primers.py results/jellyfish/conserved_kmers.txt > results/in_silico_PCR/primer_pairs.tsv
~~~

__Identifying primer pairs that give amplification products with in_silico_PCR__

in_silico_PCR was run from the results/in_silico_PCR folder on all primer pairs with the following command:

~~~
in_silico_PCR.pl -s ~/data/mitogenomes/set_1/sminthopsis-crassicaudata.fasta -p primer_pairs.tsv -l 500 | sed '/No amplification/d' | sed '/>/d' > amplifications.tsv
~~~

The primer pairs that gave amplifications were saved along with their name and product length to effective_primer_pairs.tsv with the python script [format-effective-primer-pairs-for-ribdif.py]().

~~~
python3 src/format-effective-primer-pairs-for-ribdif.py results/in_silico_PCR/amplifications.tsv results/in_silico_PCR/primer_pairs.tsv results/ribdif2/effective_primer_pairs.tsv
~~~

## Determining amplicon species resolution with RibDif2

RibDif2 was run on the set of mitogenomes specified with the primers identified in the previous step.

~~~
ribdif -u ~/data/mitogenomes/set_1 -p results/ribdif2/effective_primer_pairs.tsv
~~~

## Comparing tree topologies of amplicons with mitogenomes

__Move amplicon fastas to fastree folder__

First the fasta files with the resulting amplicons of each primer pair was moved to the folder results/fasttree/amplicons.

This was done by looping through the ribdif2 primer-pair folders and copying the amplicon fastas using the script copy-amplicon-fasta.sh.

~~~
bash src/copy-amplicon-fasta.sh
~~~

__Rename sequence names of amplicon fastas to those of the mitogenomes__

The headers of the amplicon fastas were renamed to match the headers of the mitogenome file using the script src/rename-fasta-headers.py

~~~
python3 src/rename-fasta-headers.py -r ~/data/mitogenomes/set_1.fasta -i results/fasttree/amplicons
~~~

__Create a tree for the mitogenomes and every primer pair__

First fasttree was installed into a new environment.

~~~
conda create -n fasttree
conda activate fasttree
mamba install -c bioconda fasttree
~~~

Then the script generate-trees.sh was used to create phylogenetic trees from the amplicon fastas for each primer pair and the mitogenomes fasta.

~~~
bash src/generate-trees.sh ~/data/mitogenomes/set_1.fasta results/fasttree/amplicons/ results/fasttree
~~~

__Find the amplicon tree with the topology most similar to the mitogenome tree__

To find the primer pair that creates the best amplicons for delineating the focal species their topologies were compared with that of the mitogenome tree using the Robinson-Foulds distance.

This was done using the script src/compare-rf.py.

First an environment with biopython and dendropy was created.

~~~
conda create -n compare-rf
conda activate compare-rf
mamba install -c bioconda dendropy
mamba install -c bioconda biopython
~~~

The tree topologies were then compared with the command:

~~~
python3 src/compare-rf.py results/fasttree/mitogenome_tree.nwk results/fasttree/amplicon_trees/
~~~

### Blasting amplicons against NCBI database

A local version of the NCBI refseq genome database was created in a local data folder to blast the amplicons against.

~~~
cd ~/data/ncbi_refseq
wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/mitochondrion/*.fna.gz
gunzip *.fna.gz
cat *.fna > refseq_mito.fasta
makeblastdb -in refseq_mito.fasta -dbtype nucl -out refseq_mito_db
~~~

Then the amplicons of the best matching tree were blasted against NCBI's refseq genomes database and the result saved to results/blastn/set_1-primer_pair95.blast-hits.txt

~~~
blastn -query results/fasttree/amplicons/set_1-primer_pair95.amplicons.fasta -db ~/data/ncbi_refseq/refseq_mito_db -out results/blastn/set_1-primer_pair95.blast-hits.txt
~~~

