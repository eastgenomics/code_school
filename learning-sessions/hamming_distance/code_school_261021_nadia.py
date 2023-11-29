#hamming distance
s = "GAGCCTACTAACGGGAT"
t = "CATCGTAATGACGGCCT"


def hamming_distance(s, t):
    if len(s) != len(t):
        print("DNA strings are not equal length")
    else:
        hamming = 0 
        for position in range(len(s)):
            if s[position] != t[position]:
                hamming = hamming + 1
    return hamming

print(hamming_distance(s,t))