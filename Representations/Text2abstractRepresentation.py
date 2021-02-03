import numpy

class Text2abstractRepresentation(object):
    """ generated source for class Text2abstractRepresentation """
    text = str()
    tokenIndices = []
    tokenWeighting = {}
    wavg = None
    sublevel = None

    def __init__(self, subtext, cleanTokenIndices, tokenWeighting):
        """ generated source for method __init__ """
        self.text = subtext
        self.tokenIndices = cleanTokenIndices
        self.tokenWeighting = tokenWeighting

    def __str__(self):
        """ generated source for method toString """
        return self.text

    def getText(self):
        """ generated source for method getText """
        return self.text

    def calculateWAVG(self, em):
        """ generated source for method calculateWAVG """
        self.wavg = numpy.zeros(em.getVectorLength())
        v = []
        n = 0
        for index in self.tokenIndices:
            v = em.get(index)
            if v is not None:
                for i in  range(em.getVectorLength()):
                    self.wavg[i] += v[i]
                n += 1
        for i in range(em.getVectorLength()):
            self.wavg[i] /= n

    def getWAVG(self):
        """ generated source for method getWAVG """
        return self.wavg

    def getTokenIndices(self):
        """ generated source for method getTokenIndices """
        return self.tokenIndices

    def getTokenWeighting(self):
        """ generated source for method getTokenWeighting """
        return self.tokenWeighting

    def setSubLevelRepresentations(self, cleanText):
        """ generated source for method setSubLevelRepresentations """
        self.sublevel = cleanText

    def getSubLevelRepresentation(self):
        """ generated source for method getSubLevelRepresentation """
        return self.sublevel

    def getNbrOfWords(self):
        x = 0
        if self.text:
            x = len(self.text) 
        return x

