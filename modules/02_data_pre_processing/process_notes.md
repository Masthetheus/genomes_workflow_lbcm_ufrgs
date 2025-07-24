# Gathering files

https://pmc.ncbi.nlm.nih.gov/articles/PMC3871669/
https://link.springer.com/protocol/10.1007/978-1-0716-2067-0_11
https://onlinelibrary.wiley.com/doi/full/10.1002/imt2.107

1. First we gathered the two fq.gz files from the Drive.
2. Renamed for simplicity.
3. Setup new conda env.
```bash
conda create --name preprocessing
conda activate preprocessing
```
4. Make sure bioconda channel is present and active
```bash
conda config --add channels bioconda
conda config --set channel_priority strict
```
5. Install fastp and fastqc via conda
```bash
conda install bioconda::fastqc bioconda::fastp
```
6. Fastqc in GUI mode
```bash
fastqc
```
    - File
    - Add sequence
    - Choose file
    - Wait
    - Analyze graphics

7. Fastqc GUI currently borked on conda
8. Fastqc on terminal
```bash
fastqc filename filename -o intended/out/direct
# make sure output direc already exists!
```
9. Cite that fastqc can be obtained through git
10. Analysis on the output of fastqc
    - Base metrics
    - Overview
    - Insights
    - Graphs example on main page
11. Fastp analysis
```bash
fastp -i test-genome/NCYC357_test_L1_1.fq.gz -I \
test-genome/NCYC357_test_L1_2.fq.gz -o test-genome/results/fastp/result1.fq.gz \
-O test-genome/results/fastp/result2.fq.gz
# remember to check if output exists before running
# fastp better for PE, allow reading them together
```
    - Generated the html and json on the home directory?
    - Base output stands for altered fq file
    - Analyze base output html
    - Graph interpretation
12. Fastp Bonatto's prompt:
``` bash
fastp -i NCYC357_CKDN230000699-1A_HT5GMDSX5_L1_1.fq.gz  \
-I NCYC357_CKDN230000699-1A_HT5GMDSX5_L1_2.fq.gz \
-o NCYC357_CKDN230000699-1A_HT5GMDSX5_L1_1_fastp.fq.gz \
-O NCYC357_CKDN230000699-1A_HT5GMDSX5_L1_2_fastp.fq.gz \ 
 --trim_poly_x --correction
```
    - trim_poly_x = trimms tails
    - correction = based on overlapping detection for pe data, proper overlaps
        leads to mismatch correction
    - Already gives pre and after graph comparison!
13. Draw conclusions from pre-processing
14. If needed, stablish new parameters or re-run fastp until satisfactory
    results.
15. Proceed to processing (if needed).

