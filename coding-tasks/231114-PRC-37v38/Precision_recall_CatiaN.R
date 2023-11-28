
library(devtools)
library(tidyverse)
library(dplyr)
library(readr)
library(plyr)

#set working directory where I have both b37 and b38 files
setwd("~/Documents/codeschool/14nov2023")

#set wd in b37 folder
setwd("~/Documents/codeschool/14nov2023/b37")
#list all file samples in b37folder
#aplly read_csv to all files(lapply) as well as column with id name (each file name)
#bind rows from all file samples
#eliminate .summary.csv from all file names in name (id) column
b37 <- list.files() %>%
 lapply(read_csv, id='name') %>%
 bind_rows %>% mutate(name = str_remove_all(name, ".summary.csv"))
#add column with genome ref to merged data.frame
b37$genome <- 'b37'

#same for b38
setwd("~/Documents/codeschool/14nov2023/b38")
b38 <- list.files() %>%
  lapply(read_csv, id='name') %>%
  bind_rows %>% mutate(name = str_remove_all(name, ".summary.csv"))
#add column with genome ref to merged data.frame
b38$genome <- 'b38'

#merge both data sets (already correctly identified)
All <- rbind(b37, b38)

#plot PR graph for all samples specifying the type indel, add threshold lines and change limits
#labs is for labels of axis and legend
ggplot(subset(All, Filter == 'PASS' |Type == 'INDEL'),aes(x = METRIC.Recall, y = METRIC.Precision, color = genome, shape = name)) +
  geom_point(aes(color = genome, shape = name)) + theme_minimal() +
  scale_x_continuous(limits = c(0.810, 1.01))+ 
  scale_y_continuous(limits = c(0.61, 0.8))+
  scale_color_brewer(palette = "Set2") + geom_vline(aes(xintercept = 0.850), linetype= "dotted",colour = 'orange')+
  geom_vline(aes(xintercept = 0.820), linetype='dotted', colour = 'red')+
  geom_hline(aes(yintercept = 0.620), linetype='dotted', colour ='red')+
  labs(x = "Recall", y = "Precision", color = "Genome", shape ='Sample') +
  ggtitle("Precision recall",
          "INDEL")  

#plot PR graph for all samples specifying the type SNP, add threshold lines and change limits
ggplot(subset(All, Filter == 'PASS' | Type == 'SNP'),aes(x = METRIC.Recall, y = METRIC.Precision, color = genome, shape = name)) +
  geom_point() + theme_minimal() +
  scale_x_continuous(limits = c(0.989, 1.005))+ 
  scale_y_continuous(limits = c(0.983, 1.00))+
  scale_color_brewer(palette = "Set2") + geom_vline(aes(xintercept = 0.999), linetype= "dotted",colour = 'orange')+
  geom_vline(aes(xintercept = 0.990), linetype='dotted', colour = 'red')+
  geom_hline(aes(yintercept = 0.995), linetype='dotted', colour ='red')+
  labs(x = "Recall", y = "Precision", color = "Genome", shape ='Sample') +
  ggtitle("Precision recall",
          "SNP")  

#plot PR graph-b37 INDEL
ggplot(subset(b37, Filter == 'PASS' |Type == 'INDEL'),aes(x = METRIC.Recall, y = METRIC.Precision, color = name)) +
  geom_point() + theme_minimal() +
  scale_x_continuous(limits = c(0.810, 1.01))+ 
  scale_y_continuous(limits = c(0.61, 0.8))+
  scale_color_brewer(palette = "Set2") + geom_vline(aes(xintercept = 0.850), linetype= "dotted",colour = 'orange')+
  geom_vline(aes(xintercept = 0.820), linetype='dotted', colour = 'red')+
  geom_hline(aes(yintercept = 0.620), linetype='dotted', colour ='red')+
  labs(x = "Recall", y = "Precision", color = "Sample") +
  ggtitle("Precision recall b37",
          "INDEL")  

#plot PR graph-b37 SNP
ggplot(subset(b37, Filter == 'PASS' |Type == 'SNP'),aes(x = METRIC.Recall, y = METRIC.Precision, color = name)) +
  geom_point() + theme_minimal() +
  scale_x_continuous(limits = c(0.989, 1.005))+ 
  scale_y_continuous(limits = c(0.983, 1.00))+
  scale_color_brewer(palette = "Set2") + geom_vline(aes(xintercept = 0.999), linetype= "dotted",colour = 'orange')+
  geom_vline(aes(xintercept = 0.990), linetype='dotted', colour = 'red')+
  geom_hline(aes(yintercept = 0.995), linetype='dotted', colour ='red')+
  labs(x = "Recall", y = "Precision", color = "Sample") +
  ggtitle("Precision recall b37",
          "SNP")  

#plot PR graph-b38 INDEL
ggplot(subset(b38, Filter == 'PASS' |Type == 'INDEL'),aes(x = METRIC.Recall, y = METRIC.Precision, color = name)) +
  geom_point() + theme_minimal() +
  scale_x_continuous(limits = c(0.810, 1.01))+ 
  scale_y_continuous(limits = c(0.61, 0.8))+
  scale_color_brewer(palette = "Set2") + geom_vline(aes(xintercept = 0.850), linetype= "dotted",colour = 'orange')+
  geom_vline(aes(xintercept = 0.820), linetype='dotted', colour = 'red')+
  geom_hline(aes(yintercept = 0.620), linetype='dotted', colour ='red')+
  labs(x = "Recall", y = "Precision", color = "Sample") +
  ggtitle("Precision recall b38",
          "INDEL")  

#plot PR graph-b38 SNP
ggplot(subset(b38, Filter == 'PASS' |Type == 'SNP'),aes(x = METRIC.Recall, y = METRIC.Precision, color = name)) +
  geom_point() + theme_minimal() +
  scale_x_continuous(limits = c(0.989, 1.005))+ 
  scale_y_continuous(limits = c(0.983, 1.00))+
  scale_color_brewer(palette = "Set2") + geom_vline(aes(xintercept = 0.999), linetype= "dotted",colour = 'orange')+
  geom_vline(aes(xintercept = 0.990), linetype='dotted', colour = 'red')+
  geom_hline(aes(yintercept = 0.995), linetype='dotted', colour ='red')+
  labs(x = "Recall", y = "Precision", color = "Sample") +
  ggtitle("Precision recall b38",
          "SNP")  

