#!/usr/bin/python


import os, subprocess

#Recover GenBank summaries for a sequence given its accession number

with open("assembly_accessions_unique.csv", "r") as f:

    accessions = f.readlines()

f.close()

os.mkdir("genbank")

for accession in accessions:

    acc = accession.strip()

    outfile = acc + ".gb"

    command = "efetch -db nuccore -id " + acc + " -format gb > genbank/" + outfile

    subprocess.run(command, shell = True)

    print(acc,"done!")

