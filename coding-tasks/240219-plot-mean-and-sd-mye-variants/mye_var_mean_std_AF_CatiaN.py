import pandas as pd 
import dxpy as dx 
import io
from collections import defaultdict
from statistics import mean, stdev
import matplotlib.pyplot as plt

# Find projects within data range
projects = dx.bindings.search.find_projects(
    name = "*_MYE",
    name_mode = "glob",
    created_after = "2023-12-01", 
    created_before= "2023-12-15"
    )



# Loop through projects, find folder path and find files
file_ids = []

for project in projects:
    
    folder_name = list(
        dx.bindings.dxfile_functions.list_subfolders(
            project["id"],
            "/output/",
            recurse=False))
    
    if len(folder_name) == 1 and "output/MYE-" in folder_name[0]:
        folder = folder_name[0]
        results = dx.bindings.search.find_data_objects(
            classname="file",
            name="allgenesvep.vcf",
            name_mode="regexp",
            project=project["id"],
            describe={
                'fields': {
                    'name': True,
                    'archivalState': True
                }
              }
           ) 
       
        file_ids += [result['id'] for result in results]

    else:
        ''

print(len(file_ids))
print(file_ids)


#read vcf into a dataframe and provide column names
def read_vcf(file_id):
    with dx.open_dxfile(file_id, mode="r") as fd:  
        lines = [l for l in fd if not l.startswith('##')]
    
        df = pd.read_csv(
        io.StringIO('\n'.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str, 'FORMAT': str,
               'SAMPLE': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

    return df

dfs=[read_vcf(file_id) for file_id in file_ids]





#read df and create a list with transcript and frequency listed

def get_variants_and_freq(df):
    variants = []
    for value, freq in zip(df['INFO'], df.iloc[:,9]):
        if len(value.split(";")) > 20 and len(freq) > 1:   
            variant = value.split("=")[-1] + ":" + freq.split(':')[2]
            variants.append(variant)
        
    return variants


variants = [get_variants_and_freq(df) for df in dfs]

all_variants = []
for var in variants:
    all_variants.extend(var)


#get counts (number of times a variant is listed)
#dict with id and counts
# Populate id_counts
id_counts = {}
for entry in all_variants:
    nm_id = entry.split(':')[0]
    id_counts[nm_id] = id_counts.get(nm_id, 0) + 1

# list with id, value AF and counts
only_var = [(nm_id, value, id_counts[nm_id]) for entry in all_variants for nm_id, value in [entry.split(':')]]


# Sort only_var by descending number of occurrences/counts
only_var = sorted(only_var, key=lambda x: x[2], reverse=True)



#stats from all variants
# Dictionary to store values based on the same nm_id
values_by_nm_id = defaultdict(list)

# Group values based on the same nm_id
for nm_id, value, count in only_var:
    values_by_nm_id[nm_id].append(float(value))

#get the first 20

values_by_nm_id_20 = dict(list(values_by_nm_id.items())[:20])
print(values_by_nm_id_20.keys())


# Calculate mean and standard deviation for each group with more than one data point
means = {}
std_devs = {}
for nm_id, values in values_by_nm_id_20.items():
    if len(values) >= 2:
        means[nm_id] = mean(values)
        std_devs[nm_id] = stdev(values)



print(len(only_var))
# Extract data for the first 20 elements
nm_ids = list(means.keys())
means_values = list(means.values())
std_devs_values = list(std_devs.values())

# Create a bar plot
plt.figure(figsize=(14, 8))
plt.bar(nm_ids, means_values, yerr=std_devs_values, capsize=5, color='skyblue', alpha=0.7)

# Add labels and title
plt.xlabel('Variant')
plt.ylabel('Allele Frequency')
plt.title('Mean and Standard Deviation for each nm_id')
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()

