# Task for 28/11/23:

***Plot the top 10 CNV genes (and their frequency) in the DNA samples processed on the TSO500 assay between 1st July 2023 until 1st Nov 2023.***

- You will need to filter for samples (DNA test code is 8471 and 8475) processed from 1st July 2023 until 1st Nov 2023
- Plot a histogram of the top 10 CNVs (called "gene amplification") from the file CombinedVariantOutput.tsv files - this will be in the directory **/output/TSO500-YYMMDD_HHMM/eggd_tso500/analysis_folder/Results/sampleID**
  - Please note there's multiple of each file in the project so make sure you restrict by the Results folder

- You can search the CombinedVariantOutput.tsv files using python's dxpy module or on the command line