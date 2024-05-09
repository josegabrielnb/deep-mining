#!/usr/bin/python

import os, re

#Script to get the assembly accessions, names and providers from genbank files

entries = []

for file in os.listdir("genbank"):

    if file.endswith(".gb"):

        path = "genbank/" + file

        with open(path, "r") as f:

            lines = f.readlines()

        f.close()

        info = {'assembly': '','bioproject': '', 'biosample': '', 'organism':''}

        for line in lines:

            if "Assembly: " in line:

                accession = re.search(r'Assembly: (.+)', line)

                info['assembly'] = accession.group(1)

            if "BioProject: " in line:

                bioproject = re.search(r'BioProject: (.+)', line)

                info['bioproject'] = bioproject.group(1)

            if "BioSample: " in line:

                biosample = re.search(r'BioSample: (.+)', line)

                info['biosample'] = biosample.group(1)

            if "ORGANISM" in line:

                organism = re.search(r'ORGANISM\s+(.+)', line)

                info['organism'] = organism.group(1)

        if info not in entries:

            entries.append(info)

for entry in entries:

    print(entry['organism'], entry['assembly'], entry['bioproject'], entry['biosample'], sep = ',')




