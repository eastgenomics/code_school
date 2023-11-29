#!usr/bin/env python

"""
ROSALIND
Counting Point Mutations
Topics: Alignment
Evolution as a Sequence of Mistakes

Given two strings s and t of equal length, the Hamming distance between s 
and t (denoted dH(s,t)) is the number of corresponding symbols that differ 
in s and t.

Problem
Given two DNA strings s and t of equal length (not exceeding 1 kbp), return
the Hamming distance dH(s,t).

Sample Dataset:
GAGCCTACTAACGGGAT
CATCGTAATGACGGCCT

Sample Output: 7
"""

from random import choice, randint


def use_example_strings():
    # Define the sample strings as variables
    string_1 = 'GAGCCTACTAACGGGAT'
    string_2 = 'CATCGTAATGACGGCCT'

    # Get the length of the strings
    string_length = len(string_1)

    return string_length, string_1, string_2


def get_strings_from_file(filename):
    # Get the contents of the file (as a single string)
    with open(filename, 'r') as file_object:
        file_contents = file_object.read()
    
    # Split the string on newline characters and get the number of strings
    contents_list = file_contents.split('\n')
    string_count = len(contents_list)

    # Check there are only 2 strings to compare
    if string_count != 2:
        print('Error: Script requires 2 strings, {} were submitted.'.format(
            a = string_count
            ))
    
    else:
        string_1 = contents_list[0].strip()
        string_2 = contents_list[1].strip()

        # Check the strings are the same length
        if len(string_1) != len(string_2):
            print('Error: Strings must be the same length.')
        
        # Check the strings are 1kb or less
        elif len(string_1) > 1000:
            print('Error: Strings must be 1000 characters or less.')
        
        else:
            string_length = len(string_1)

            return string_length, string_1, string_2


def generate_random_strings():
    # Specify which characters can be used to create strings
    characters = ['A', 'C', 'G', 'T']

    # Generate a random number to determine how long the string will be
    string_length = randint(1, 1000)

    # Generate two strings of that length by randomly picking characters
    string_1 = ''.join([choice(characters) for i in range(string_length)])

    string_2 = ''.join([choice(characters) for i in range(string_length)])

    return string_length, string_1, string_2


def get_unmatched_positions(string_length, string_1, string_2):
    # Print the strings which are being compared
    print('Two strings of length {a}: \n{b} \n{c}'.format(
        a = string_length,
        b = string_1,
        c = string_2,
        ))

    # Initialise output variables
    unmatched_count = 0
    unmatched_positions = []

    # Identify the number and position of characters which don't match
    for i in range(string_length):
        if string_1[i] != string_2[i]:
            unmatched_count += 1
            unmatched_positions.append(i)

    # Print the result
    print('The strings differ at {a} positions: {b}'.format(
        a = unmatched_count,
        b = unmatched_positions,
        ))


def main():
    # string_length, string_1, string_2 = use_example_strings()
    # string_length, string_1, string_2 = generate_random_strings()

    string_length, string_1, string_2 = get_strings_from_file(filename)

    get_unmatched_positions(string_length, string_1, string_2)


if __name__ == '__main__':
    main()
