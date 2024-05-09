#!/usr/bin/python

#Parse orthologue list

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--flank_size')
args = parser.parse_args()

command1 = "cat " + args.file + " | sed 's/,//g' | sed 's/{//g' | sed 's/}//g' | sed \"s/'//g\" | tr \" \" \"\\n\" | sed -E 's/_([0-9]*)_([0-9])/\\t\\1\\t\\2/g' | xargs -l bash -c 'efetch -db nuccore -format fasta -id $0 -seq_start $1 -seq_stop $2' > eve_loci.fasta"

#print(command1)
subprocess.run(command1, shell = True)

#Download EVE fasta sequences using efetch


#Diamond against RVDB to find query strand

command2 = "diamond blastx --db /home/user/Desktop/hi-fever/data/nr_clustered_wtaxa.dmnd --query eve_loci.fasta -e 1e-1 --outfmt 6 qseqid sseqid evalue qstrand | awk '{print $1, $4}' | uniq > sequence_strands.txt"
#command2 = "diamond blastx --db /home/user/Desktop/JoseGabriel/Manuscript/Orthology/curation/circo.dmnd --query eve_loci.fasta -e 1e-1 --outfmt 6 qseqid sseqid evalue qstrand | awk '{print $1, $4}' | uniq > sequence_strands.txt"
#command2 = "diamond blastx --db /home/user/Desktop/JoseGabriel/Manuscript/Orthology/curation/RVDB/rvdbv26_clustered.dmnd --query eve_loci.fasta -e 1e-1 --outfmt 6 qseqid sseqid evalue qstrand | awk '{print $1, $4}' | uniq > sequence_strands.txt"
#command2 = "diamond blastx --db Borna_G.dmnd --query eve_loci.fasta -e 10 --outfmt 6 qseqid sseqid evalue qstrand | awk '{print $1, $4}' | uniq > sequence_strands.txt"

#print(command2)
subprocess.run(command2, shell = True)

#Compute new coordinates based on flank size

with open("sequence_strands.txt", "r") as f:

    seqs = f.readlines()

f.close()

flank_size = int(args.flank_size)

exists_list = []

for seq in seqs:

    data = seq.strip().split(" ")

    exists_list.append(data[0])

    accession = data[0].split(":")[0]
    coords = data[0].split(":")[1].split("-")
    start = coords[0]
    end = coords[1]

    start_new = str(int(start) - flank_size)
    end_new = str(int(end) + flank_size)

    strand = data[1]

    #Download sense sequences for each orthologue candidate (ready for alignment)

    if strand == "+":

        command3 = "efetch -db nuccore -format fasta -id " + accession + " -seq_start " + start_new + " -seq_stop " + end_new + " -strand " + "plus >> curated_seqs.fasta"
        
        #print(command3)
        subprocess.run(command3, shell = True)

    elif strand == "-":

        command4 = "efetch -db nuccore -format fasta -id " + accession + " -seq_start " + start_new + " -seq_stop " + end_new + " -strand " + "minus >> curated_seqs.fasta"
        
        #print(command4)
        subprocess.run(command4, shell = True)

#Check for missing sequences

command5 = "cat " + args.file + " | sed 's/,//g' | sed 's/{//g' | sed 's/}//g' | sed \"s/'//g\" | tr \" \" \"\\n\" | sed -E 's/_([0-9]*)_([0-9])/\\t\\1\\t\\2/g' | awk '{print $1\":\"$2\"-\"$3}' > accession_list.txt"

subprocess.run(command5, shell = True)

with open("accession_list.txt", 'r') as f:

    lines = f.readlines()

f.close()

for line in lines:

    acc_id = line.strip()

    if acc_id not in exists_list:

        with open('missing.log', 'a+') as f:

            print(acc_id, file=f)



