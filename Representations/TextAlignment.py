#!/usr/bin/env python
""" generated source for module TextAlignment """
# package: simplifiedTextAlignment.Representations
class TextAlignment(object):
    """ generated source for class TextAlignment """
    source = str()
    target = str()
    similarity = float()
    id = str()
    index1 = int()
    index2 = int()

    def __init__(self, text1, text2, sim, i1, i2):
        """ generated source for method __init__ """
        self.source = text1
        self.target = text2
        self.similarity = sim
        self.index1 = i1
        self.index2 = i2
        self.id = self.toString()

    def hashCode(self):
        """ generated source for method hashCode """
        return self.id.hashCode()

    def toString(self):
	    return str(self.index1)+":\t"+str(self.source) + "\t---("+str(self.similarity)+")--->\t"+str(self.index2)+":\t"+str(self.target)

    def equals(self, obj):
        """ generated source for method equals """
        if not (isinstance(obj, (TextAlignment, ))):
            return False
        if obj == self:
            return True
        return self.id == obj

    def compareTo(self, o):
        """ generated source for method compareTo """
        return self.id.compareTo(o.id)

    def __str__(self):
        """ generated source for method toString """
        return self.index1 + ":\t" + self.source + "\t---(" + self.similarity + ")--->\t" + self.index2 + ":\t" + self.target

    def getSource(self):
        """ generated source for method getSource """
        return self.source

    def getTarget(self):
        """ generated source for method getTarget """
        return self.target

    def getSimilarity(self):
        """ generated source for method getSimilarity """
        return self.similarity

    def getIndexAlignmentString(self):
        """ generated source for method getIndexAlignmentString """
        return self.index1 + " --> " + self.index2 + " (" + self.similarity + ")"

    def getSourceIndex(self):
        """ generated source for method getSourceIndex """
        return self.index1

    def getTargetIndex(self):
        """ generated source for method getTargetIndex """
        return self.index2

    def setTarget(self, text, newIndex, newSim):
        """ generated source for method setTarget """
        self.target = text
        self.index2 = newIndex
        self.similarity = newSim
        self.id = self.toString()

    def setTargetIndex(self, newIndex):
        """ generated source for method setTargetIndex """
        self.index2 = newIndex

    def setSourceIndex(self, newIndex):
        """ generated source for method setSourceIndex """
        self.index1 = newIndex

    def recalcID(self):
        """ generated source for method recalcID """
        self.id = self.toString()

    def toCVS(self):
        return str(self.index1)+";"+str(self.index2)+";"+str(self.similarity)+";"+str(self.source) + ";"+str(self.target)
	

