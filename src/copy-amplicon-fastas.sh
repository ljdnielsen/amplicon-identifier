#!/bin/bash

for dir in results/ribdif2/set_1/amplicons/*
do
    primer_pair="${dir##*/}"
    cp results/ribdif2/set_1/amplicons/$primer_pair/set_1-$primer_pair.amplicons results/fasttree/amplicons/set_1-$primer_pair.amplicons.fasta
done