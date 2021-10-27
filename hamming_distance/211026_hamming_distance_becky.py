#!usr/bin/python

"""
ROSALIND exercise to calculate Hamming distance
Takes .txt input file from Rosalind with two sequences on two lines"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
    strings=file.readlines()
    firststring,secondstring=[line.rstrip('\n') for line in strings]

def hamming_distance(string1, string2):
    """Takes two strings of equal length and computes distance"""
    #Check strings are same length
    if len(string1) != len(string2):
        raise Exception('Please ensure strings are the same length')
    #Return sum of each time the zipped tuple letter pair is different
    return (sum(i!=j for i,j in zip(string1,string2)))

print(hamming_distance(firststring, secondstring))
