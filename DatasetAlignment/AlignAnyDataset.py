import argparse
import time
import os, re

from Utils import MyIOutils, DefinedConstants, TextProcessingUtils, VectorUtils, MyIOutils
from Representations import ModelContainer, NgramModel, EmbeddingModel


# baseDir = "/path/to/your/dataset/parent/folder/"
# inFile = baseDir+"SimplifiedTextAlignment/WikiSimpleWiki/annotations.txt"
# firstSentIndex = 1
# secondSentIndex = 2
# language = DefinedConstants.EnglishLanguage
# alignmentLevel = DefinedConstants.SentenceLevel
# nGramSize = 3
#
# #similarityStrategy = DefinedConstants.WAVGstrategy;
# #similarityStrategy = DefinedConstants.CWASAstrategy;
# similarityStrategy = DefinedConstants.CNGstrategy
# alignmentStrategy = DefinedConstants.closestSimStrategy
# subLvAlignmentStrategy = DefinedConstants.closestSimStrategy
# outFile = MyIOutils.getOutputFileName(inFile, alignmentLevel, similarityStrategy, nGramSize)


def cleanTest(stringToCleanup):
	chars = "\n;\"'"
	for c in chars:
		stringToCleanup = stringToCleanup.replace(c, ' ')
	return stringToCleanup


def get_settings(param2value):
	nGramSize = 0
	if not bool(param2value):
		print("Error: invalid input options. ")
		print(MyIOutils.showNewselaUsageMessage())
		exit()
	if param2value.get("inputdir"):
		setting = "align_files_of_loop_dir"
		pass
	elif param2value.get("input_complex") and param2value.get("input_target"):
		setting = "align_two_files"
		# run with two files
		# inFileComplex = param2value.get("input_complex")
		# inFileSimple = param2value.get("input_target")
	else:
		print("Error: invalid input. Either add a directory with input field or specify two files to align. ")
		print(MyIOutils.showNewselaUsageMessage())
		exit()

	outFolder = param2value.get("output")
	similarityStrategy = param2value.get("similarity")
	globalSimilarityStrategy = similarityStrategy
	language = param2value.get("language")
	embeddingsFile = param2value.get("emb")
	# linelevel - extra property for handling sentence segmentation per line (to be able to compare with other tools)
	lineLevel = param2value.get("linelevel")
	alignmentLevel = param2value.get("aLv")
	alignmentStrategy = param2value.get("aSt")
	subLvAlignmentStrategy = param2value.get("aSt2")
	model = None
	return setting, outFolder, globalSimilarityStrategy, similarityStrategy, language, embeddingsFile, lineLevel, \
		alignmentStrategy, alignmentLevel, subLvAlignmentStrategy,model, nGramSize


def preprocessing(inFileComplex, inFileSimple, outFolder, globalSimilarityStrategy, similarityStrategy, language, embeddingsFile, lineLevel,
				  alignmentStrategy, alignmentLevel, subLvAlignmentStrategy,model, nGramSize):
	vocab = set()
	aux = None
	if len(globalSimilarityStrategy) == 3 and globalSimilarityStrategy[0] == 'C' and globalSimilarityStrategy[-1] == 'G':
		nGramSize = int(globalSimilarityStrategy[1])
		similarityStrategy = DefinedConstants.CNGstrategy
		model = None
	if similarityStrategy == DefinedConstants.CWASAstrategy or similarityStrategy == DefinedConstants.WAVGstrategy:
		text1 = MyIOutils.readTextFile(inFileComplex)
		vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(text1))
		text2 = MyIOutils.readTextFile(inFileSimple)
		vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(text2))

		aux = EmbeddingModel(embeddingsFile, vocab)
		model = ModelContainer(aux, None)
		if similarityStrategy == DefinedConstants.CWASAstrategy:
			model.em.precomputeW2VcosDist()
			model.em.createSimilarityMatrix()

	elif similarityStrategy == DefinedConstants.CNGstrategy:
		aux = NgramModel(True, nGramSize)
		model = ModelContainer(None, aux)
		text1 = MyIOutils.readTextFile(inFileComplex)
		aux.processAndCountTextNgrams(text1, alignmentLevel, lineLevel)
		text2 = MyIOutils.readTextFile(inFileSimple)
		aux.processAndCountTextNgrams(text2, alignmentLevel, lineLevel)
		aux.calculateIDF()

	return vocab, model, aux, nGramSize, similarityStrategy, globalSimilarityStrategy


def alining(inFileComplex, inFileSimple, alignmentLevel, alignmentStrategy, subLvAlignmentStrategy, similarityStrategy, model, lineLevel):
	# print("Aligning...")
	ini = time.time()
	text1 = MyIOutils.readTextFile(inFileComplex)
	# print(text1, alignmentLevel, similarityStrategy, model, lineLevel)
	cleanSubtexts1 = TextProcessingUtils.getCleanText(text1, alignmentLevel, similarityStrategy, model, lineLevel)
	text2 = MyIOutils.readTextFile(inFileSimple)
	cleanSubtexts2 = TextProcessingUtils.getCleanText(text2, alignmentLevel, similarityStrategy, model, lineLevel)
	alignments = VectorUtils.alignUsingStrategy(cleanSubtexts1, cleanSubtexts2, similarityStrategy, alignmentStrategy,
												model)
	if alignmentLevel == DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel:
		alignments = VectorUtils.getSubLevelAlignments(alignments, cleanSubtexts1, cleanSubtexts2, similarityStrategy,
													   subLvAlignmentStrategy, model)
	output_alignments_simple = list()
	output_alignments_complex = list()
	for alignment in alignments:
		# print(cleanTest(str(alignment.source).rstrip()))
		# print(cleanTest(str(alignment.target).rstrip()))
		# print(alignment.similarity)
		# MyIOutils.saveAlignments(alignments, outFolder + "x" + "_ALIGNED_WITH_" + "y")
		output_alignments_simple.append(cleanTest(str(alignment.target).rstrip()))
		output_alignments_complex.append(cleanTest(str(alignment.source).rstrip()))
		# stats = MyIOutils.getStats(alignments, cleanSubtexts1, cleanSubtexts2,
		# 					   outFolder + "x" + "_ALIGNED_WITH_" + "y" + "_stats.txt")
		# print(stats)
	end = time.time()
	diff = end - ini
	# print("Total processing time: %d min %f sec" % (int(diff / 60), diff % 60))
	return output_alignments_complex, output_alignments_simple

def start(given_arguments=None):
	start_time = time.time()
	parser = argparse.ArgumentParser()
	parser.add_argument('-ic', required=False, help='input_complex')
	parser.add_argument('-it', required=False, help='input_target')
	parser.add_argument('-o', required=True, help='outputdir')
	parser.add_argument('-i', required=False, help='inputdir')
	parser.add_argument('-l', required=True, help='language')
	parser.add_argument('-s', required=True, help='similarity')
	parser.add_argument('-a', required=False, help='aLv')
	parser.add_argument('-t', required=False, help='aSt')
	parser.add_argument('-u', required=False, help='aSt2')
	parser.add_argument('-e', required=False, help='emb')
	parser.add_argument('-ll', required=False, help='linelevel')

	if given_arguments:
		param2value = given_arguments
	else:
		args = parser.parse_args()
		param2value = MyIOutils.parseOptions(args)
	all_alignments_complex, all_alignments_simple = list(), list()
	setting, outFolder, globalSimilarityStrategy, similarityStrategy, language, embeddingsFile, lineLevel, alignmentStrategy, alignmentLevel, subLvAlignmentStrategy, model, nGramSize = get_settings(param2value)
	print(setting, outFolder, similarityStrategy, language, embeddingsFile, lineLevel, alignmentStrategy, alignmentLevel, subLvAlignmentStrategy, model, nGramSize)
	print("setting, outFolder, similarityStrategy, language, embeddingsFile, lineLevel, alignmentStrategy, alignmentLevel, subLvAlignmentStrategy, model, nGramSize")
	if setting == "align_two_files":
		inFileComplex = param2value.get("input_complex")
		inFileSimple = param2value.get("input_target")
		vocab, model, aux, nGramSize, similarityStrategy, globalSimilarityStrategy = preprocessing(inFileComplex, inFileSimple, outFolder, globalSimilarityStrategy, similarityStrategy, language, embeddingsFile, lineLevel,
				  alignmentStrategy, alignmentLevel, subLvAlignmentStrategy, model, nGramSize)
		output_alignments_complex, output_alignments_simple = alining(inFileComplex, inFileSimple, alignmentLevel, alignmentStrategy, subLvAlignmentStrategy, similarityStrategy, model, lineLevel)
		all_alignments_simple.extend(output_alignments_simple)
		all_alignments_complex.extend(output_alignments_complex)
	elif setting == "align_files_of_loop_dir":
		inputdir = param2value.get("inputdir")
		all_files = [filename for filename in os.listdir(inputdir) if filename.endswith("src")]
		for inFileComplex in all_files:
			inFileSimple = inFileComplex[:-4]+".tgt"
			vocab, model, aux, nGramSize, similarityStrategy, globalSimilarityStrategy = preprocessing(inputdir+"/"+inFileComplex, inputdir+"/"+inFileSimple, outFolder, globalSimilarityStrategy, similarityStrategy, language, embeddingsFile, lineLevel,
					  alignmentStrategy, alignmentLevel, subLvAlignmentStrategy, model, nGramSize)
			output_alignments_complex, output_alignments_simple = alining(inputdir+"/"+inFileComplex, inputdir+"/"+inFileSimple, alignmentLevel, alignmentStrategy, subLvAlignmentStrategy, similarityStrategy, model, lineLevel)
			all_alignments_simple.extend(output_alignments_simple)
			all_alignments_complex.extend(output_alignments_complex)
	with open(outFolder+"/"+similarityStrategy+"_"+str(nGramSize)+"_"+ alignmentStrategy +"_"+alignmentLevel+"_complex.txt", "w") as f:
		f.write("\n".join(all_alignments_complex))  # f.write("\n".join(all_alignments_complex))
	with open(outFolder+"/"+similarityStrategy+"_"+str(nGramSize)+"_"+ alignmentStrategy +"_"+alignmentLevel+"_simple.txt", "w") as f:
		f.write("\n".join(all_alignments_simple))  # f.write("\n".join(all_alignments_simple))
	print("Saved.")
	print("Processing Time --- %s seconds ---" % (time.time() - start_time))
