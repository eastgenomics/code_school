"""Utility function for calculating the length of a bed file."""
import os
import pandas as pd


def calculate_total_bed_length(filepath):
    """
    Calculates the total genomic length covered by a BED file.

    This function reads the first three columns of a BED file (Chrom, Start,
    End), validates that the coordinates are numeric and logical, and
    returns the sum of the lengths of all regions.

    Parameters
    ----------
    filepath : str
        The path to the BED file to be processed.

    Returns
    -------
    int
        The total number of base pairs across all regions defined in the file.

    Raises
    ------
    FileNotFoundError
        If the provided filepath does not exist on the system.
    TypeError
        If the 'start' or 'end' columns contain non-numeric data.
    ValueError
        If any record has a start coordinate greater than the end coordinate.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")

    cols = ['chrom', 'start', 'end']
    df = pd.read_csv(filepath, sep='\t', names=cols, usecols=[0, 1, 2])

    if df.empty:
        return 0

    # Explicit validation instead of try/except
    if not pd.api.types.is_numeric_dtype(df['start']) or \
       not pd.api.types.is_numeric_dtype(df['end']):
        raise TypeError("BED coordinates must be numeric.")

    df['length'] = df['end'] - df['start']

    if (df['length'] < 0).any():
        raise ValueError("Found BED record where start > end.")

    return int(df['length'].sum())
