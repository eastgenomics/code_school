library(ggplot2)
library(tidyverse)

# Collect all files in the b37 folder
b37_files <- dir("/home/rebecca/CodeSchool_task/b37", full.names=TRUE)

# Read them all in as one dataframe, adding a column for the sample name (by removing the rest of the file path)
# And adding a new column build with constant "GRCh37" to denote they are b37 samples
b37 <- read_csv(b37_files, id = "Sample_ID") %>%
  mutate(Sample_ID = str_remove_all(Sample_ID, ".summary.csv")) %>%
  mutate(Sample_ID = str_remove_all(Sample_ID, "/home/rebecca/CodeSchool_task/b37/")) %>%
  add_column(build = "GRCh37")

# Do the same for b38 files with column to say they are GRCh38
b38_files <- dir("/home/rebecca/CodeSchool_task/b38", full.names=TRUE)
b38 <- read_csv(b38_files, id = "Sample_ID") %>%
  mutate(Sample_ID = str_remove_all(Sample_ID, ".summary.csv")) %>%
  mutate(Sample_ID = str_remove_all(Sample_ID, "/home/rebecca/CodeSchool_task/b38/")) %>%
  add_column(build = "GRCh38")

# Concatenate the two dataframes together
b37_and_b38 <- rbind(b37, b38)

# Change variant type to be a factor with levels to determine order of the facets
b37_and_b38$Type = factor(b37_and_b38$Type, levels=c('SNP','INDEL'))

# Create dataframes to denote the locations of the threshold lines for each facet
precision_lines <- data.frame(Type = c("SNP", "INDEL"), Metric.Precision = c(0.995, 0.620))
precision_lines$Type =factor(precision_lines$Type, levels=c('SNP','INDEL'))

recall_warning <- data.frame(Type=c("SNP", "INDEL"), Metric.Recall=c(0.999, 0.850))
recall_warning$Type =factor(recall_warning$Type, levels=c('SNP','INDEL'))

recall_fail <- data.frame(Type=c("SNP", "INDEL"), Metric.Recall=c(0.990, 0.820))
recall_fail$Type =factor(recall_fail$Type, levels=c('SNP','INDEL'))

# Plot with ggplot a subset of only PASS variants, colour by genome build
# Make size of scatter points larger
# Have different facets for SNP vs INDEL but same axes, set x and y lims, update labels
# Use dataframes we made just now to denote the h and y lines
ggplot(subset(b37_and_b38, Filter=="PASS"), aes(x = METRIC.Recall, y = METRIC.Precision, color = build)) +
  geom_point(size=2) +
  facet_grid(~Type) +
  xlim(NA, 1) +
  ylim(NA, 1) +
  labs(x = "Recall", y = "Precision", color = "Genome build") + 
  ggtitle("Precision and recall of GIAB samples tested against GRCh37 vs GRCh38") +
  geom_hline(data=precision_lines, aes(yintercept = Metric.Precision), colour="orange") +
  geom_vline(data=recall_warning, aes(xintercept=Metric.Recall), colour="orange") +
  geom_vline(data=recall_fail, aes(xintercept=Metric.Recall), colour="red") +
  scale_colour_brewer(palette="Set1") +
  theme(plot.title = element_text(size=16))
