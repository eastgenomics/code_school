#Rationale: convert xlsx file into tsv file

import argparse
import pandas as pd

def parse_args() -> argparse.Namespace:
    """
    Parse the inputs given on the command line
    
    Returns
    ----------
    args : Namespace
        Namespace object of passed command line argument inputs
    """
    parser = argparse.ArgumentParser(
        description="Required input file to convert xlsx file to tsv"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        required=True,
        help="The xlsx file name to convert into tsv file"
    )

    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=True,
        help="The tsv file name to save the gene list in tsv format"
    )

    
    args = parser.parse_args()
    return args


def read_xlsx_to_dataframe(input_file: str) -> pd.DataFrame:
    """
    Read a xlsx file to a Pandas dataframe.

    Parameters
    ----------
    input_file : str
        Name of input file

    Returns
    ----------
    pd.DataFrame
        xlsx file contents as Pandas dataframe
    
    Raises
    ----------
    SystemExit
        If file not found
    """
    try:
        dataframe = pd.read_excel(input_file, skiprows=2,header=None) #genes start at line 2
    except FileNotFoundError as exc:
        raise SystemError(f"File not found -> {input_file}.") from exc
    
    return dataframe


def save_df_into_tsv(input_df: pd.DataFrame, outfile_name: str):
    """
    Save the dataframe into a tsv file
    
    Parameters
    ----------
    input_df : pd.DataFrame
        dataframe with no headers containing one column of genes and some values to be stripped
    
    Returns:
    ----------
    str
        output file name to save the dataframe into tsv file
    
    Raises
    ----------
    ValueError
        IF the number of genes are less or more than 1385, as expected from the TruSight pancancer panel, raise an error
    """
    #Rename columns:
    input_df.columns = ["Gene", "Excess"]
    #Remove any white spaces and any extra lines with text rather than genes:
    gene_list_pancan = input_df['Gene'].str.strip().dropna()

    if (len(gene_list_pancan) != 1385):
        raise ValueError("Gene list does not contain the expected number of genes (less or more than 1385 genes)")
    
    else:
        print(f"There are {len(gene_list_pancan)} as expected - writing formatting version into {outfile_name}")
        gene_list_pancan.to_csv(outfile_name, index=False, sep='\t')


def main():
    args = parse_args()
    gene_list_pancan = read_xlsx_to_dataframe(args.input_file)
    save_df_into_tsv(gene_list_pancan, args.output_file)

if __name__ == "__main__":
    main()