import argparse
import datetime
import os
import re
import traceback

from dotenv import load_dotenv, find_dotenv
import dxpy
import pandas as pd
import plotly.express as px


load_dotenv(find_dotenv())

DX_TOKEN = os.environ.get("DNANEXUS_TOKEN")


def login_dnanexus():
    """ Login to DNAnexus using a auth token present in the environment """

    DX_SECURITY_CONTEXT = {
        "auth_token_type": "Bearer",
        "auth_token": DX_TOKEN,
    }

    dxpy.set_security_context(DX_SECURITY_CONTEXT)

    try:
        dxpy.whoami()
        print("DNAnexus login successful")
    except Exception:
        traceback.print_exc()
        exit()


def convert_str_to_timestamp(date: str) -> str:
    """ Convert dates from the command line to timestamp

    Args:
        date (str): Date in a YYMMDD format

    Returns:
        str: Epoch timestamp
    """

    date_obj = datetime.datetime.strptime(date, "%y%m%d")
    # add 3 zeros at the end because DNAnexus needs milliseconds info
    return f"{int(date_obj.timestamp())}000"


def get_tso_projects(start_date: int, end_date: int):
    """ Get the TSO500 projects in DNAnexus using a date range

    Args:
        start_date (int): Epoch timestamp for the start date for filtering
        end_date (int): Epoch timestamp for the end date for filtering

    Returns:
        generator: Generator for the list of projects
    """

    assert end_date > start_date, (
        f"End_date {end_date} is before than start_date {start_date}"
    )

    return dxpy.bindings.search.find_projects(
        name="002*TSO500", name_mode="glob", created_after=start_date,
        created_before=end_date
    )


def get_sample_files(
    project_id: str, folder_pattern: list, file_pattern: str
) -> list:
    """ Get the files according to the folder pattern and the file pattern

    Args:
        project_id (str): Project id to restrict file search
        folder_pattern (list): List of the test code to filter the right samples
        file_pattern (str): String to filter the file to get

    Returns:
        list: List of file objects
    """

    files = []

    for file in dxpy.bindings.search.find_data_objects(
        name=f"*{file_pattern}*", name_mode="glob", project=project_id
    ):
        file_obj = dxpy.DXFile(file["id"], file["project"])
        file_path = file_obj.describe()["folder"]

        regex_pattern = (
            r"/output/TSO500-[0-9]{6}_[0-9]{4}/eggd_tso500/analysis_folder/"
            r"Results/.*" + f"({'|'.join(folder_pattern)})"
        )

        # check if the file path endswith the test codes that we want 
        if re.fullmatch(regex_pattern, file_path):
            # check if the file is live
            if file_obj.describe()["archivalState"] == "live":
                files.append(file_obj)

    return files


def parse_data_file(file: dxpy.DXFile) -> list:
    """ Parse the CombinedVariantOutput file

    Args:
        file (dxpy.DXFile): DXFile for the CombinedVariantOutput file

    Returns:
        list: List of the Gene Amplifications section
    """

    data = []
    # flag to identify whether we are in the gene amplification section
    gene_amplification_flag = False

    for line in file:
        line = line.strip()

        if line == "[Gene Amplifications]":
            gene_amplification_flag = True
            continue

        if gene_amplification_flag:
            # skip the "header" row of the gene amplification section
            if line == "Gene\tFold Change":
                continue

            # skip sections when no CNVs were detected
            if line == "NA":
                gene_amplification_flag = False
                return data
        
            # return data after empty line i.e. finished going through the CNV
            # data 
            if line == "":
                return data

            data.append(line.split("\t"))

    return data


def plot_cnvs(df: pd.DataFrame):
    """ Plot the CNV data using Plotly

    Args:
        df (pd.DataFrame): Dataframe to plot
    """

    fig = px.histogram(df, x=df.index, y="count")
    fig.write_html("plot_correct.html")


def main(**args):
    login_dnanexus()

    full_df = pd.DataFrame([], columns=["Gene", "Fold change"])

    for project in get_tso_projects(
        convert_str_to_timestamp(args["start_date"]),
        convert_str_to_timestamp(args["end_date"])
    ):
        files = get_sample_files(
            project["id"], args["test_code"], args["file_type"]
        )

        for file in files:
            file_data = parse_data_file(file)

            if file_data:
                df = pd.DataFrame(file_data, columns=["Gene", "Fold change"])
                # change type of the Fold change column
                df["Fold change"] = pd.to_numeric(df["Fold change"])
                full_df = pd.concat([full_df, df])

    # Group using the Gene column and append values into a list
    full_df = full_df.groupby(by="Gene").agg(list)
    # Get the number of occurences of each CNV
    full_df["count"] = full_df["Fold change"].str.len()

    # get the 10 highest values in the Fold change column and get their rows
    # for plotting
    plot_cnvs(full_df.nlargest(10, "count"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-start_date", "--start_date", required=True, help="Format as YYMMDD"
    )
    parser.add_argument(
        "-end_date", "--end_date", required=True, help="Format as YYMMDD"
    )
    parser.add_argument(
        "-test_code", "--test_code", nargs="+", required=True, help=""
    )
    parser.add_argument(
        "-file_type", "--file_type", required=True, help=""
    )

    args = parser.parse_args()
    main(
        start_date=args.start_date, end_date=args.end_date,
        test_code=args.test_code, file_type=args.file_type
    )
