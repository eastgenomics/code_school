#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dxpy as dx
from collections import Counter
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

# Find projects within data range
projects = dx.bindings.search.find_projects(
    name = "*_TSO500",
    name_mode = "glob",
    created_after = "2023-07-01",
    created_before = "2023-11-01")


# Loop through projects, find folder path and find files
file_ids = []
for project in projects:
    
    folder_name = list(
        dx.bindings.dxfile_functions.list_subfolders(
            project["id"],
            "/output/",
            recurse=False))
    
    if len(folder_name) == 1 and "output/TSO500-" in folder_name[0]:
        folder = folder_name[0]
        results = dx.bindings.search.find_data_objects(
            classname="file",
            name="(8471|8475)_CombinedVariantOutput\.tsv",
            name_mode="regexp",
            project=project["id"],
            folder=folder+"/eggd_tso500/analysis_folder/Results/") 
        
        file_ids += [result["id"] for result in results]
    
    else:
        print(f"Weird folder structure for {project['id']}")
        
# Weird folder structure for project-GYxKjQj44xj1694QbKXyJ8f3

# Parse CNV genes
file_ids = set(file_ids)
data = []
switch = 0
for file_id in file_ids:
    fd = dx.open_dxfile(file_id)
    for line in fd:
        if "[Splice Variants]" in line.split("\t"):
            switch = 0
            break
        
        if "[Gene Amplifications]" in line.split("\t"):
            switch = 1
            continue
            
        if line != "Gene\tFold Change\t" and not line.isspace() and switch == 1:
            data.append(line.split("\t")[0])
            
# Count frequency of genes in list and turn into df
df = pd.DataFrame().from_dict(Counter(data), orient = "index")
df = df.rename(columns={0:"Freq"})

# Sort and take top 10 (exlcuding NA)
df.sort_values(by="Freq", axis=0,ascending=False,inplace=True)
df_top10 = df.iloc[1:11,]

fig = px.histogram(
    df_top10, x=df_top10.index, y="Freq")
fig.update_layout(title = "Top 10 CNVs July to November 2023",yaxis_title="Frequency", xaxis_title = "Gene")
fig.show()


        
        
