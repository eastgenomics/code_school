#!/usr/bin/python3

#Rationale: create prompt for ChatGPT to create unittest using pytest given a fucntion name and its arguments

import argparse
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
        "-i_function",
        "--input_function_name",
        type=str,
        required=True,
        help="The function name to create unittest from"
    )
    parser.add_argument(
        "-i_args",
        "--input_arguments_name",
        type=str,
        required=True,
        help="The arguments names to create unittest from"
    )
    
    args = parser.parse_args()
    return args

#Edited from Zain Ahmad - Medium post
#https://levelup.gitconnected.com/how-i-automatically-write-unit-tests-for-my-python-code-using-gpt-4-and-ast-parsing-c98b210c8e2b#:~:text=framework%2E-,def,outputs%2E%22%22%22

def create_prompt(function_name, args):
    print(args)
    return f"""
Write a Python pytest for the following function:def {function_name}({args}):
    # Function body is unknown
Use standard unittest structure with mock inputs and expected outputs.
"""


def main():
    args = parse_args()
    print(create_prompt(args.input_function_name, args.input_arguments_name))

if __name__ == "__main__":
    main()