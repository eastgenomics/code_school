# Question 1
from collections import Counter


def count_nucleotides(file):
	with open(file, "r") as f:
		full_str = f.read()
		d = dict(Counter(full_str))

	return '{} {} {} {}'.format(d['A'], d['C'], d['G'], d['T'])

# Question 2
def transcribe_dna(file):
	with open(file, 'r') as f:
		full_str = f.read()
	
	return full_str.replace('T', 'U')

# Question 3
complements = {
    'A': 'T',
    'G': 'C',
    'T': 'A',
    'C': 'G'
}

def complement_dna(file):
	with open(file, 'r') as f:
		full_str = f.read()
		full_str = full_str[::-1]

		result = ''

	for w in full_str:
		try:
			result += complements[w]
		except Exception:
			pass
	return result

# Question 4
def wabbit(month, k):
	rabbits = [0] * month
	rabbits[0] = 1
	rabbits[1] = 1

	for n in range(2, len(rabbits)):
		rabbits[n] = rabbits[n-1] + rabbits[n-2] * k
	return rabbits[-1]

# Question 5
# !pip3 install biopython

from Bio import SeqIO


max_name = 0
max_seq = 0

def gc_count(st):
	gc_count = st.count('G') + st.count('C')
	gc_percent = gc_count / len(st) * 100
	return gc_percent

f = SeqIO.parse(open('/content/rosalind_gc.txt'), 'fasta')


for fasta in f:
	percent = gc_count(fasta.seq)
	if percent > max_seq:
		max_seq = percent
		max_name = fasta.id
  
print(max_name, max_seq)