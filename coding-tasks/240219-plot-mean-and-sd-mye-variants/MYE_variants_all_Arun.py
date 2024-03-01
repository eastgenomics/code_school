"""
Codeschool task for 19/02/24:
--------------------------------------------------------------
Aggregate all MYE variants and plot a histogram of the allele frequency 
(of the top 20 variants) along with the mean and standard deviation.
- Start from run 01/12/23 to 05/02/24
- Files end in *_allgenesvep.vcf and exist in the output folder 
(for example: /output/MYE-YYMMDD_HHMM/eggd_vcf_handler_for_uranus-2.7.0)

"""
import concurrent.futures
import dxpy as dx
import matplotlib.pyplot as plt
import pandas as pd




def get_002_mye_projects_in_period(start_date, end_date):
    """
    Gets all the 002 MYE projects between the period given
    Parameters
    ----------
    first_date : str
        e.g. '2023-12-01'
    end_date : str
        e.g. '2024-02-05'
    Returns
    -------
    mye_projs_response : list
        list of dicts, each representing info about a proj found
    """
    # Search projs in the period starting with 002 and ending with MYE
    mye_projs_response = list(dx.find_projects(
        level='VIEW',
        created_after=start_date,
        created_before=end_date,
        name="002*MYE",
        name_mode="glob",
        describe={'fields': {'name': True}}
    ))

    return mye_projs_response

def get_all_genes_vcf_file(project_list):
    """
    Gets all the 002 MYE projects between the period given
    Parameters
    ----------
    project : list
        e.g. input from get_002_mye_projects_in_period
        
    Returns
    -------
    mye_projs_response : list
        list of file ids
    """
    file_ids = []
    for proj in project_list:
        file_name = "*_allgenesvep.vcf"

        # Find files in each project
        search_result = list(dx.bindings.search.find_data_objects(
            classname="file",
            name=file_name,
            name_mode="glob",
            folder="/output",
            project=proj["id"]
        ))

        if len(search_result) == 0:
            print(f"no file found in {proj['id']}")
        elif len(search_result) >= 1:
            for file in search_result:
                file_ids.append([proj["id"], file["id"]])
    
    return file_ids

# Example file_id: ['project-Gbjy6k04F8b3jB1Xfbzf7KX0',
# 'file-GbjzZ904v0J0pK39YJ4Q71bz']

def read2vcf(file_id):
    """
    Read vcf files into a dataframe format, will be used for parallelisation
    Parameters
    ----------
    file_id : list
        from DNAnexus [project-id, file-id]

    Returns
    -------
    pandas.dataframe
        returns dataframe, using specific columns, reads from line 282
    """
    file = dx.bindings.dxfile_functions.open_dxfile(
        dxid=file_id[1],
        project=file_id[0],
        mode="r"
    )
    
    # 282 to return all variants, 281 to return variants with the start of
    # the vcf header, while dropping duplicates
    return pd.read_csv(file, sep ="\t", skiprows=282, header=None, 
                       usecols=[0,1,2,3,4,9]).drop_duplicates()

def get_merged_vcfs(file_ids):
    """
    Read in and merge a list of vcf tables

    Parameters
    ----------
    file_ids : list
        list of DNA files from get_all_genes_vcf_file(project_list)
        

    Returns
    -------
    merged_df : df table

    """
    all_dfs = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        concurrent_jobs = {
            executor.submit(read2vcf, file_id): file_id for file_id in file_ids
            }
        for  future in concurrent.futures.as_completed(concurrent_jobs):
            try:
                all_dfs.append(future.result())
            except Exception as exc:
                print(f"Error reading file for {concurrent_jobs[future]} : \
                      {exc}")
    merged_df = pd.concat(all_dfs)
    return merged_df


def main():
    # Get projects in perioids
    projects = get_002_mye_projects_in_period("2023-12-01", "2024-02-05")
    print(f"No. of projects: {len(projects)}")

    # Get file_ids with files of interest
    file_ids = get_all_genes_vcf_file(projects)
    print(f"No. of files {len(file_ids)}")

    # Generate a df with all vcfs merged into one
    merged_df = get_merged_vcfs(file_ids)
    # Create an allele frequency column, the elements of each column are in
    # a string format
    merged_df["AF"] = merged_df[9].str.split(":", expand=True).iloc[:, 2]
    # Convert the "AF" column to numeric, raise when exceptions occur
    merged_df["AF"] = pd.to_numeric(merged_df["AF"], errors='raise')
    # Create a table with counted number of variants, choosing relevant cols

    # create a dict to store counts of each unique variants
    variant_counts = {}

    for i in range(len(merged_df)):
        row = merged_df.iloc[i]
        variant = tuple(row[0:5])
        if variant in variant_counts:
            variant_counts[variant] += 1
        else:
            variant_counts[variant] = 1

    # Get the top 20 key-value pairs
    sorted_variant_counts = dict(sorted(variant_counts.items(),
                                        key=lambda item: item[1],
                                        reverse=True))
    top_20_dict = dict(list(sorted_variant_counts.items())[:20])

    # Filter the DataFrame to keep only the top frequent variants
    # Top 20 variants have 503 or more
    filtered_df = merged_df[merged_df.apply(lambda row: tuple(row[0:5]) in 
                                            top_20_dict, axis=1)]
    # Alternative
    #filtered_df = merged_df[merged_df.apply(lambda row: tuple(row[0:5]) in 
    #                                        variant_counts and 
    #                                        variant_counts[tuple(row[0:5])] >=
    #                                        503, axis=1)]
    
    # Create a new table, each row is [variant], [AF]
    data = []
    for i in range(len(filtered_df)):
        row = filtered_df.iloc[i]
        variant = str(tuple(row[0:5]))
        allele_frequency = row['AF']
        data.append([variant,allele_frequency])
    
    df = pd.DataFrame(data=data, columns =['Variant', 'AF'])
    
    # calculate the mean and standard deviation value for each variant
    variant_AF_stats = df.groupby('Variant')['AF'].agg(['mean', 'std'])

    # Plotting the data
    plt.figure(figsize=(10,7))
    plt.bar(variant_AF_stats.index, variant_AF_stats['mean'],
            yerr=variant_AF_stats['std'], capsize=7)
    plt.xlabel('Variants')
    plt.ylabel('Mean Allele Frequency')
    plt.title('Mean allele frequency of each Variant')
    plt.xticks(rotation=90)
    plt.show()


if __name__ == "__main__":
    main()
