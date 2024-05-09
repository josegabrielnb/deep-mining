#!/usr/bin/python

import os
from Bio import SeqIO

for folder in os.listdir('.'):

    if folder.startswith('Parvo'): #Change to measure ORF lengths in different family: Borna, Chu, Circo, Filo, Parvo

        os.chdir(folder)

        for file in os.listdir('.'):

            if file.endswith("curated.fasta"):

                with open(file) as handle:

                    for record in SeqIO.parse(handle, "fasta"):

                        print(folder, record.id, len(record.seq)/3, sep = ",")

        os.chdir('..')