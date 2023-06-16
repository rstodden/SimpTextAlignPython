#!/usr/bin/env python
""" generated source for module EmbeddingModel """
# package: simplifiedTextAlignment.Representations
import math  
import re
import os
import numpy
from Utils import MyIOutils, DefinedConstants, TextProcessingUtils, VectorUtils
class EmbeddingModel(object):
    """ generated source for class EmbeddingModel """


    def __init__(self, embeddingsFile, vocab):

        self.i2v = []
        self.w2i = {}
        with open(embeddingsFile, "r", encoding="utf-8") as f:
            next(f)
            for l in f.readlines():
                # print(l)
                if not l.strip():
                    continue
                if l:
                    ar = l.split(" ")
                    v = []
                    # print(ar[0].encode("utf-8"))
                    if ar[0] in vocab:
                        for i in range(1, len(ar)):
                            v.append(float(ar[i]))
                        self.i2v.append(v)
                        self.w2i[ar[0]] =len(self.w2i)
        self.vectorLen = len(self.i2v[0])

    def precomputeW2VcosDist(self):
        """ generated source for method precomputeW2VcosDist """
        for v in self.i2v:
            VectorUtils.getCosDistPartialResultVector(v)

    def getVectorLength(self):
        """ generated source for method getVectorLength """
        return self.vectorLen

    def get(self, index):
        """ generated source for method get """
        return self.i2v[index]

    def getIndex(self, token):
        """ generated source for method getIndex """
        if token in self.w2i:
            return self.w2i[token]
        return None

    def createSimilarityMatrix(self):
        """ generated source for method createSimilarityMatrix """
        self.similarityM = numpy.zeros((len(self.i2v), len(self.i2v)))

    def getSimilatity(self, susp, source):
        """ generated source for method getSimilatity """
        sim = self.similarityM[susp][source]
        if sim != 0:
            return sim
        if susp == source:
            return 1
        sim = VectorUtils.getCosSimUsingPartialResults(self.i2v[susp], self.i2v[source])
        self.similarityM[susp][source] = sim
        self.similarityM[source][susp]  = sim
        return sim

