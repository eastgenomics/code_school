import dxpy as dx
import glob
import os
import pandas as pd


def find_tso_projects():
    tso_projects = list(dx.find_projects(
        level='VIEW',
        created_after='2023-07-18',
        created_before='2024-01-30',
        name="002*CEN",
        name_mode="glob"
    ))

    # Get only the IDs from each response dict
    tso_projects_ids = [proj['id'] for proj in tso_projects]

    return tso_projects_ids

def download_excluded_files(tso_projects_ids):
    no_excluded_bed = []
    need_archival = []

    for project in tso_projects_ids:
        excluded_file = list(
                dx.find_data_objects(
                    project=project,
                    recurse=True,
                    name=".*_excluded_intervals.bed",
                    name_mode='regexp',
                    classname='file'
                )
            )

        print(excluded_file)
        # some projects maybe new and not have the excluded bed file
        # generated so skip these
        if len(excluded_file) != 0:
            excluded_file_id = excluded_file[0]['id']
            if dx.bindings.dxdataobject_functions.describe(excluded_file_id)['archivalState'] != "live":
                # check if it is live, if not then note it
                need_archival.append(excluded_file_id)
            else:
                excluded_file_name= dx.bindings.dxdataobject_functions.describe(excluded_file_id)['name']
                print(excluded_file_name)
                dx.bindings.dxfile_functions.download_dxfile(excluded_file_id, excluded_file_name)
        else:
            project_no_bed = dx.bindings.dxdataobject_functions.describe(project)['name']
            no_excluded_bed.append(project_no_bed)

def merge_excluded_files(extension):
    file_list_all = glob.glob(extension)
    file_list = list(filter(lambda file: os.stat(file).st_size > 0, file_list_all))
    # check how many excluded bed fules were empty
    print( set(file_list_all) - set(file_list))
    dfs = []
    for file in file_list:
        df = pd.read_csv(file, sep='\t', names=["chr","start","end","+","."],index_col=False)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df.drop(columns=["+","."],inplace=True)
    df.to_csv("combined_excluded_intervals.tsv", sep="\t", index=None)

    return df

def add_symbol_annotation(excluded_interval_exonic, symbol_gcf):
    exc_panel_transcript = pd.read_csv(excluded_interval_exonic,
                                    sep = "\t", header=None,
                                    names=["chr_exluded", "pos_start_excluded",
                                    "pos_end_excluded", "count",
                                    "chr", "start", "end", "HGNC_ID",
                                    "Transcript", "Exon"])
    exc_panel_transcript_subset = exc_panel_transcript[[
                                        "chr_exluded", "pos_start_excluded",
                                        "pos_end_excluded", "count", "HGNC_ID",
                                        "Transcript", "Exon"]]

    ## merge with the cds based on the transcript info
    cds_gene = pd.read_csv(symbol_gcf,
                            sep="\t",names=["Chr", "Start",
                            "End", "Gene_Symbol", "Transcript",
                            "Exon"], dtype='unicode')
    cds_gene_subset = cds_gene[["Gene_Symbol", "Transcript"]]
    cds_gene_subset = cds_gene_subset.drop_duplicates()

    df = exc_panel_transcript_subset.merge(cds_gene_subset,
                                                on='Transcript', how='left')
    return df

def main():

    # get the projects
    # tso_projects_ids = find_tso_projects()
    # print(len(tso_projects_ids))

    # find and download the excluded files
    # download_excluded_files(tso_projects_ids)

    # read in all excluded files and concat them
    df = merge_excluded_files("*_excluded_intervals.bed")

    # get the counts from the merged df
    df2 = df.groupby(["chr","start","end"]).size()
    (pd.DataFrame(df2
            )
    .to_csv('count_combined_excluded_intervals.tsv', sep='\t'
            )
    )

    # on the cmd line intersect with exonic file to get the transcript
    # and HGNC id information
    os.system("bedtools intersect -b GCF_000001405.25_GRCh37.p13_genomic.exon_5bp_v2.0.0.tsv -a count_combined_excluded_intervals.tsv -wao > count_combined_excluded_intervals_exonic.tsv")

    df = add_symbol_annotation("count_combined_excluded_intervals_exonic.tsv", "GCF_000001405.25_GRCh37.p13_genomic.symbols.exon_5bp_v2.0.0.tsv")
    df.to_csv("annotated_count_combined_excluded_intervals.tsv", sep="\t", index=None)

if __name__ == "__main__":

    main()