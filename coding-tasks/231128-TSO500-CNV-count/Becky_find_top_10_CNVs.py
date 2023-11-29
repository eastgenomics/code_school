import concurrent.futures
import dxpy as dx
import os
import pandas as pd
import plotly.express as px
import sys
import time

from datetime import datetime
from dotenv import load_dotenv


def dx_login(dx_token) -> None:
    """
    Log into DNAnexus
    Parameters
    ----------
    token : str
        authorisation token for DNAnexus, from credentials.json
    Raises
    ------
    Error
        Raised when DNAnexus user authentification check fails
    """
    DX_SECURITY_CONTEXT = {
        "auth_token_type": "Bearer",
        "auth_token": dx_token
    }

    dx.set_security_context(DX_SECURITY_CONTEXT)

    try:
        dx.api.system_whoami()
    except Exception as err:
        sys.exit(1)


def get_002_TSO500_projects_in_period(first_date, last_date):
    """
    Gets all the 002 TSO500 projects between the period given
    Parameters
    ----------
    first_date : str
        e.g. '2023-07-01'
    last_date : str
        e.g. '2023-11-01'
    Returns
    -------
    tso_projs_ids : list
        list of project IDs within the period
    """
    # Search projs in the period starting with 002 and ending with TSO500
    # Return only the ID field from describe
    tso_projs_response = list(dx.find_projects(
        level='VIEW',
        created_before=last_date,
        created_after=first_date,
        name="002*TSO500",
        name_mode="glob"
    ))

    # Get only the IDs from each response dict
    tso_projs_ids = [proj['id'] for proj in tso_projs_response]

    return tso_projs_ids


def get_name_of_TSO_folder(project_id):
    """
    Get the name of the main analysis folder in the TSO500 project
    to enable searching a specific folder for the CombinedVariantOutput
    files later

    Parameters
    ----------
    project_id : str
        ID of the project being searched

    Returns
    -------
    folder_name : str
        name of the folder within the output folder e.g. 'TSO500-230724_0472"
    """
    folder_names = list(
        dx.bindings.dxfile_functions.list_subfolders(
            project=project_id,
            path='/output/',
            recurse=False
        )
    )

    # Check that the TSO500 workflow has only been run once
    if len(folder_names) > 1:
        print(f"Warning: more than one folder found for project {project_id}")

    # Get the actual string of the folder name from the list
    # and remove /output/ from the beginning of the string to just get the
    # name of the single folder, rather than path
    folder_name = [
        name.removeprefix('/output/') for name in folder_names
    ][0]

    return folder_name


def get_combinedvariantoutput_files(project_id, folder_name):
    """
    Find the CombinedVariantOutput files in the relevant path for each project,
    subsetting to only files with 8471 and 8475 in the name as they are DNA

    Parameters
    ----------
    project_id : str
        the proj ID as a string
    Returns
    -------
    combined_var_files : list
        list of dicts containing info about the files found
    """
    # List all of the CombinedVariantOutput files in the specific folder
    # of that project. Only find files with 8471 or 8475 in the name (DNA)
    combinedvar_files_response = list(
        dx.find_data_objects(
            project=project_id,
            folder=(
                f"/output/{folder_name}/eggd_tso500/analysis_folder/Results/"
            ),
            recurse=True,
            name=".*[8471|8475]_CombinedVariantOutput.tsv",
            name_mode='regexp',
            classname='file',
            describe={
                'fields': {
                    'name': True,
                    'archivalState': True
                }
            }
        )
    )

    # Get only these fields in a simple dict for easier querying later
    # and to make the merged list of the hundreds of files slightly
    # smaller later
    combined_var_files = [
        {
            'project': x['project'],
            'id': x['id'],
            'name': x['describe']['name'],
            'archive_state': x['describe']['archivalState']
        } for x in combinedvar_files_response
    ]

    return combined_var_files


def find_archived_files(combined_var_files):
    """
    Check the archivalState of all of the CombinedVariantOutput files
    and return any files which are not live

    Parameters
    ----------
    combined_var_files : list
        list of dicts containing info about each file

    Returns
    -------
    archived_files : list
        list of file IDs of files which are not live
    """
    archived_files = []
    for x in combined_var_files:
        if x['archive_state'] != 'live':
            archived_files.append({'project': x['project'], 'id': x['id']})

    return archived_files


def unarchive_files(archived_files):
    """
    Call unarchive on any files which are not live

    Parameters
    ----------
    archived_files : list
        list of file IDs of non-live files
    """
    for idx, file in enumerate(archived_files):
        print(f"Checking file {idx + 1}/{len(archived_files)}")
        file_object = dx.DXFile(file.get('id'), project=file.get('project'))
        file_object.unarchive()
        time.sleep(5)


def read_to_df(file_dict):
    """
    Read only the [Gene Amplifications] part of the CombinedVariantOutput tsv
    (from a DNAnexus file ID) into a pandas dataframe

    Parameters
    ----------
    file_dict : dict
        dict containing information about the CombinedVariantOutput file

    Returns
    -------
    amplifications : pd.DataFrame
        pandas df of Gene and Fold Change for the sample
    """
    file_id = file_dict['id']
    proj_id = file_dict['project']
    sample_name = file_dict['name'].split('_')[0]

    with dx.open_dxfile(file_id, mode='r') as dx_file:
        # Read TSV to pandas df
        data = pd.read_csv(
            dx_file, sep='\t', header=None, names=list(range(11))
        )
        # Get indexes of section of TSV we want
        start_string = '[Gene Amplifications]'
        idx_start = data.index[data[0] == start_string][0]
        end_string = '[Splice Variants]'
        idx_end = data.index[data[0] == end_string][0]

        # Subset df to just those columns and first two columns
        amplifications = data.loc[idx_start +1: idx_end-1][[0, 1]]
        # Get rid of weird index column
        amplifications = amplifications[1:]
        # Change column names to Gene and Fold Change
        amplifications.columns = ['Gene', 'Fold Change']
        amplifications.reset_index(drop=True, inplace=True)
        # Add constant columns with sample name and proj ID
        amplifications['sample_name'] = sample_name
        amplifications['project_id'] = proj_id

    return amplifications


def concurrent_read_tsv(list_of_file_dicts, workers):
    """
    Concurrently read in the Gene Amplifications to a df for each
    TSV file

    Parameters
    ----------
    list_of_file_dicts : list
        list of dicts, each dict containing info on a CombinedVariantOutput file
    workers : int
        Number of workers

    Returns
    -------
    single_df : pd.DataFrame
        single df with the gene amplification data from all samples
    """
    list_of_dfs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        concurrent_jobs = {
            executor.submit(
                read_to_df, file_dict
            ): file_dict for file_dict in list_of_file_dicts
        }
        for future in concurrent.futures.as_completed(concurrent_jobs):
            try:
                data = future.result()
                list_of_dfs.append(data)
            except Exception as exc:
                print(
                    f"Error reading file for {concurrent_jobs[future]}: {exc}"
                )
    # Concat all the dfs in the list to one
    single_df = pd.concat(list_of_dfs)

    return single_df


def get_gene_counts(var_df):
    """
    Convert a df of all sample gene amplifications to a df containing the
    count of each of the top 10 most frequent genes with CNVs

    Parameters
    ----------
    var_df : pd.DataFrame
        dataframe of all the gene amplifications from all samples

    Returns
    -------
    gene_counts : pd.DataFrame
        dataframe of counts of each of the top 10 most frequent genes
        with CNVs
    """
    gene_counts = var_df[
        var_df['Gene'].notna()
    ]['Gene'].value_counts().rename_axis('Gene').head(10).reset_index(name='Count')

    return gene_counts


def plot_top_10_genes(count_df):
    """
    Plot a histogram with Plotly of the top 10 CNV genes

    Parameters
    ----------
    count_df : pd.DataFrame
        dataframe of counts of each of the top 10 most frequent genes
        with CNVs

    Returns
    -------
    fig: Plotly figure object
        histogram of the counts of the top 10 genes
    """
    fig = px.histogram(count_df, x="Gene", y='Count')

    fig.update_layout(
        title=(
            'Top 10 genes with CNVs for the TSO500 assay, 1st July - 1st '
            'November 2023'
        ),
        yaxis_title='Count'
    )
    return fig


def main():
    print(datetime.now(), "Logging in")
    load_dotenv()
    DX_TOKEN = os.getenv("DX_TOKEN")
    dx_login(DX_TOKEN)

    tso_proj_ids = get_002_TSO500_projects_in_period(
        '2023-07-01', '2023-11-01'
    )
    print(datetime.now(), f"Found {len(tso_proj_ids)} TSO500 projects in the period")

    combined_var_files = []
    for proj in tso_proj_ids:
        folder_to_search = get_name_of_TSO_folder(proj)
        combined_var_files.extend(get_combinedvariantoutput_files(
            proj, folder_to_search
        ))
    print(datetime.now(), f"Found {len(combined_var_files)} CombinedVariantOutput files in those projects")

    print(datetime.now(), "Checking for archived files")
    archived_files = find_archived_files(combined_var_files)

    if archived_files:
        print(
            f"{len(archived_files)} files are still archived. Calling "
            "unarchive on them and exiting. Please re-run later when files are"
            "unarchived"
        )
        unarchive_files(archived_files)
        sys.exit(1)
    else:
        print(datetime.now(), "All files are unarchived. Reading into dataframes and concatenating")
        all_samples_gene_df = concurrent_read_tsv(combined_var_files, 12)

        print(datetime.now(), "Getting the top 10 genes with CNVs")
        gene_counts = get_gene_counts(all_samples_gene_df)

        print(datetime.now(), "Plotting histogram of top 10 genes")
        fig = plot_top_10_genes(gene_counts)
        fig.show()


if __name__ == '__main__':
    main()
