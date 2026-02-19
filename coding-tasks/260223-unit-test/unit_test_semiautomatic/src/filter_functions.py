#!/usr/bin/python3

#Rationale: filter out functions and arguments from a .py file using the package ast

import argparse
import ast



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
        help="The .py file name to extract functions and arguments from"
    )
    
    args = parser.parse_args()
    return args


#from Zain Ahmad - Medium post
#https://levelup.gitconnected.com/how-i-automatically-write-unit-tests-for-my-python-code-using-gpt-4-and-ast-parsing-c98b210c8e2b#:~:text=import,functions,-This

def extract_functions(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read())
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args]
            })
    return functions

def main():
    args = parse_args()
    print(extract_functions(args.input_file))

if __name__ == "__main__":
    main()