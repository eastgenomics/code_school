import argparse
import csv
import pandas as pd
import random


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments inputs given

    Returns
    -------
    args : Namespace
        Namespace object of passed command line argument inputs
    """
    parser = argparse.ArgumentParser(
        description="Information necessary for assigning secret santa"
    )
    parser.add_argument(
        "-i",
        "--input_names",
        type=str,
        required=True,
        help="TXT file with each participant, one name per line",
    )

    parser.add_argument(
        "-e",
        "--exclusion_pairs",
        type=str,
        required=True,
        help=(
            "CSV file with pairs of people not to be matched together (format"
            " giver,receiver)"
        ),
    )

    parser.add_argument(
        "-m",
        "--max_attempts",
        type=int,
        default=20,
        required=False,
        help="Maximum number of attempts for assignment",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Name of output CSV file with secret santa assignments",
    )

    args = parser.parse_args()
    return args


def read_csv_to_dataframe(input_file: str, separator=",") -> pd.DataFrame:
    """
    Read a CSV file to a Pandas dataframe.

    Parameters
    ----------
    input_file : str
        Name of input file

    Returns
    -------
    pd.DataFrame
        CSV file contents as Pandas dataframe

    Raises
    ------
    SystemExit
        If file not found
    """
    try:
        dataframe = pd.read_csv(input_file, sep=separator)
    except FileNotFoundError as exc:
        raise SystemExit(f"File not found → {input_file}. Exiting") from exc

    return dataframe


def validate_participants(input_names_df: pd.DataFrame) -> list[str]:
    """
    Validate the input file of participants names

    Parameters
    ----------
    input_names_df : pd.DataFrame
        dataframe with one column (name) and participant names

    Returns
    -------
    list
        list of names as strings

    Raises
    ------
    ValueError
        IF there is no 'name' column in the input names file or less than 2
        participants given as input
    """
    if "name" not in input_names_df:
        raise ValueError(
            "Input names file does not have required 'name' column header"
        )

    # Remove any whitespace, empty lines and convert to list
    names_list = input_names_df["name"].str.strip().dropna().to_list()

    if len(names_list) < 2:
        raise ValueError("Error: Number of names inputted is less than 2")

    return names_list


def convert_excluded_dataframe_to_dict(input_df: pd.DataFrame, names: list):
    """
    Convert dataframe of excluded pairs to a dictionary, where the
    giver is the key and the people they cannot give to are present in the
    value list.

    Parameters
    ----------
    input_df : pd.DataFrame
        dataframe with headers giver and receiver for excluded pairs

    Returns
    -------
    dict
        dictionary of excluded pairs. Example:
            {
                "Bob": ["Erin"],
                "Alice": ["Bob", "Charlie"]
            }

    Raises
    ------
    RuntimeError
        If input CSV of excluded pairs doesn't have giver and receiver columns
        or has names which aren't in input participant names
    """
    if not {"giver", "receiver"}.issubset(input_df.columns):
        raise RuntimeError(
            "Error: Exclusion CSV must contain 'giver' and 'receiver' columns."
        )

    # Strip whitespace
    input_df["giver"] = input_df["giver"].astype(str).str.strip()
    input_df["receiver"] = input_df["receiver"].astype(str).str.strip()

    # Check that any people in the excluded pairs file are in the actual
    # participants list
    invalid = (set(input_df["giver"]) | set(input_df["receiver"])) - set(names)
    if invalid:
        raise RuntimeError(
            "Error: These names appear in exclusions but not in the"
            f" participant list: {invalid}"
        )

    excluded_pairs_dict = (
        input_df.groupby("giver")
        .agg({"receiver": list})
        .reset_index()
        .set_index("giver")["receiver"]
        .to_dict()
    )

    return excluded_pairs_dict


def assign_secret_santa(
    names: list, exclusions_dict: dict[str, list[str]], max_attempts: int
) -> dict[str, str] | None:
    """
    Assign Secret Santa pairs.

    Parameters
    ----------
    names : list
        List of names taking part in Secret Santa
    exclusions_dict : dict[str, list[str]]
        Dictionary showing people (keys) who cannot give to receivers (value)
    max_attempts: int
        Number of attempts to run

    Returns
    -------
    dict[str, str] | None
        dictionary of giver as key and receiver as value

    Raises
    ------
    RuntimeError
        If no assignment can be found after the maximum attempts
    """
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        receivers = names.copy()
        random.shuffle(receivers)

        valid = True
        for giver, receiver in zip(names, receivers):
            if receiver == giver:
                valid = False
                break
            if receiver in exclusions_dict.get(giver, []):
                valid = False
                break

        if valid:
            return dict(zip(names, receivers))

    raise RuntimeError(
        "Error: No valid secret santa assignment found after"
        f" {max_attempts} attempts"
    )


def print_and_write_out_results(santa_assignment: dict, outfile_name: str):
    """
    Print results to terminal and write out dictionary of Secret Santa assignment to CSV file.

    Parameters
    ----------
    santa_assignment : dict
        dict where key is giver and value is receiver
    outfile_name : str
        name of output file
    """
    santa_ascii = r"""
          * * *
        *       *
       *  O   O  *
       *    >    *
        *  ---  *
          *   *
       *  * * *  *
     *             *
    *   HO HO HO!   *
     *             *
       *  * * *  *
    """
    print(santa_ascii)
    print("Shhh! Here are the secret Santa assignments:")
    print("-" * 40)

    for giver, receiver in santa_assignment.items():
        print(f"{giver} buys a present for {receiver}")
    print("-" * 40)

    with open(outfile_name, mode="w", encoding="utf8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["giver", "receiver"])
        writer.writerows(santa_assignment.items())
        print(f"Results written to {outfile_name}")


def main():
    args = parse_args()
    names_df = read_csv_to_dataframe(args.input_names)
    santa_names = validate_participants(names_df)
    excluded_pairs = read_csv_to_dataframe(args.exclusion_pairs)
    excluded_pairs_dict = convert_excluded_dataframe_to_dict(
        excluded_pairs, santa_names
    )
    santa_assignment = assign_secret_santa(
        santa_names, excluded_pairs_dict, args.max_attempts
    )
    print_and_write_out_results(santa_assignment, args.output)


if __name__ == "__main__":
    main()
