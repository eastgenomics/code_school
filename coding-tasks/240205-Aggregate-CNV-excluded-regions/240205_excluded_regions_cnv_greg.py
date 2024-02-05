import concurrent.futures
import dxpy as dx
import pandas as pd
import subprocess

def get_projects(search, date):
    """Find projects within specified data range"""
    projects = dx.bindings.search.find_projects(
        name = search,
        name_mode = "glob",
        created_after = date,
        describe = {'fields': {'name': True}})
    return list(projects)


def read2df(file_id):
    """Read in tsv file to df"""
    file = dx.bindings.dxfile_functions.open_dxfile(
        file_id[1],
        project=file_id[0], 
        mode="r", 
    )
    return pd.read_csv(file, sep = "\t", header = None)    


def get_merged_tables(file_ids):
    """Read in and merge a list of tables"""
    all_dfs = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        concurrent_jobs = {
            executor.submit(read2df, file_id): file_id for file_id in file_ids
            }
        for future in concurrent.futures.as_completed(concurrent_jobs):
            try:
                all_dfs.append(future.result())
            
            except Exception as exc:
                print(
                    f"Error reading file for {concurrent_jobs[future]}: {exc}"
                )
    merged_df = pd.concat(all_dfs)
    return merged_df


def main():
    projects = get_projects("002*_CEN", "2023-07-18")
    print(f"No. of projects: {len(projects)}")
    file_ids = []
    for proj in projects:
        run_name = proj["describe"]["name"]
        file_name = run_name + "_excluded_intervals.bed"
        
        # Find files in project
        search_results = list(dx.bindings.search.find_data_objects(
            classname ="file",
            name = file_name,
            name_mode = "glob",
            folder = "/output",
            project = proj["id"]))

        if len(search_results) == 1:
            file_ids.append([proj["id"], search_results[0]["id"]])
        elif len(search_results) > 1:
            print(f"multiple files in {proj['id']}")

    print(f"No. of files {len(file_ids)}")
    merged_df = get_merged_tables(file_ids)
    merged_df_counted = merged_df.groupby(merged_df.columns.tolist(), as_index=False).size()
    print(f"No. of unique regions {len(merged_df_counted)}")
    merged_df_counted.to_csv(
        "excluded_regions.tsv", sep = "\t", header = True, index = False
    )
    # Annotate regions in merged excluded regions using data in exons and gt2 files 
    subprocess.run(
        """sort -k 1,1 -k2,2n excluded_regions.tsv -o excluded_regions1.tsv
        bedtools map -a excluded_regions1.tsv -b <(dx cat file-GF611Z8433Gk7gZ47gypK7ZZ | sort -k 1,1 -k2,2n) -c 4 -o antimode > excluded_regions2.tsv
        bedtools map -a excluded_regions2.tsv -b <(dx cat file-GF611Z8433Gf99pBPbJkV7bq | sort -k 1,1 -k2,2n) -c 4 -o antimode > excluded_regions_final.tsv""",
        shell=True, executable="/bin/bash")


if __name__ == "__main__":
    main()