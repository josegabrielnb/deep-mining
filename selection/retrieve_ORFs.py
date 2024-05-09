#!/usr/bin/python

#Read genomic coordinates file

import argparse
import subprocess
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('--file')

args = parser.parse_args()

with open(args.file,'r') as f:

    lines = f.readlines()

f.close()


fasta_file = args.file.replace(".txt", "_genomic.fasta")


def efetch_command(acc, start, end, strand, outfile):

    command = "efetch -db nuccore -format fasta -id " + acc + " -seq_start " + start + " -seq_stop " + end + " -strand " + strand + " >> " + fasta_file

    return command


for line in lines:

    data = line.strip().split(':')

    accession = data[0]

    coords = data[1]

    if "c" in coords:

        numeric = coords.replace("c","").split("-")

        start = int(numeric[1]) + 4400

        end = int(numeric[0]) - 4400

        command1 = efetch_command(accession, str(start), str(end), "minus", fasta_file)

        subprocess.run(command1, shell = True)

        print(accession, "c" + str(end) + "-" + str(start))

    else:

        numeric = coords.split("-")

        start = int(numeric[0]) + 4400

        end = int(numeric[1]) - 4400

        command2 = efetch_command(accession, str(start), str(end), "plus", fasta_file)

        subprocess.run(command2, shell = True)

        print(accession, str(start) + "-" + str(end))

command3 = "sed 's/:/@/g' *_genomic.fasta > curated_labels_genomic.fasta"

subprocess.run(command3, shell = True)

command4 = "getorf -sequence curated_labels_genomic.fasta -outseq " + fasta_file.replace("_genomic.fasta","_nt_ORFs.fasta") + " -minsize 300 -find 3 -reverse N"

subprocess.run(command4, shell = True)

command5 = """awk '{if($0~">") print $1","$2","$4","$5"_"$6}' *_nt* | sed 's/\[//g' | sed 's/\]//g' > patterns.csv"""

subprocess.run(command5, shell = True)

if os.stat("patterns.csv").st_size != 0:

    with open("patterns.csv", 'r') as f:

        lines = f.readlines()

    f.close()
        
    for line in lines:

        data = line.strip().split(",")

        species = data[3]

        shift1 = int(data[1])

        shift2 = int(data[2])

        accession = data[0].split("@")[0].replace(">","")

        if "@c" in data[0]:

            start = data[0].split("@c")[1].split("-")[0]

            start2 = int(start) - shift1 + 1

            end2 = int(start) - shift2 + 1

            with open("pattern_replace.txt", "a+") as f:

                print(data[0], ">" + species + "@" + accession + ":c" + str(start2) + "-" + str(end2), file = f)

        else:

            start = data[0].split("@")[1].split("-")[0]

            start2 = int(start) + shift1 - 1

            end2 = int(start) + shift2 - 1

            with open("pattern_replace.txt", "a+") as f:

                print(data[0], ">" + species + "@" + accession + ":" + str(start2) + "-" + str(end2), file = f)

        f.close()

command6 = """cat pattern_replace.txt | xargs -n2 bash -c 'sed -i s/$0/$1/g *nt*'"""

subprocess.run(command6, shell = True)

command7 = "awk '{print $1}' *nt* > " + fasta_file.replace("_genomic.fasta","_nt_ORFs_clean.fasta")

subprocess.run(command7, shell = True)

os.mkdir("files")

command8 = "mv *ORFs.fasta files; mv *_genomic.fasta files; mv patterns.csv files; mv *replace.txt files"

subprocess.run(command8, shell = True)