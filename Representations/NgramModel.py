#!/usr/bin/env python
""" generated source for module NgramModel """
# package: simplifiedTextAlignment.Representations
import math  
import re
import os
from Utils import MyIOutils, DefinedConstants, TextProcessingUtils, VectorUtils

class NgramModel(object):


    def __init__(self, isCNG, n):
        """ generated source for method __init__ """
        self.nSize = n
        self.isCNGmodel = isCNG
        self.n2i = {}
        self.i2IDF = []
        self.nDocs = 0

    
        


    def buildNewselaNgramModel(self, inFolder, language, alignmentLevel, lineLevel):
        """ generated source for method buildNewselaNgramModel """
        regFilter = r'^.*\.'+language+'.0.txt$'
        for dirpath, dirs, files in os.walk(inFolder):  
            for filename in files:
                if re.match(regFilter, filename):
                    text = MyIOutils.readTextFile(inFolder + filename)
                    self.processAndCountTextNgrams(text, alignmentLevel, lineLevel)
                    # CARE, THIS LOOP IS DEPENDENT OF THE NEWSELA DATASET FORMAT
                    i = 1 
                    while i<5:
                        # CARE, THIS LOOP IS DEPENDENT OF THE NEWSELA DATASET FORMAT
                        file_ = re.sub("." + language + ".0.txt","." + language + "." + str(i) + ".txt", filename)
                        text = MyIOutils.readTextFile(inFolder + file_)
                        if text != None:
                            self.processAndCountTextNgrams(text, alignmentLevel, lineLevel)
                        i += 1
        self.calculateIDF()


    def buildTwoTextPerLineFileModel(self, inFile, alignmentLevel, fistSentIndex, secondSentIndex):
        """ generated source for method buildTwoTextPerLineFileModel """
        with open(inFile, "r") as f:
            for l in f.readlines():
                if not l.strip():
                    continue
                if l:
                    ar = l.split("\t")
                    self.processAndCountTextNgrams(ar[fistSentIndex], alignmentLevel)
                    self.processAndCountTextNgrams(ar[secondSentIndex], alignmentLevel)
        self.calculateIDF()

    def processAndCountTextNgrams(self, text, alignmentLevel, lineLevel):
        """ generated source for method processAndCountTextNgrams """
        subtexts = []
        if not alignmentLevel == DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel:
            subtexts = TextProcessingUtils.getSubtexts(text, alignmentLevel, lineLevel)
        else:
            # if it is done at sentence and paragraph level, since this is to calculate the IDF, we can concatenate both levels. This is done because the sentence splitter may introduce some new ngrams, as a result of the tokenization
            subtexts = []
            subtexts1 = TextProcessingUtils.getSubtexts(text, DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel, lineLevel)
            for subtext1 in subtexts1:
                subtexts2 = TextProcessingUtils.getSubtexts(text, DefinedConstants.SentenceLevel, lineLevel)
                builder = ""
                for subtext2 in subtexts2:
                    builder += subtext2 + " "
                subtexts.append(subtext1 + " " + builder)
        self.countSubtextsIDFngrams(subtexts)


    def calculateIDF(self):
        """ generated source for method calculateIDF """
        i = 0
        for freq in self.i2IDF:
            self.i2IDF[i] = math.log(1 + (self.nDocs / freq))
            i += 1

    def countSubtextsIDFngrams(self, subtexts):
        """ generated source for method countSubtextsIDFngrams """
        for text in subtexts:
            self.countTextIDFngrams(text)

    def countTextIDFngrams(self, text):
        """ generated source for method countTextIDFngrams """
        if self.isCNGmodel:
            self.countTextNonRepCharNgrams(text)
        else:
            None
            #  TO IMPLEMENT AT WORD LEVEL

    def countTextNonRepCharNgrams(self, text):
        """ generated source for method countTextNonRepCharNgrams """
        cng = []
        strvar = ""
        index = 0
        seen = []
        i = 0
        while i < len(text) - self.nSize+1:
            cng = []
            for j in range(self.nSize):
                cng.append(text[j+i])
            strvar = "".join(cng).replace("\n", " ")
            if not strvar in seen:
                index  =  self.n2i.get(strvar)
                if index  != None:
                    self.i2IDF[index] = self.i2IDF[index] + 1
                else:
                    self.i2IDF.append(1.0)
                    self.n2i[strvar] =  len(self.n2i)
                    #print("Added ["+str(index)+"] ["+strvar+"] ["+str(self.n2i[strvar])+"] ["+str(len(self.n2i))+"]" )

                seen.append(strvar)
            i += 1
        self.nDocs += 1

    def getCharNgramTFIDFmap(self, text):
        """ generated source for method getCharNgramTFIDFmap """
        tfidf = {}
        cng = []
        strvar = ""
        index = 0
        i = 0
        while i < len(text) - self.nSize+1:
            j=0
            cng = []
            for j in range(self.nSize):
                cng.append(text[j+i])
            strvar = "".join(cng).replace("\n", " ")
            index = self.n2i[strvar]
            if index != None:
                tfidf[index] = tfidf.get(index, 0.0) + 1
            i += 1
        for id in tfidf.keys():
            tfidf[id]=  (1 + math.log(tfidf.get(id))) * self.i2IDF[id]
        VectorUtils.getCosDistPartialResultVector(tfidf)
        return tfidf

