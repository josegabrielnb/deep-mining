#!/usr/bin/python

import argparse
import os, subprocess, re
import pandas as pd
import numpy as np
import networkx as nx

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--flank_size')
parser.add_argument('--coverage_threshold')
args = parser.parse_args()

#Read file with sequence accession and coordinates

with open(args.file, 'r') as f:

    lines = f.readlines()

f.close()

#Create dictionary with coodinates information

seqs = {}

for line in lines:

    data = line.split(',')

    start = int(data[1])
    end = int(data[2])
    accession = data[0] + "_" + str(start) + "_" + str(end)

    seqs[accession] = (int(start),int(end))

#Extract upstream and downstream flank coordinates

flanks = {}

for accession in seqs.keys():

    flank_size = int(args.flank_size) #set flank size

    flank_1 = accession + '_up'
    start_1 = max(1,seqs[accession][0] - flank_size)
    flanks[flank_1] = (start_1, seqs[accession][0])

    flank_2 = accession + '_down'
    end_2 = seqs[accession][1] + flank_size
    flanks[flank_2] = (seqs[accession][1], end_2)

#print(flanks)

#print(flanks)
print("Analysing orthology for %s sequences (%s flanks)" % (len(seqs.keys()), len(flanks.keys())))

os.mkdir("fastas")
os.chdir("fastas")

#Fetch all sequences

for accession in flanks.keys():

    if accession.endswith("_up"):

        acc = re.sub(r'_[0-9]+_[0-9]+_up$', "", accession)

        efetch_command = "efetch -db nuccore -format fasta -id " + acc + " -seq_start " + str(flanks[accession][0]) + " -seq_stop " + \
                            str(flanks[accession][1]) + " > " + accession + ".fasta" 

        subprocess.run(efetch_command, shell = True)

        sed_command = "sed -i 's/>.*/>" + accession + "/' " + accession + ".fasta"

        subprocess.run(sed_command, shell=True)

        #print(efetch_command)

    elif accession.endswith("_down"):

        acc = re.sub(r'_[0-9]+_[0-9]+_down$', "", accession)

        efetch_command = "efetch -db nuccore -format fasta -id " + acc + " -seq_start " + str(flanks[accession][0]) + " -seq_stop " + \
                            str(flanks[accession][1]) + " > " + accession + ".fasta" 

        subprocess.run(efetch_command, shell = True)

        sed_command = "sed -i 's/>.*/>" + accession + "/' " + accession + ".fasta"

        subprocess.run(sed_command, shell=True)

        #print(efetch_command)

#Join all sequences into one file

join_command = "cat *.fasta > all_flanks.fasta"

subprocess.run(join_command, shell=True)

os.chdir("..")

#Blast flanks against each other (all against all blast)

os.mkdir("blastdb")
os.chdir("blastdb")

makeblastdb_command = "mv ../fastas/all_flanks.fasta . && makeblastdb -in all_flanks.fasta -dbtype nucl -parse_seqids"

subprocess.run(makeblastdb_command, shell = True)

blastn_command = 'blastn -task blastn -query all_flanks.fasta -db all_flanks.fasta -evalue 1e-5 -outfmt "6 delim=, qacc sacc qcovs pident evalue" \
                    > blastn_results.csv'

subprocess.run(blastn_command, shell = True)

os.chdir("..")

#Create data frame and initialise with zeroes

df = pd.DataFrame(0, index=list(flanks.keys()), columns=list(flanks.keys()))

#Populate matches from blast results

with open("blastdb/blastn_results.csv", "r") as g:

    results = g.readlines()

f.close()

coverage_threshold = int(args.coverage_threshold) #70

for line in results:

    data = line.split(',')

    seq1 = data[0]
    seq2 = data[1]
    qcovs = int(data[2])

    if seq1 != seq2:

        if qcovs >= coverage_threshold:

            df[seq1][seq2] = 1

#print(df)
df.to_csv('df.csv', index=True)

row_names = df.index.values.tolist()
col_names = list(df.columns)

#print(row_names)
#print(col_names)

row_names_unique = list(set([re.sub(r'_up$|_down$', "", name) for name in row_names]))
col_names_unique = list(set([re.sub(r'_up$|_down$', "", name) for name in col_names]))
#print(row_names_unique)
#print(col_names_unique)

#Extract 2x2 pairwise comparisons to infer orthology clusters

#initialise zero-matrix to record results

df2 = pd.DataFrame(0, index=row_names_unique, columns=col_names_unique)

#Create orthology adjacency matrix

for i in row_names_unique:

    for j in col_names_unique:

        name_i_up = i + "_up"
        name_i_down = i + "_down"

        name_j_up = j + "_up"
        name_j_down = j + "_down"

        test_df = df.filter(items=[name_j_up, name_j_down]).loc[[name_i_up, name_i_down]]

        if np.sum(test_df.values) > 1: # > 0 less strict, > 1 more strict

            df2[i][j] = 1

        #print(test_df)
        #print(np.sum(test_df.values))

print(df2)
print()

#Create graph from adjacency matrix

G = nx.from_pandas_adjacency(df2)

G.name = "Graph from orthology adjacency matrix"

print(G)
print()

components = list(nx.connected_components(G))

print(components)
print()

n = 1

for component in components:

    print("Orthogroup %s: %s" % (str(n), component))

    n += 1
 
