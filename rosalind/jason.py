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

## Question 7
# http://saradoesbioinformatics.blogspot.com/2016/06/mendels-first-law.html
# https://stackoverflow.com/questions/25119106/rosalind-mendels-first-law-iprb

hom = k = 15
het = m = 19
rec = n = 20

# AAAA & aaaa & AaAa
# AAaa AAAa Aaaa
combination = ['AAAA', 'aaaa', 'AaAa', 'AAaa', 'AAAa', 'Aaaa']

# probability of dominant allele
punnett_probabilities = {
      'AAaa': 1,
      'AAAA': 1,
      'aaaa': 0,
      'AaAa': 3 / 4,
      'AAAa': 1,
      'Aaaa': 1 / 2
  }

event_prob = {}

# total population
totals = hom + het + rec

# calculate probability of each event
P_kk = hom / totals * (hom - 1) / (totals - 1)
event_prob['AAAA'] = P_kk

P_mm = het / totals * (het - 1) / (totals - 1)
event_prob['AaAa'] = P_mm

P_nn = rec / totals * (rec - 1) / (totals - 1)
event_prob['aaaa'] = P_nn

P_km = k / totals * m / (totals - 1)
P_mk = m / totals * k / (totals - 1)
event_prob['AAAa'] = P_km + P_mk

P_kn = k / totals * n / (totals - 1)
P_nk = n / totals * k / (totals - 1)
event_prob['AAaa'] = P_kn + P_nk

P_mn = m / totals * n / (totals - 1)
P_nm = n / totals * m / (totals - 1)
event_prob['Aaaa'] = P_mn + P_nm

# overall probability of dominant allele
total_prob = 0
for event in combination:
  total_prob += punnett_probabilities[event] * event_prob[event]

print(total_prob)

## Question 8

# probability of dominant allele offspring
# assuming each couple produce 2 offsprings
comb = {
	'AAAA': 2,
	'AAAa': 2,
	'AAaa': 2,
	'AaAa': 1.5,
	'Aaaa': 1,
	'aaaa': 0
	}

seq = comb.keys()
input = [17677, 19464, 17724, 18168, 16351, 17000]

total_offspring = 0

for i,com in enumerate(seq):
  num_couple = input[i]
  total_offspring += comb[com] * num_couple

print(total_offspring)

## Question 9

codon_table = {
	"UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
    "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S",
    "UAU":"Y", "UAC":"Y", "UAA":"STOP", "UAG":"STOP",
    "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W",
    "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
    "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
    "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
    "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
    "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
    "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
    "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
    "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
    "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
    "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
    "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
    "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G"
	}

input = 'AUGGGUAAUUUGAUGUUGGGUACCAGCCUGAAUGCUACCGUGUAUCACUACCGUAACGCACACGAGGAUCGCCUUCAAAGACUAGGCGGCCACAAGUCACUGAGCCGAAUAAUUAUCCCGUGCGCCGCUGAGGUUCGGUCAUCUGUGACAUUAUCCUGCGACGAGUCCUGGUAUCUGACGUCUGCAAGCUGGAGAUACGUCGCAGCUCGAAACUUUUAUCAGCGUGAGGAAAUAAAGCUACCAUCCCGUUGCCGACGAAGUUCUGUUGAGUUAGAAUUUGUGAGAUACCCCAGGUUCUCCUGCCAGUCGUGUUCAGUUCAAGUGACAUACGUACUCAGCCAAAGAUCUCACUAUCUGCCUCCCAGUCAGGUUUUGGUAUGCAUGAGUUGCUACCGAUUGCCUGCAGAAACCACAACGAUGAACUACAUUCCCCUCGUGGAACAUUUCAUUAAUUCAGUCGUGUUUUCCAUACAUUCUUACAUGAGUUUGAAUGAAGAUAUGGACACUAGGAUGAGAGUCUUUUUCACUGGCGCGCGAGUUACGUUAACUCGUCGCAGUCCAAUUACUGACUUACCACGACGGUGUAUGGUGCUUCAGAACGAAGGGAGAGAGGUUGGGCACAACCCAAGCUGCUUUGUCGUCCUGUGCGUAUGGGGGCCCAUGCGAGUUUGUGGGAGCCUCUGUGUGGACUUGUUCAUCCUCGCAGAGUCGCUACGACAAUUGGCCUCAUCCCGGACAAUAAAUAUAGUAUACACAAUUACAGUUCACUCCCCAAAUGUUGUCGGCCGUGCGCAAAGCGACACUGAGAUUACUGGCUCAGUAAGUAUCGCGGUCUGUAAUGGACUUAGACCGCGGUUUGAGCUAGUACAGAAUAAUAUCAGUGAGCUGUAUCGACGUCUAUGUUAUGCCAGUAUGUUGGACAAUCGUGGAAAAGGUAAAUGGAAAGAAACCACGAGAUAUUACACGAAUCACUCGUUCACCUCCUUGAGGAUAACACCCGAGAGUGAGAGGUGUGGGGAUAUCUACUCGCAUAUGAGCGGGAACUAUUGCGGGCUGUACGCAACGAUAUUGUUAGCAGAAGAAUUCCUGUGGCUUGUUAGACGUCAGGCGAAAUGUUAUCACGAUCUUCAAACUAUGCGAGGUUGGCCGGUGAAUUCUCUGUUUGACCAAGCUUACAGUGAUGUAAGAGCCGCGAUUCGCCGUAGACGAUGCCCGGGAUGCCCGCCCCCAGGUGGCCGGGUGCAUGUAGACUUAAUCGCGCGAGCAUAUUGUGAGCUGGCCUUUGCGACCGCGAGACCUUAUAUAGAACUGUCUCUCGCCAUCUCAAUUUCAUUUGGGUAUGCGGCCUUAGUGCGCGUAUCACAGGGGAAGAUAUUUGCAACGUGUAUUUGGAUAUACCGUAAAUCCAACUACCUCUUGGGGGUUAAGCCUAGAUCCCCCAGGGGCACAAGUUUAGACAACUUGGAAACAAGUGCUUCUACCUGUACGAGUGAGAGCAACGCGUUGGUGGUUCCCCGAACCUGGCGAAGAGCCAUGAGUCCCUCCAUCCUGCCCGUGUCGGCCAUCACUCGUCUACAAACUGAACUCCUUCCGGUCGAGCCCCAGUAUCCGCUUUGCCUAUAUGCGCCCACGUCAGCGGAUACUGUAGAGAAGGGAGAGUCCGGCCUCUGCACACUUGCGAUAUUCCGAACAUUACACGUUGCAACAUCUGAACAUUUCUCAUUCGUUUACGCCCAAAGUUAUACCAAGUGCACUAGGGUGUGCUCUCUACACAUCACACACAGCUUACCAGCGCUCUGGUUGAAGCAUGGCAGCCCUGAUGAGAGUAUACCCGAAGGAAAGUGCGCGUGGGCGACUACUAAUCACAGAGUUCACCGUGAUUCGCGGGUAGACAACCAAUUCAUAGACGCGAUUAAAUUGCUAUCAGAGUAUACUCAACGACGAGUCUGUAGUGCGAGAAUGAACUGGCCGCUCAUGUCAGCCCAAGCUGGGUCCCAGCAUUCUGAGACGCACCAUAUGCCGAUAGCUGAACUAUGCGCCAUUGCUUACCCGGCCCGAGUGUACUCCGGUUCUAACUCCGCCAUAUUUCUCCCUCCAACGCCGGUCCGACCGAGCAUCCCUCGAGCUACGCCCUACUUCUCGCGAGGUCUUAGGAUUUCGUUGACUACCAAGUUGAAGCCCUCCGGCGCCCCACAGGGGGCUGUUCGCUUGUUGCAAAAGAGGGGACGGCUUCGUCCUGUAUGCCCCUAUAUCCCGAGUUCCGAAGGUAACAAUCGAAAUUACGGAUGCGUGCGGUGGGGCAUGGGUUUUACGUCCAACGGACAUCUGGCAGCUGUUCCAUUCAACUGGCCGGAAGAGCCGACCGCAACCGCCAGUGUUCACCCGAACCCGCAGGCUCGAGAUCCAUGGCUGCUUGCAAUUCAGACGCAACCGAUACGAGGAGUCUCCAGUGUGUCGGAUCUCGUUUUGAUAGGUGCCUUUACGCGUACAAUCAGGGUGAAGGCCUGUUUGAUGGCUGCCGGGUCGAGCGCGGAAUCUGGACUCUCCCUGCUCUCCUCACGGGACAUAGUAUUUCGCGAAUCGGAAAAUGGGAGGUACUAUGACAUAUGCAUUCUCCUCUUCCUUGUGUUGCUAUCUCAUAACCAAGUACUAAAAUACAGGAAUAUUGUAGCCCAAGGCGAUGACGCAUGUACCAAGAGGUGCUCCACGCACUACCAUGAAGUCGAGGUGUUAACUAAACGAUUUAGCGGCAGGACGACCAGACGUGCGAGAUAUGCCUGCAGCGCCAGUGGCGGCAUUGGCCUACUGACCGGCAUUACCGAUAAGCAACGUUCAAUACAGUCGGUCUAUAUGGAAUCAACUCCUUGCAGGUUAGGCAAUGGGGUUGAAACGCUAUGGGAUACUCCCUCGGUGAAUGCGCUGCUGAAUCAUGCGCGCUCUCAUCGGGAUGGAUUUCACGUACAGUUGGAUCUGUACUUAAGACCGACUCAAAAUCACAUAAAAAAUCCAGAGAUUACUGGUACUGGAAUGAAUAUUCCCCCAGCACCUAAGAACUCUCUGCCCAGACCCCGUAGGGGCGACUGUGAUACGUUGGAUAAUAAUAUGAUAAGCAAUCUUCUCGAUUAUCCGGAUGUGCUGGAGACAGGGGGGAUGGGAGAAUGGCCGGCUGAUCAUCACUGGCCGACGUUUAGAAAGCGACACUCGCGCAAAUGGGCUAUGCUGCUGGCGGUUCUCGAGCCACACUGGAACUCCCUUGACUAUAAGGCGCUGACCUUGCCCUAUCAAAGGGCAACCGGUAACGUCACCGGAAAUGGAAUUAGAAACGUCCUAAGUUUGAUCCAUGGGAUACUGCAACCGAGACCUCAUACCCCAGUUUCCAAUUCCCCAAGUGGCUCUCAAGCAGUCGUUUCCCGAUUCCCGUCUAGCACUCCCAUAUCCGACCGACGUGGCGGAAGUCGGAGGCUCCCAUGGCCUGAACCGAUCACCGUAGGGCGUCGCUUAUAUAUAAUGAAUGAGGCUAGGUCGCAACCCAUGCUUGAUUGUAAAACCUUCUUUCAGUUCGUCGUGGCUCUCUCUGAUCGGCCAAUGUGUGUGAGGCCGCAACGGGGGGUGGGAACCACGGGCACAUUCAGUAAUCAUAUUCGUUAUGUCGUCCAUAAAAGAAUACCAGCAACUGAGGCUGAGCAGAUUAGCCGUCAAGCAAUAGCUACGUUAUUAGCAUAUUCAAACUGCCUCUUGUCACUUUUCAUUCAAAGUUGUCCUUGGCUGGUUGUACGCUGGUUAGCUUCUACCCGCCCUCCGAGGGAUGUCCACAGGCAUGACAACCACGACCGAGAACUACAGGUGAUCCGCCAAUACCUAGCGCUUGUACACCUUGUCUGUCACGUCUCGAGUAUGUCCCAUGUGAAAUUGCGGGCACUAUUCCUAUCCCACAGGCUCGGUCCGGAACCGAGAACAAAUUGGACCAAGCUACCUCAAGGGGUAAGCUACAAAGAGUCGCAGUACCUCCCUGCAUAUUUCAAUACGUCCCAGUCAGCAAAUUCGUACAGAUCAGAAUCACGAGAGGAGGAGGGCCCGGUGGGUGCUCUUACCUUUUCUUGUCGGAAAUAUCACACGUCGUACGUUGAACAAGAUCGGGGUCAUUUUGGUUACAGCGUGCGUAUACGGCGGACUUCUCGGCUCAAUAUCGCAGUAGGUAGCACUCGACCACGCCUCUGUUUUCUCCCCCUCCUCGUCCAAUUCUCGGUGAAAUUGUGGCAACUGGCCUGGGUCCCGACGCCGAUGGAAUUGUGCAUGUGUCUUGUAAACUUUUUAAACGACAUGGCUCAACACGGACGCCCCUGCAUUUUAGCGAUCCAUCAUACCCUGGGAUAUCUGAAGUACGCAGACUUCCCUUCGAUCUUCCAAGCGAAAGGAUUACUUGAAGGUGAGCUACUAGUGAUAGAAAUGACCCAUAAACGCGCCGUAGUUCAGGAGUUCACCGUACUUCUCCGGAGACGACAAGGAAAAGGGAAAUUUCUUAUCACUCGCAUGCCUGCGAGAUUCACCCAAAUUAGGUGCCUAGACGUUUCGCGUAACGCCACAAUCGCAGGUAAAUUCCAGGUCAUUCGGAGCGUACCUGUAUUCCUCCCUGACACUCGUGUUAUCACGUUUGGCGUGUGCCUGGCGCUUUGCGAUUCGCGCUCCUCUAACGUAUUCCACGCCCUCCGAGCACAUUGGCUUGAUAUUUAUUCUUGUCUGAUAGUGAAAGCAAGUUGGCGUAAACAUCCUUCCACCCUUACGUACGGGUGGUGGCACGGUGGCCGGGUCUUUAACUUGCGUGACGCGACGGAGUUGGCUGCGUUGCCUCAUCUGUCGUGUAAGUCGCUUGGGCAGGGACGAGAUAGAGGGCGCGGGGGUCGCGAAGGUAAUACAUUAACUGACCGCCGGCUGCAAACUUUGCCUCGGACUGCGAUUGGGAACAUAUUCCGGAUCGGUAAAAGAGUGGACGAUCUCCCGCACGAACAGCGCCCUUCGGGUGAGGUCGCCCCUCAACCUCGUCCCAAGAGUAUACAGGACUCUCGCCCGCUUAUAUUUGGCUUCACGCGAGGAAGGUGUCCGCUGUCGCCGGAAGCCGUCAGUGCACAAAACAAGCAAACUUCGGAGACCGCCGUUCAAACUUGUAUAUGCCGGCUAGCCCAGUGUUACUGGCCGAUCUCCGUCACGAAAGCGACCCCGGAGGCCCUGACAGGCGCAUCGGAGUGCCUUAUGUUGCUGUGGAUGAUAAAGAAACCCGCAACGUUGCGGAGUCAGAACAGUGGAGCAUAUUGUGAUGACCUCAUCUCUCCUCCAAUAGGGGGUUGUCUAGCUGUCAUGACGGGUCAUUGCUUGAAUUCUAACUCAGCAUGGCUACCAGAAGAUUGCAGAUGCCUCGUUCUUAAGUUCACAAAUGUACCCUUAGAAGAAGCCCGUAAAACGCGAGGAGCCUGGAUUAGCCUAAUCUCGACUAAUUGGAUCGAUCCUUAUUUUUUUCUAUAUGGGACACCACCGCCCCUACAAUGGGGCUCGACGAGAUGCGUUCCAUGUCUCCUCGGAGUGCCGCCCCGGUAUUACCACCGUAGUAACGGCGGACACUCUGAGGCAAUAUGCAAGGGUCGGUGCUAUACCUGUUACUCUUGUGGAUCACGGAAGUCUAAGCUCUGCCCUAUAUGGUACGAAAUGAGUGCUAAAACCUUUGGAUGCAGACUUAGCGAGUGGAGGCAGCCUAUAAAUUCGCUUUUCUUCUCAUCCGGGCGUACAUCUCGAAUCCGUAAAGUAACGUUCAACCCCGUCGCUUUGUAUGAUGACGUGAGUAGUGCUUUAUUAGGGUAUUUUUUUACCGCCGACAUAUUGGAAAAUGCGGCGUUCACCGACUUCGGCAGCGGCUCAAUGCUUGCGCAUAGUUAUGUGCCACCAGAAAACUCUACGAUAGAUACCAGGGUUGCAAGCCGGGUAGGGUCGAGCCUGUGUUGCAGGAGGUGUACCUUGGCUUUAAAAUACGGGGUCUUGUGCCAUGUGAUGGAUCUGUCGAGUCCCCUUGUAAAUAGUGGUAAGUUGUCAACAAGACAUCCCGGGUCAGGAACCUGUCUCACGUAUCAUGGCGAAAUGACCGUCUCCGGCGUCUCCCUAGCCAUGAGCUCAAAGGUUCAAGAUAUGCUGGGUUCAAGCCAAGGCGGGAACUGCCUACGGACCUCGUCGGCAGAAACCAUUCCGCCAUUCCUCGCCCCUAUGGACACAGUCCGGUACCGGUGGCGUGUCGCGGCGAUAAUUCUCCACGUGAUGUCGGGCAUGGGACGACUCACGAGAGGAAGGAACGUCAGAGCGCGUGAUAAGACCACUUUUUCAAUAGAUCUCCGUAAGAAACCUAUCGGGUCGACACGAGAAACCCGCGCAUUGAGCACACCAAGUCACCCGCGCGCGCGCUUAGGCUUCACUAUCCCUCAACCAACGCGAGUCGUUGGCAGCCGCUCAGCCGAACGCGGAUUACCGGGGGCAUACCUUUGCGCUGUGCGCAGCUUGUGCUUGGCCUAUACCCGUGGCAGGAAGCUUUCUGCAGAAGGCGAUCUGCGCUGUGGUGAGGUUGUCACUAUCUAUUGGCGAUCAUCGGACCAAUAUGUCGCAGGGAUGCUGUCAAGCCUCGAUGUGACCUUCUCCUUGGGUAAUACGUUUGUCCCACAAUCCCAAUGUAACCUAAGACCACCUGAUGUUACGCAACGUUCACCGGUCUUCUUGUGGGUUGCUUGUCGCUUUCGCAUCCGGGUUGUUAGCAUACUCCCAUGGUCACCUCUAUCUCCUUUCGAGUCAUUAAUGAGGUACUGCUUUGUCUCAAACACGUGGUUUUCGGCUGCACUGGAGGCAUCGAAGUCCUACACUUGUACGUCGUCCGAAAUGUAUUCGAACGCAGCACUAAGCAAUUUAAUCCCGAACUACGUGCAGUCACGGUAUUCCUCAACUAUGUCGGGCAUAGGUAAUCGUGAUCACACCAAAUUACGACGCACGACAAAUGGAGAAACGAGCCGUGGCACGUUCCGGUGGCGACACUCUCCAAACAAUGUGUCUUCGUUUGCGGAUGCCUUGGAGACGAACUGUAGGGCCCUGGUGCAAAGGAUUCCUGCCUGUGCUGCCGGACAACAAGUCUGCCAAAGUGAUGUUCCGGGCAGGGGAGCACGGAGUAUAGCCCCCUCCAGGUGGCCCUAUAAGUUAAAUGUGCUCCGAAAGGUUUACCACUGCAGAGAAAGCGGCGGAAAGUACAUGGGGCACGGAGGUCUAGUCGACUCUACCGCAUGGACUGUGGUAAACCGAAUGAUUGAGCUACGACAGUAUCGCAACAGCAUCAUGGCCGUCCUUCAUGUAUGCAAUAUCCUCUCUAGGGGCACUCUAGAGAUUACUCUCUUCGAUGGUAUCCCGCUGUUAUCUCCCCUUGUGACACGGGGCAUACUACAUAAAAGCGACGGAUCUGACUGCCUAGCCGUUCUAUCCUUCUAUCGAUGGCAGCCUAGCGUUCUAAGUGCCCGGUUUGAUGAUGGCAUGUUGCUGGGACGAUUCGAGCCCUGGAGCACCAUGUCUGCAAAGAGAUCUUUGAUAUGGGCAGCGCCACGCAUACCACUACCUGGGUGCAUGGGGCGCGGCAAAGUGUUAACCCGCGAAUUUACUGCCAUCACCGCCGGUACUCUGGUCCUCAGUGAGCUCGCAACCUGUCGCGGCGGAGGCAGCCCUCUGUACUGCUCGUACCGAGGGCGUUGUUCUACAAGGGCCCAACCGCUGGUGCGCAUUACAGGCUGUGUGCUCUCGCGGCUGGACAGUAAAUGCUUCGUAGCCGCAACAAGCCGCCAUCGUGAGAUCUGUCAGACGGAGCCGAAAGGGCUGUGGGCUUACCCUCUAAUUGGGGCAGUAAGAGUAUUGUGCUCUGGCUUUCGAUUAGCAUCCUGUAGCGAACGGCAUGAGCUACCCUUCGGUCGCUGGUUAGCCGUUGUAGGCACACGAUUGUCGCGGGCGAACGCUAUUGUCCCGAUACUCCGUCAAAACCUGGGCGUGUUUAUUCCUGGCACAGCGCUGAACUCUAAGUACAGACUCAAGGACCCGUUCCCGGCAAAAUGCAGCAACUUUCCGCCAAUAGGCAUCGCCAGCAGAAAUCGAAGUUCCGACAUAUAUAGUAAUAGCGGAACGCUCCAAUGUGACAGUGUGAAGGCCAGAAGAAACCCCAAAUUUUUUUAUCAGGAAAUGUCGUACGCCGAUGACCUUGUUGAUGCACCUUAUGCCGCCUGUGCAAUAAUUCACUGUUCAACAAAAUGGCCGUUUGGAGAGACAUGGCUAGGCACGUUCCACCGUCUUGGCUUUUACUUAAUCUAUCCUCAAAGCCGGCCAAUUUUGCGUCGCGGCUACAAGUCCGGCGGUCGCAACUAUAACCCAUCUGAGCUUCAGACCAGUUAUUCGACACUCACCCGGCGUGAGCUCAGAAAAUAUACGACUGGCGAGGGAAGUGUAGUCCGGAUGUCAUAUGUAUUACCUCGCGAGAUAGUUGGAACGUAUAAUUACGAAGCAUACCGCUGUAGGCUAUGCCUAAAAUGCGCUCUAGUAGAAGUUACCUUAAACGUCGCUGGCGGCUAUGGCCAGCCUACGAAUUCACGUCAAGAACGCUUGACACGAUGUGGCUUUAAAGCCCGUGGUUACCCCGUGUUGGUCGUUACAUAA'
final_output = []

# sliding window size
window_size = 3
k = 0

for i in range(len(input) - window_size + 1):
  seq = input[k:k+ window_size]

  if seq in codon_table.keys():
    if codon_table[seq] == 'STOP': 
		break
	final_output.append(codon_table[seq])
    k += 3

output = ''.join([x.upper() for x in final_output])
print(output)

## Question 10

input = 'MMEDDGQMGVELCKKNQCYAMIMAMPGPSKMFCMDNEQPKVFGGSIYGMAWIAYSFRDQSTSDNSYRTWHTNNLTTTCMKWMMPVSWHYSNWASLHHYAHWHEWGQKFCLTCQMCMTTSREPKYRIQFSQWFTQQFKPNNWFLNTGFRCWMHNVCLTFMWINTEENCELEAAWLVHGLESKNPDVAWKHHMYDPCQQYPQRNMHNTCTHKMKRSNQWKQQCRSLVCGSIVIVKICMTRFLCALGHHGRRIANLLKPHFFRACHCIVQFSMSITRRINHALSSQLHKLCHEQKTFITYNCTISDEAFSPWQKRTQGKRIKHTVTMPCGIFPTGTSLCQKHYERYCSEPSYQDWVNYYTERNAIYVQRGQMMHEWGFNMMHDCHCAWDVILGNKCYFYQVIMYRWKRGNLMLMHDNNQNIESTAFRVMTWAFPCSEFGKEWMSMKSGDWLQWVCMMEWRINAAMVPHWNNATCWYMEQCNCMWLRAKITIQPGYTKLHYENSHYFVREPFWHTVAYFLPCFQAVYWYTMCPVFYGYLVWIVLTGPPTKWCWFAPMTVVVMDRINKCCQFDVHHQPRRFTFNMRFLNIWIAMPHIRYSEAVFCLIPKDMPIIWVQRPQLFSDVGIILCHLMDQARYWDFWRIDCENFRMWYVAITQVDRYPLNCAKTTKTKSIEQWDEAPTGKGTSISVVGTCAGEGGGGRREDMPPCFLDTEILTMSGPWWLQFDWSHSQVFVDWLQANSCKLKEWVEFEGIEWLGYWTSMCQNIRLLNQVTGYMLWFEDYYCVPKQFWICVQAMLHVMAWLAWTSCEMQEKGYDLMINTYRHYHFGAWQENSVHPLNNPDNFGNFMCLGTKFVNNKAKPSMPHITRAESAKGVQGPDKDICTWETRTIKWVHHVPATMIDLEIGNKMVYRWWEQICITLTRVFCHVVWSAWVKSTVWDFSALIKPCCFCCAFHDDLSLESTGHCHNKWHENPQVYINLGVRVARIRSQFTNYVGRQVCW'
totals = 1

for n in input:
  num_of_translation = len([i for i,j in enumerate(list(codon_table.values())) if j == n])
  totals *= num_of_translation

totals *= len([i for i,j in enumerate(list(codon_table.values())) if j == 'STOP'])
print(totals % 1000000)