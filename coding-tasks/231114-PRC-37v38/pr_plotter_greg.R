library(dplyr)
library(ggplot2)

setwd('~/Documents/Codeschool/231101_precision_recall_plot')

# Function to read and merge CSV files
merge_csv <- function(g_build) {
  path = paste("./", g_build, sep="")
  
  df = list.files(path=path, full.names = T) %>%
    lapply(read.csv, header = T) %>% bind_rows(.id="id")
  df$'g_build' = g_build
  return(df)
}

df_b37 = merge_csv("b37")
df_b38 = merge_csv("b38")
df_b37_b38 = bind_rows(df_b37,df_b38)

# Plot Precision-Recall for SNPs
snp_df_b37_b38 = df_b37_b38 %>% filter(Type == "SNP" & Filter == "PASS")

snp_pr <- ggplot(snp_df_b37_b38, aes(x=METRIC.Recall, y=METRIC.Precision)) +
  geom_point(aes(colour=g_build)) +
  geom_hline(yintercept=0.995, col = "orange") +
  geom_vline(xintercept=0.999, col = "orange") +
  geom_vline(xintercept=0.990, col = "red") +
  xlim(0.96,1) +
  ylim(0.96,1) +
  ggtitle("SNP Precision-Recall b37/b38") +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  labs(x="Recall", y="Precision", colour = "Genome build")
plot(snp_pr)

# Plot Precision-Recall for Indels
indel_df_b37_b38 = df_b37_b38 %>% filter(Type == "INDEL" & Filter == "PASS") 

indel_pr <- ggplot(indel_df_b37_b38, aes(x=METRIC.Recall, y=METRIC.Precision)) +
  geom_point(aes(colour=g_build)) +
  geom_hline(yintercept=0.62, col = "orange") +
  geom_vline(xintercept=0.850, col = "orange") +
  geom_vline(xintercept=0.820, col = "red") +
  xlim(0.55,1) +
  ylim(0.55,1) +
  ggtitle("Indel Precision-Recall b37/b38") +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  labs(x="Recall", y="Precision", colour = "Genome build")
plot(indel_pr)


