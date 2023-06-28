from evaluate import evaluate
from DatasetAlignment import AlignAnyDataset


def merge_n_to_1(complex_lines, simple_lines):
	output_complex = list()
	output_simple = list()
	i_simple = 0
	i_complex = 0
	while i_complex < len(complex_lines) and i_simple < len(simple_lines):
		complex_sent = complex_lines[i_complex].strip()
		j_complex = 0
		while i_complex+ j_complex < len(complex_lines) and complex_sent == complex_lines[i_complex+j_complex].strip():
			j_complex += 1
		if j_complex != 1:
			output_complex.append(complex_lines[i_complex].strip())
		else:
			output_complex.append(" ".join([sent.strip() for sent in complex_lines[i_complex:i_complex + j_complex]]))
		output_simple.append(" ".join([sent.strip() for sent in simple_lines[i_simple:i_simple + j_complex]]))
		i_simple = i_simple + j_complex
		i_complex = i_complex + j_complex
	return output_complex, output_simple


def merge_n_to_n(complex_filename, simple_filename):
	# todo problem n:m currently only 1:n and n:1
	with open(complex_filename) as f:
		complex_lines = f.readlines()
	with open(simple_filename) as f:
		simple_lines = f.readlines()
	output_complex, output_simple = merge_n_to_1(complex_lines, simple_lines)
	# output_complex, output_simple = merge_n_to_1(output_simple, output_complex)
	with open(complex_filename.split(".")[0]+"_complex_clean.txt", "w") as f:
		f.write("\n".join(output_complex))
	with open(simple_filename.split(".")[0]+"_simple_clean.txt", "w") as f:
		f.write("\n".join(output_simple))
	return complex_filename.split(".")[0]+"_complex_clean.txt", simple_filename.split(".")[0]+"_simple_clean.txt"


# python main.py -i data/deplain/documents -o data/deplain/output  -l "de" -s "C3G" -a "sentence" -t closestSimStrategy -ll line
method_name = "CNG_3_closestSimStrategy_sentence"
params = {'inputdir': 'data/deplain/documents', 'output': 'data/deplain/output', 'language': 'de', 'similarity': 'C3G', 'aLv': 'sentence', 'aSt': 'closestSimStrategy', 'linelevel': 'line'}
AlignAnyDataset.start(params)
print("default", "without_identical", False, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt"))
print("default", "without_identical", True, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt", without_identical=True))

simple_f, complex_f = merge_n_to_n("data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt")
print("n:m", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f))
# print("default", "without identical", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt", without_identical=True))
# print("n:m", "without identical", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f, without_identical=True))

# python main.py -i data/deplain/documents -o data/deplain/output  -l "de" -s "C3G" -a "sentence" -t closestSimKeepingSequenceStrategy -ll line
method_name = "CNG_3_closestSimKeepingSequenceStrategy_sentence"
params = {'inputdir': 'data/deplain/documents', 'output': 'data/deplain/output', 'language': 'de', 'similarity': 'C3G', 'aLv': 'sentence', 'aSt': 'closestSimKeepingSequenceStrategy', 'linelevel': 'line'}
# AlignAnyDataset.start(params)
print("default", "without_identical", False, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt"))
print("default", "without_identical", True, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt", without_identical=True))
# simple_f, complex_f = merge_n_to_n("data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt")
# print("n:m", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f))
# print("default", "without identical", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt", without_identical=True))
# print("n:m", "without identical", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f, without_identical=True))
#
#
# python main.py -i data/deplain/documents -o data/deplain/output  -l "de" -s "CWASA" -a "sentence" -t closestSimStrategy -ll line -e data/de-word2vec/vectors.txt
method_name = "CWASA_0_closestSimStrategy_sentence"
params = {'inputdir': 'data/deplain/documents', 'output': 'data/deplain/output', 'language': 'de', 'similarity': 'CWASA', 'aLv': 'sentence', 'aSt': 'closestSimStrategy', 'linelevel': 'line', 'emb': 'data/de-word2vec/cc.de.300.vec'}
AlignAnyDataset.start(params)
print("default", "without identical", False, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt"))
# simple_f, complex_f = merge_n_to_n("data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt")
# print("n:m", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f))
# print("default", "without identical", True, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt", without_identical=True))
# print("n:m", "without identical", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f, without_identical=True))
#
#
# # # python main.py -i data/deplain/documents -o data/deplain/output  -l "de" -s "WAVG" -a "sentence" -t closestSimStrategy -ll line -e data/de-word2vec/vectors.txt
# # method_name = "WAVG_0_closestSimStrategy_sentence"
params = {'inputdir': 'data/deplain/documents', 'output': 'data/deplain/output', 'language': 'de', 'similarity': 'WAVG', 'aLv': 'sentence', 'aSt': 'closestSimStrategy', 'linelevel': 'line', 'emb': 'data/de-word2vec/cc.de.300.vec'}
AlignAnyDataset.start(params)
print("default", "without identical", False, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt"))
print("default", "without identical", True, method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", "data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt", without_identical=True))
# # simple_f, complex_f = merge_n_to_n("data/deplain/output/"+method_name+"_complex.txt", "data/deplain/output/"+method_name+"_simple.txt")
# # print("n:m", method_name, evaluate("data/deplain/gold_data.src", "data/deplain/gold_data.tgt", complex_f, simple_f))
#
