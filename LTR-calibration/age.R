library(ape)

setwd('~/Desktop/diamond-results/results2.0/Arenaviridae/LTRs/')

m = "TN93"

#Csyrichta2 <- read.FASTA('Csyrichta2_LTRs.fasta', type = "DNA")
#distance2 <- dist.dna(Csyrichta2, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta6 <- read.FASTA('Csyrichta6_LTRs.fasta', type = "DNA")
distance6 <- dist.dna(Csyrichta6, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta9 <- read.FASTA('Csyrichta9_LTRs.fasta', type = "DNA")
distance9 <- dist.dna(Csyrichta9, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta10 <- read.FASTA('Csyrichta10_LTRs.fasta', type = "DNA")
distance10 <- dist.dna(Csyrichta10, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta11 <- read.FASTA('Csyrichta11_LTRs.fasta', type = "DNA")
distance11 <- dist.dna(Csyrichta11, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta12 <- read.FASTA('Csyrichta12_LTRs.fasta', type = "DNA")
distance12 <- dist.dna(Csyrichta12, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta13 <- read.FASTA('Csyrichta13_LTRs.fasta', type = "DNA")
distance13 <- dist.dna(Csyrichta13, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta14 <- read.FASTA('Csyrichta14_LTRs.fasta', type = "DNA")
distance14 <- dist.dna(Csyrichta14, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta15 <- read.FASTA('Csyrichta15_LTRs.fasta', type = "DNA")
distance15 <- dist.dna(Csyrichta15, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta16 <- read.FASTA('Csyrichta16_LTRs.fasta', type = "DNA")
distance16 <- dist.dna(Csyrichta16, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta17 <- read.FASTA('Csyrichta17_LTRs.fasta', type = "DNA")
distance17 <- dist.dna(Csyrichta17, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta18 <- read.FASTA('Csyrichta18_LTRs.fasta', type = "DNA")
distance18 <- dist.dna(Csyrichta18, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta20 <- read.FASTA('Csyrichta20_LTRs.fasta', type = "DNA")
distance20 <- dist.dna(Csyrichta20, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta21 <- read.FASTA('Csyrichta21_LTRs.fasta', type = "DNA")
distance21 <- dist.dna(Csyrichta21, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta22 <- read.FASTA('Csyrichta22_LTRs.fasta', type = "DNA")
distance22 <- dist.dna(Csyrichta22, model = m, pairwise.deletion = TRUE, gamma = TRUE)

Csyrichta23 <- read.FASTA('Csyrichta23_LTRs.fasta', type = "DNA")
distance23 <- dist.dna(Csyrichta23, model = m, pairwise.deletion = TRUE, gamma = TRUE)


df <- data.frame(sequence = c('Csyrichta6','Csyrichta9','Csyrichta10','Csyrichta12',
                              'Csyrichta13','Csyrichta14','Csyrichta15','Csyrichta16',
                              'Csyrichta17','Csyrichta18','Csyrichta20','Csyrichta21',
                              'Csyrichta22','Csyrichta23'),
       distances = c(distance6, distance9, distance10, distance12, distance13,
                     distance14, distance15, distance16, distance17, distance18,
                     distance20, distance21, distance22, distance23))

min_rate <- 2.2E-3 #Kumar S, Subramanian S (2002) Mutation rates in mammalian genomes. PNAS 99: 803–808
max_rate <- 3E-3 #Pace JK, Gilbert C, Clark MS, Feschotte C (2008) Repeated horizontal transfer of a DNA transposon in mammals and other tetrapods. PNAS 105: 17023–17028

age <- function(vector,rate) {
  
  A <- c()
  
  for (i in 1:length(vector)){
    a <- vector[i]/(2*rate)
    A <- append(A, a)
  }
  
  return(A)
}

min_ages <- data.frame(min_age = age(df$distances,max_rate))

max_ages <- data.frame(max_age = age(df$distances,min_rate))

cbind(df,min_ages,max_ages)
