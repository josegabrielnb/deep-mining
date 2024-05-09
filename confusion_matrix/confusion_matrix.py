#!/usr/bin/python

import pandas as pd
import random

"""df = pd.read_table('diamond_results.txt',sep='\t',header=None)

df_reduced = df.iloc[:,[0,9]] #Select sequence label and superkingdom columns

df_reduced = df_reduced.rename(columns={0: 'seq_label', 9: 'class'}) #Rename columns for clarity

results = {}

for i in range(0,len(df_reduced)):

    print(i)

    label = df_reduced.iloc[i,:]["seq_label"]

    if label not in results.keys():

        if "Virus" in str(df_reduced.iloc[i,:]["class"]):

            results[label] = [1, 1] #[virus hits, total hits]

        else:

            results[label] = [0, 1] #[virus hits, total hits]

    else:

        if "Virus" in str(df_reduced.iloc[i,:]["class"]):

            results[label][0] += 1
            results[label][1] += 1

        else:

            results[label][1] += 1

for my_key in results.keys():

    percentage_virus = round(float(results[my_key][0])/float(results[my_key][1]),2)

    with open('percentages.tsv','a+') as f:

        print(my_key, percentage_virus, sep="\t",file=f)

    f.close()"""

df_results = pd.read_table('percentages.tsv',sep='\t',header=None)

df_results = df_results.rename(columns={0: 'seq_label', 1: 'perc'})

df_viruses = df_results.query('perc >= 0.50')

df_host = df_results.query('perc < 0.50')

def write_sample(sample,category,number):

    for i in sample:

        file = category + "_sample_" + str(number) + '.txt'

        with open(file,'a+') as f:

            print(i, file=f)

        f.close()

above_or_equal_fifty = list(df_viruses["seq_label"])

#Virus sample 1
random.seed(1)

virus_sample_1 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_1, 'virus', 1)

#Virus sample 2
random.seed(2)

virus_sample_2 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_2, 'virus', 2)

#Virus sample 3
random.seed(3)

virus_sample_3 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_3, 'virus', 3)

#Virus sample 4
random.seed(4)

virus_sample_4 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_4, 'virus', 4)

#Virus sample 5
random.seed(5)

virus_sample_5 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_5, 'virus', 5)

#Virus sample 6
random.seed(6)

virus_sample_6 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_6, 'virus', 6)

#Virus sample 7
random.seed(7)

virus_sample_7 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_7, 'virus', 7)

#Virus sample 8
random.seed(8)

virus_sample_8 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_8, 'virus', 8)

#Virus sample 9
random.seed(9)

virus_sample_9 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_9, 'virus', 9)

#Virus sample 10
random.seed(10)

virus_sample_10 = random.sample(above_or_equal_fifty, 50)
write_sample(virus_sample_10, 'virus', 10)

below_fifty = list(df_host["seq_label"])

#Host sample 1
random.seed(1)

host_sample_1 = random.sample(below_fifty, 50)
write_sample(host_sample_1, 'host', 1)

#Host sample 2
random.seed(2)

host_sample_2 = random.sample(below_fifty, 50)
write_sample(host_sample_2, 'host', 2)

#Host sample 3
random.seed(3)

host_sample_3 = random.sample(below_fifty, 50)
write_sample(host_sample_3, 'host', 3)

#Host sample 4
random.seed(4)

host_sample_4 = random.sample(below_fifty, 50)
write_sample(host_sample_4, 'host', 4)

#Host sample 5
random.seed(5)

host_sample_5 = random.sample(below_fifty, 50)
write_sample(host_sample_5, 'host', 5)

#Host sample 6
random.seed(6)

host_sample_6 = random.sample(below_fifty, 50)
write_sample(host_sample_6, 'host', 6)

#Host sample 7
random.seed(7)

host_sample_7 = random.sample(below_fifty, 50)
write_sample(host_sample_7, 'host', 7)

#Host sample 8
random.seed(8)

host_sample_8 = random.sample(below_fifty, 50)
write_sample(host_sample_8, 'host', 8)

#Host sample 9
random.seed(9)

host_sample_9 = random.sample(below_fifty, 50)
write_sample(host_sample_9, 'host', 9)

#Host sample 10
random.seed(10)

host_sample_10 = random.sample(below_fifty, 50)
write_sample(host_sample_10, 'host', 10)