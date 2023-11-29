# 231123 codeschool

## Task for 28/11/23
Plot the top 10 CNV genes (and their frequency) in the DNA samples processed on the TSO500 assay between 1st July 2023 until 1st Nov 2023.

- You will need to filter for samples (DNA test code is 8471 and 8475) processed from 1st July 2023 until 1st Nov 2023
- Plot a histogram of the top 10 CNVs (called "gene amplification") from the file CombinedVariantOutput.tsv files - this will be in the directory /output/TSO500-YYMMDD_HHMM/eggd_tso500/analysis_folder/Results/sampleID
- You can search the CombinedVariantOutput.tsv files using python's dxpy module or on the command line

```bash
# wrong thing
time python do_the_thing_code.py --start_date 230701 --end_date 231101 --test_code 8471 8475 --file_type CombinedVariantOutput
DNAnexus login successful

real    17m18.379s
user    0m20.769s
sys     0m3.019s

# with histogram
time python do_the_thing_code.py --start_date 230701 --end_date 231101 --test_code 8471 8475 --file_type CombinedVariantOutput
DNAnexus login successful

real    18m32.992s
user    0m17.608s
sys     0m2.411s
```
