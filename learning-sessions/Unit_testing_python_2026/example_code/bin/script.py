"""
This module contains a function to calculate the GC content of a DNA sequence.
"""


def calculate_gc_content(sequence):
    """
    Calculates the GC content percentage of a DNA sequence.

    Input:
        sequence (str): A string representing the DNA sequence (e.g., "ATGC").

    Output:
        float: The GC content percentage, rounded to two decimal places.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the sequence contains characters other than A, T, G, C.
    """

    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string.")

    if not sequence:
        return 0.0

    # Normalize to uppercase to handle mixed cases
    seq = sequence.upper()

    # Validate that sequence contains only DNA bases
    valid_bases = set('ATGC')
    if not all(base in valid_bases for base in seq):
        raise ValueError("Sequence contains invalid characters. "
                         "Only A, T, G, C are allowed.")

    # Count Gs and Cs
    g_count = seq.count('G')
    c_count = seq.count('C')

    gc_percentage = ((g_count + c_count) / len(seq)) * 100
    return round(gc_percentage, 2)
