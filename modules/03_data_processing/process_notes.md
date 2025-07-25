# Tools

Trimming is a complex question, being very dependent on the current available
data and the project main objective. Also, a large variety of tools are
available. We are gonna present general guidelines and operation on 3 main
wide-spread tools, but further research is always advised.
- Trimmomatic
- ConDeTri
- BBDuk

# Overview

We are gonna to use the pre-processing information to operate on the files
aiming to get better data. FASTP does a great work in pipelining this portion of
the workflow, because it analyses and already trims data. When opting to use
a separate tool, all precautions are needed, and one must keep in mind that this
step is detrimental to the final result.

# Using the tools

## ConDeTri

## Trimmomatic

## BBDuk

1. Installing = bbmap?
```bash
conda install bbmap
```
2. Now, inside bbmap, we'll use the BBDuk tool.
    - With paired end in 2 separated files, both must be read together.
    - You shall use in1/in2 and out1/out2 parameters to specify them.
    - The program accepts a reference file for k-mer trimming.
    - Supports k 1-31.
```bash
bbduk.sh in1=result1_trim.fq in2=result2_trim.fq out1=cleantrim1.fq \
out2=cleantrim2.fq \
ref=/home/leveduras/miniforge3/envs/preprocessing/opt/bbmap-38.90-2\
/resources/adapters.fa ktrim=n k=23 mink=11 hdist=1 tpe tbo qtrim=rl trimq=10
```
    - Check the adapters.fa file.
    - A lot of custom options one must consider.
    - Review docs.
```bash
Initial:
Memory: max=18488m, total=18488m, free=18438m, used=50m

Added 217135 kmers; time: 	0.050 seconds.
Memory: max=18488m, total=18488m, free=18354m, used=134m

Input is being processed as paired
Started output streams:	0.002 seconds.
Processing time:   		11.816 seconds.

Input:                  	25395400 reads 		3805761120 bases.
QTrimmed:               	38573 reads (0.15%) 	398042 bases (0.01%)
KMasked:                	28066 reads (0.11%) 	375927 bases (0.01%)
Trimmed by overlap:     	145 reads (0.00%) 	7372 bases (0.00%)
Total Removed:          	6 reads (0.00%) 	405414 bases (0.01%)
Result:                 	25395394 reads (100.00%) 	3805355706 bases (99.99%)

Time:                         	11.869 seconds.
Reads Processed:      25395k 	2139.64k reads/sec
Bases Processed:       3805m 	320.65m bases/sec
```
3. You can check one more time with fastqc the new trimmed files for scouting,
   if needed.
4. Proceed to the next step.
