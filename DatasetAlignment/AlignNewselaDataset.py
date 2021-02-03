import argparse
import time
import os, re

from Utils import MyIOutils, DefinedConstants, TextProcessingUtils, VectorUtils, MyIOutils
from Representations import ModelContainer, NgramModel, EmbeddingModel


baseDir = "/path/to/your/dataset/parent/folder/"
inFile = baseDir+"SimplifiedTextAlignment/WikiSimpleWiki/annotations.txt"
firstSentIndex = 1
secondSentIndex = 2
language = DefinedConstants.EnglishLanguage
alignmentLevel = DefinedConstants.SentenceLevel
nGramSize = 3

#similarityStrategy = DefinedConstants.WAVGstrategy;
#similarityStrategy = DefinedConstants.CWASAstrategy;
similarityStrategy = DefinedConstants.CNGstrategy
alignmentStrategy = DefinedConstants.closestSimStrategy
subLvAlignmentStrategy = DefinedConstants.closestSimStrategy
outFile = MyIOutils.getOutputFileName(inFile, alignmentLevel, similarityStrategy, nGramSize)

embeddingsFile = baseDir+"w2v_collections/Wikipedia/vectors/EN_Wikipedia_w2v_input_format.txtUTF8.vec"



def start():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='input')
    parser.add_argument('-o', required=True, help='output')
    parser.add_argument('-l', required=True, help='language')
    parser.add_argument('-s', required=True, help='similarity')
    parser.add_argument('-a', required=False, help='aLv')
    parser.add_argument('-t', required=False, help='aSt')
    parser.add_argument('-u', required=False, help='aSt2')
    parser.add_argument('-e', required=False, help='emb')

    args = parser.parse_args()
    param2value = MyIOutils.parseOptions(args)
    nGramSize = 0     
    if not bool(param2value):
        print("Error: invalid input options. ")
        print(MyIOutils.showNewselaUsageMessage())
        exit()         
    inFile = param2value.get("input")
    outFile = param2value.get("output")
    similarityStrategy = param2value.get("similarity")
    embeddingsFile = param2value.get("emb")
    if len(similarityStrategy) == 3 and similarityStrategy[0]=='C' and similarityStrategy[-1]=='G':
        nGramSize = int(similarityStrategy[1])
        similarityStrategy = DefinedConstants.CNGstrategy
    

    model = None 
    if similarityStrategy == DefinedConstants.CWASAstrategy or similarityStrategy==DefinedConstants.WAVGstrategy:
        print("Reading embeddings...")
        vocab = MyIOutils.readNewselaEmbeddingVocabulary(inFile, language)
        aux = EmbeddingModel(embeddingsFile, vocab)
        model = ModelContainer(aux, None)
        if similarityStrategy == DefinedConstants.CWASAstrategy:
            print("compute w2v cosine distance")
            model.em.precomputeW2VcosDist()
            model.em.createSimilarityMatrix()
             
    elif similarityStrategy == DefinedConstants.CNGstrategy:
        print("Calculating IDF...")
        aux = NgramModel(True, nGramSize)
        model = ModelContainer(None, aux)
        aux.buildNewselaNgramModel(inFile, language, alignmentLevel)
    print("Aligning...")
    ini = time.time()
    alignNewselaDataset(inFile, language, outFile, alignmentLevel, similarityStrategy, alignmentStrategy, subLvAlignmentStrategy, model)
    end = time.time()
    diff = end - ini
    print("Total processing time: %d min %f sec" % (int(diff / 60), diff % 60))


def alignNewselaDataset( inFolder, language, outFolder, alignmentLevel, similarityStrategy, alignmentStrategy, subLvAlignmentStrategy, model):

    regFilter = r'^.*\.'+language+'.0.txt$'
    k =0 
    for dirpath, dirs, files in os.walk(inFolder):  
        for fileProto in files:
            if re.match(regFilter, fileProto):
                file2clean = {}
                for i in range(5):
                    file1 = fileProto.replace("." + language + ".0.txt","." + language + "." + str(i) + ".txt")
                    text1 = MyIOutils.readTextFile(inFolder + file1)
                    if text1:
                        file2clean[file1] = TextProcessingUtils.getCleanText(text1, alignmentLevel, similarityStrategy, model)
                
                cleanSubtexts1 = []
                cleanSubtexts2 = []
                for i in range(5):
                    file1 = fileProto.replace("." + language + ".0.txt", "." + language + "." + str(i) + ".txt")
                    cleanSubtexts1 = file2clean[file1]

                    if cleanSubtexts1:
                        for j  in range(i + 1, 5):
                            file2 = fileProto.replace("." + language + ".0.txt", "." + language + "." + str(j) + ".txt")
                            cleanSubtexts2 = file2clean[file2]
                            if cleanSubtexts2:
                                alignments = VectorUtils.alignUsingStrategy(cleanSubtexts1,	cleanSubtexts2, similarityStrategy, alignmentStrategy, model)
                                if  alignmentLevel == DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel:
                                    alignments = VectorUtils.getSubLevelAlignments(alignments, cleanSubtexts1, cleanSubtexts2, similarityStrategy, subLvAlignmentStrategy, model)
                                MyIOutils.saveAlignments(alignments, outFolder + file2 + "_ALIGNED_WITH_" + file1)
                                stats = MyIOutils.getStats(alignments, cleanSubtexts1,cleanSubtexts2,outFolder + file2 + "_ALIGNED_WITH_" + file1 + "_stats.txt")
                                print(stats)
						