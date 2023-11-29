import argparse

parser = argparse.ArgumentParser(
    description="Write sequences as text input for the two sequences to compare.")
parser.add_argument('--Sequence_1', '-s1', type=str, 
                    metavar='', required=True, 
                    help='Type in sequence - not FASTA just raw bases.')
parser.add_argument('--Sequence_2', '-s2', type=str, 
                    metavar='', required=True, 
                    help='Type in sequence - not FASTA just raw bases.')
parser.add_argument('-F', '--FileMode', 
                    action='store_true', required=False,
                    help='Set file mode to take .txt files')
args = parser.parse_args()

def Hamming_calc(input1, input2):
    Hamming_distance = 0 #Tracks the number of differences.
    loop = 0 #use as a counter to work out which position to compare.
    try:
        for i in input1:
            if i != input2[loop]:
                Hamming_distance += 1
                loop += 1
            else:
                loop += 1
#This for loop compares the two strings at position loop.
#and if not the same adds to hamming_distance otherwise continue.
    except Exception as e:
        print("Error with input, try writing the sequence as raw bases e.g AACGAATT")

    else: print(f'The Hamming distance is {Hamming_distance}') #f-string to print results

if __name__ == '__main__':
    if args.FileMode:
        with open(args.Sequence_1) as f:
            seq1 = f.read().replace('\n', '')
            print(seq1)
        with open(args.Sequence_2) as f:
            seq2 = f.read().replace('\n', '')
            print(seq2)
        Hamming_calc(seq1, seq2)
    else:
        print(args.Sequence_1)
        print(args.Sequence_2)
        Hamming_calc(args.Sequence_1, args.Sequence_2)
