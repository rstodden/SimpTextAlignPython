from pathlib import Path
import os
import re
from decimal import Decimal
import csv
import numpy

from Utils import TextProcessingUtils
from Utils import DefinedConstants

def readEmbeddingsFromTxtFile(inFile):
    w2v = {}
    with open(inFile, "r") as f:
        for l in f.readlines():
            if not l.strip():
                continue
            if l:
                ar = l.strip().split()
                v = []
                for i in range(ar.length):
                    v[i-1] = Decimal(ar[i])
                w2v[ar[0]] = v
    return w2v

def readEmbeddingsFromTxtFileUsingVocab(inFile, vocab):
    w2v = {}
    with open(inFile, "r") as f:
        for l in f.readlines():
            if not l.strip():
                continue
            if l:
                ar = l.strip().split()
                if ar[0] in vocab:
                    v = []
                    for i in range(ar.length):
                        v[i-1] = Decimal(ar[i])
                    w2v[ar[0]] = v
    return w2v

def readTextFile(inFile):
    out  = []
    with open(inFile, "r") as f:
        for i in f.readlines():
            if not i.strip():
                continue
            if i:
                out.append(i+'\n')
    return ''.join(out)

def saveAlignments(alingments, outFile, fileEncoding="utf-8"):
    if len(alingments)>0:
        with open(outFile, 'w',encoding=fileEncoding) as f:
            for match in alingments:
                f.write(match.toString()+"\n\n")



def readNewselaEmbeddingVocabulary(inFolder, language):
    vocab = set()
    regFilter = r'^.*\.'+language+'.0.txt$'
    for dirpath, dirs, files in os.walk(inFolder):
        for filename in files:
            if re.match(regFilter, filename):
                fname = os.path.join(dirpath,filename)
                text = readTextFile(fname)
                print("Read file "+fname)
                vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(text))
                for i in range(1, 5):
                    filename = re.sub("." + language + ".0.txt","." + language + "." + str(i) + ".txt", filename)
                    fname = os.path.join(dirpath,filename)
                    text = readTextFile(fname)
                    if text:
                        vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(text))
    return vocab


def displayAlignments(alignments,  detailed=True):
    print ("Alignments:")
    for alignment in alignments:
        if detailed:
            print(alignment.toString())
        else:
            print(alignment.getIndexAlignmentString())
    print("")



def readTwoTextPerLineFileEmbeddingVocabulary(inFile, fistSentIndex, secondSentIndex):
    vocab = set()
    with open(inFile, "r") as f:
        for l in f.readlines():
            if not l.strip():
                continue
            if l:
                ar = l.strip().split("\t")
                vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(ar[fistSentIndex]))
                vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(ar[secondSentIndex]))
    return vocab

def convertArgToOption(param2value, args, key):
    if args:
        param2value[key] = args

def parseOptions(args):
    param2value = {}
    convertArgToOption(param2value, args.i, "inputdir")
    convertArgToOption(param2value, args.i, "input")
    convertArgToOption(param2value, args.ic, "input_complex")
    convertArgToOption(param2value, args.it, "input_target")
    convertArgToOption(param2value, args.o, "output")
    convertArgToOption(param2value, args.l, "language")
    convertArgToOption(param2value, args.s, "similarity")
    convertArgToOption(param2value, args.a, "aLv")
    convertArgToOption(param2value, args.t, "aSt")
    convertArgToOption(param2value, args.u, "aSt2")
    convertArgToOption(param2value, args.e, "emb")
    convertArgToOption(param2value, args.ll, "linelevel")
    return param2value

def showNewselaUsageMessage():
    print("Usage:\nprogram -i inFolder -o outFolder  -l language -s similarityStrategy -a alignmentLevel -t alignmentStrategy"
            + " {-u SubLevelalignmentStrategy} {-e embeddingsTxtFile}\n"
            + "\"inFolder\" is the folder with the original newsela texts.\n"
            + "\"outFolder\" is the folder where the alignments will be stored.\n"
            + "\"language\" can be \""+DefinedConstants.SpanishLanguage+"\" or \""+DefinedConstants.EnglishLanguage+"\". Default: \""+DefinedConstants.EnglishLanguage+"\".\n"
            + "\"similarityStrategy\" can be \""+DefinedConstants.CNGstrategy+"\", \""+DefinedConstants.WAVGstrategy+"\", or \""+DefinedConstants.CWASAstrategy+"\", where the N in \""+DefinedConstants.CNGstrategy+"\" should be replaced for the desired n-gram size, e.g. \""+DefinedConstants.CNGstrategy.replace("N", 3+"")+"\". Default: \""+DefinedConstants.CNGstrategy.replace("N", 3+"")+"\".\n"
            + "\"alignmentLevel\" can be \""+DefinedConstants.ParagraphSepEmptyLineLevel+"\", \""+DefinedConstants.SentenceLevel+"\", or \""+DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel+"\". Default: \""+DefinedConstants.SentenceLevel+"\".\n"
            + "\"alignmentStrategy\" can be \""+DefinedConstants.closestSimStrategy+"\" or \""+DefinedConstants.closestSimKeepingSeqStrategy+"\". Default: \""+DefinedConstants.closestSimStrategy+"\".\n"
            + "\"SubLevelalignmentStrategy\" can be \""+DefinedConstants.closestSimStrategy+"\" or \""+DefinedConstants.closestSimKeepingSeqStrategy+"\". Default: \""+DefinedConstants.closestSimStrategy+"\".\n"
            + "\"embeddingsTxtFile\" is the file with the embeddings using the classical word2vec txt format.\n"
            )


def showCustomModelUsageMessage():
    print("Usage:\nprogram -i inFile -o outFile -s similarityStrategy {-e embeddingsTxtFile}\n"
             "\"inFile\" is a file with two tab-separated texts per line. The program will output a similarity score for each one of these text pairs.\n"	
             "\"outFile\" contains the original \"inFile\" tab-separated texts plus their similarity score.\n"	
             "\"similarityStrategy\" can be \""+DefinedConstants.CNGstrategy+"\", \""+DefinedConstants.WAVGstrategy+"\", or \""+DefinedConstants.CWASAstrategy+"\", where the N in \""+DefinedConstants.CNGstrategy+"\" should be replaced for the desired n-gram size, e.g. \""+DefinedConstants.CNGstrategy.replace("N", str(3)+"")+"\". Default: \""+DefinedConstants.CNGstrategy.replace("N", str(3)+"")+"\".\n"	
             "\"embeddingsTxtFile\" is the file with the embeddings using the classical word2vec txt format.\n"
            )

def getOutputFileName(inFile, alignmentLevel, similarityStrategy, nGramSize):
    simStr = similarityStrategy
    if similarityStrategy == DefinedConstants.CNGstrategy:
        simStr.replace("N", str(nGramSize)+"")
    return inFile+"_"+ alignmentLevel+"_"+ simStr

def saveAlignmentsToCVS(alingments, outFile, fileEncoding="utf-8"):

    with open(outFile, 'w',encoding=fileEncoding) as f:
        for alingment in alingments:
            f.write(alingment.toCVS()+"\n\n")



def getStats(alingments, nbrOfLineOrginal, nbrOfLineSimple, outFile):
    data = numpy.zeros(len(alingments)).tolist()
    for i in range(len(alingments)):
        data[i] = alingments[i].getSimilarity()

    histogram = calcHistogram(data, 0.0, 1.0, 10)
    out = ""

    out = outFile+";"+str(len(nbrOfLineOrginal))+"/"+str(getTotalWord(nbrOfLineOrginal))+";"
    out += str(len(nbrOfLineSimple))+"/"+str(getTotalWord(nbrOfLineSimple))+";"

    total =0.0
    aboveTrashord=0.0
    for i in range(len(histogram)):
        total+=histogram[i]
        if i>=4:
            aboveTrashord+=histogram[i]

    out += str(aboveTrashord)+";"
    out += str(((aboveTrashord)/(total))) + "%;"
    for i in range(len(histogram)):
        out += str(histogram[i])+" ["+"{:.2f}".format((histogram[i]/total)*100.0)+"%]"+";"
    return out

def getTotalWord(nbrOfLineOrginal):
    x = 0
    for sentence in nbrOfLineOrginal:
        x+= sentence.getNbrOfWords()
    return x

def calcHistogram(data, min,  max, numBins):
    result =  numpy.zeros(numBins).tolist()
    binSize = (max - min)/numBins

    for d in data:
        bin = ((d - min) / binSize)
        if bin < 0:
            bin=0
        elif bin >= numBins:
            bin = numBins -1
        result[int(bin)] += 1
    return result
