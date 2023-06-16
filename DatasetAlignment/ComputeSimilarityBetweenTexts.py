import argparse
import time

from Utils import MyIOutils, DefinedConstants, TextProcessingUtils, VectorUtils
from Representations import ModelContainer, NgramModel, EmbeddingModel
import DatasetAlignment.AlignAnyDataset

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
outFile = MyIOutils.getOutputFileName(inFile, alignmentLevel, similarityStrategy, nGramSize)

# embeddingsFile = baseDir+"w2v_collections/Wikipedia/vectors/EN_Wikipedia_w2v_input_format.txtUTF8.vec"
embeddingsFile = "data/de-word2vec/cc.de.300.vec"



def start():

    parser = argparse.ArgumentParser()
    parser.add_argument('-ic', required=False, help='input_complex')
    parser.add_argument('-it', required=False, help='input_target')
    parser.add_argument('-i', required=False, help='input')
    parser.add_argument('-o', required=True, help='output')
    parser.add_argument('-l', required=True, help='language')
    parser.add_argument('-s', required=True, help='similarity')
    parser.add_argument('-a', required=False, help='aLv')
    parser.add_argument('-t', required=False, help='aSt')
    parser.add_argument('-u', required=False, help='aSt2')
    parser.add_argument('-e', required=False, help='emb')
    parser.add_argument('-ll', required=False, help='linelevel')

    args = parser.parse_args()
    param2value = MyIOutils.parseOptions(args)
    # setting, outFolder, globalSimilarityStrategy, similarityStrategy, language, embeddingsFile, lineLevel, alignmentStrategy, alignmentLevel, subLvAlignmentStrategy, model, nGramSize = DatasetAlignment.AlignAnyDataset.get_settings(
    #    param2value)
    nGramSize = 0
    firstSentIndex = 0
    secondSentIndex = 1         
    if not bool(param2value):
        print("Error: invalid input options. ")
        print(MyIOutils.showCustomModelUsageMessage())
        exit()         
    # inFileComplex = param2value.get("input_complex")
    # inFileSimple = param2value.get("input_target")
    inFile = param2value.get("input")
    outFile = param2value.get("output")
    similarityStrategy = param2value.get("similarity")
    embeddingsFile = param2value.get("emb")
    language = param2value.get("language")
        # linelevel - extra property for handling sentence segmentation per line (to be able to compare with other tools)
    lineLevel = param2value.get("linelevel") 
    if len(similarityStrategy) == 3 and similarityStrategy[0]=='C' and similarityStrategy[-1]=='G':
        nGramSize = int(similarityStrategy[1])
        similarityStrategy = DefinedConstants.CNGstrategy
    

    model = None 
    if similarityStrategy == DefinedConstants.CWASAstrategy or similarityStrategy==DefinedConstants.WAVGstrategy:
        print("Reading embeddings...")
        vocab = MyIOutils.readTwoTextPerLineFileEmbeddingVocabulary(inFile, firstSentIndex, secondSentIndex)
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
        aux.buildTwoTextPerLineFileModel(inFile, alignmentLevel, firstSentIndex, secondSentIndex, lineLevel)
    print("Aligning...")
    ini = time.time()
    calculateTwoTextPerLineFileSimilarities(inFile,outFile, similarityStrategy, alignmentStrategy, alignmentLevel, model, firstSentIndex, secondSentIndex, lineLevel)
    end = time.time()
    diff = end - ini
    print("Total processing time: %d min %f sec" % (int(diff / 60), diff % 60))


def calculateTwoTextPerLineFileSimilarities( inFile,  outFile,  similarityStrategy, 
			 alignmentStrategy,  alignmentLevel,  model,  firstSentIndex,  secondSentIndex, lineLevel):
    inF = open(inFile, "r")
    outF = open(outFile, "w")
    for line in inF.readlines():
        if not line.strip():
            continue
        if line:
            ar = line.strip().split("\t")
            cleanSubtexts1 = TextProcessingUtils.getCleanText(ar[firstSentIndex],alignmentLevel, similarityStrategy,model, lineLevel)
            cleanSubtexts2 = TextProcessingUtils.getCleanText(ar[secondSentIndex],alignmentLevel, similarityStrategy,model, lineLevel)
            alignments = VectorUtils.alignUsingStrategy(cleanSubtexts1, cleanSubtexts2,similarityStrategy, alignmentStrategy, model)
            if len(ar) == 3 or len(ar) == 4: # this is only for the WikiSimpleWiki dataset     
                outF.write(ar[0] +"\t"+ar[firstSentIndex]+"\t"+ar[secondSentIndex]+"\t"+str(alignments[0].getSimilarity())+"\n")
            elif len(ar) == 2:
                outF.write(ar[firstSentIndex]+"\t"+ar[secondSentIndex]+"\t"+str(alignments[0].getSimilarity())+"\n")
            else:
                print("Error: the format of the input file is the following (use tab separator):\ntext1\ttext2")
                exit(1)
    inF.close()
    outF.close()