import math  
from Utils import DefinedConstants
from Representations import TextAlignment
import numpy


def calculateWAVGs(cleanSubtexts,  em):
    for subtext in cleanSubtexts:
        subtext.calculateWAVG(em)
        getCosDistPartialResultVector(subtext.getWAVG())


def getCosDistPartialResultVector(v):
    a = 0.0
    for key in v:
        a += pow(v[key], 2)
    if a > 0:
        a = math.sqrt(a)
        for key in v:
            v[key]= v[key] / a


def alignUsingStrategy(cleanSubtexts1, cleanSubtexts2,  similarityStrategy,  alignmentStrategy,  model):
    sims = [[]]
    if similarityStrategy == DefinedConstants.WAVGstrategy:
        sims = alignUsingWAVG(cleanSubtexts1,cleanSubtexts2)
    elif similarityStrategy == DefinedConstants.CWASAstrategy:
        sims = alignUsingCWASA(cleanSubtexts1,cleanSubtexts2, model.em)
    elif similarityStrategy == DefinedConstants.CNGstrategy:
        sims = alignUsingNgrams(cleanSubtexts1,cleanSubtexts2)
    else:
        print("Error: similarity strategy not recognized.")
        exit(1)
    alignments = []
    if alignmentStrategy == DefinedConstants.closestSimStrategy:
        alignments = getAlignmentsUsingClosestCosSim(cleanSubtexts1,cleanSubtexts2, sims)
    elif alignmentStrategy == DefinedConstants.closestSimKeepingSeqStrategy:
        alignments = getAlignmentsUsingClosestCosSimKeepingSeq(cleanSubtexts1,cleanSubtexts2, sims)
    else:
        print("Error: alignment strategy not recognized.")
        exit(1)
    return alignments


def alignUsingNgrams( subtexts1, subtexts2):
    sims = numpy.zeros((len(subtexts1), len(subtexts2)))
    i = 0
    for  subtext1 in  subtexts1:
        weighting1 = subtext1.getTokenWeighting()
        j = 0
        for subtext2 in subtexts2:
            sims[i][j] = getCosSimUsingPartialResults(weighting1,subtext2.getTokenWeighting())
            if(math.isnan(sims[i][j])):
                sims[i][j] = 0
            j+=1
        i+=1
    return sims.tolist()

def getCosSimUsingPartialResults( v1, v2):
    sim = 0.0
    for key in v1:
        if key in v2:
            v2w = v2[key]
            sim += v1[key]*v2w                
    return sim


def alignUsingCWASA(subtexts1, subtexts2, em):
    sims = numpy.zeros((len(subtexts1), len(subtexts2)))
    i = 0
    for subtext1 in subtexts1:
        indices1 = subtext1.getTokenIndices()
        j = 0
        for subtext2 in subtexts2:
            sims[i][j] = getCWASAsimilarity(indices1,subtext2.getTokenIndices(), em)
            if math.isnan(sims[i][j]):
                sims[i][j] = 0
            j+=1
        i+=1
    return sims.tolist()


def getCWASAsimilarity(words1, words2, em):
    if len(words1) == 0 or len(words2) == 0:
        return 0.0
    sourceSims = numpy.zeros(len(words2)).tolist()
    isNotDoubleDirAligned = numpy.zeros(len(words2)).tolist()
    for i in range(len(sourceSims)):
        sourceSims[i] = -1
    total = 0.0
    sim= 0.0
    for susp in words1:
        max = -1
        i = 0
        for source in words2:
            sim=em.getSimilatity(susp,source)
            if sim > max:
                max = sim	
                if sim > sourceSims[i]:
                    sourceSims[i] = sim
                    isNotDoubleDirAligned[i] = False
            elif sim > sourceSims[i]:
                sourceSims[i] = sim
                isNotDoubleDirAligned[i] = True
            i+=1
        total += max
    n = len(words1)
    for i in  range(len(sourceSims)):
        if isNotDoubleDirAligned[i]:
            total += sourceSims[i]
            n+=1
    if n > 0:
        return total / n
    return total

def alignUsingWAVG(subtexts1, subtexts2):
    sims = numpy.zeros((len(subtexts1), len(subtexts2)))
    i = 0
    for subtext1 in subtexts1:
        v1 = subtext1.getWAVG()
        j = 0
        for subtext2 in subtexts2:
            sims[i][j] = getCosSimUsingPartialResults(v1,subtext2.getWAVG())
            if math.isnan(sims[i][j]):
                sims[i][j] = 0
            j+=1
        i+=1
    return sims.tolist()


def getAlignmentsUsingClosestCosSim(cleanSubtexts1, cleanSubtexts2, sims):
		alignments = []		
		i = 0
		for subtext2 in cleanSubtexts2:
			closestIndex = getIndexOfClosestSample(sims,i)
			alignments.append(TextAlignment(subtext2.getText(), cleanSubtexts1[closestIndex].getText(),sims[closestIndex][i], i, closestIndex))
			i+=1
		return alignments


def getIndexOfClosestSample( sims,  i):
    closest = -1
    index = -1
    for j in range(len(sims)):
        if sims[j][i] > closest:
            closest = sims[j][i]
            index = j
    return index


def getAlignmentsUsingClosestCosSimKeepingSeq(cleanSubtexts1, cleanSubtexts2, sims):
    alignments = getAlignmentsUsingClosestCosSim(cleanSubtexts1,cleanSubtexts2, sims)
    validIndexes = getLongestIncreassingTargetSequenceIndexes(alignments)
    prevValid = 0
    for i in range(len( alignments)):
        alignment2fix = alignments[i]
        if not i in validIndexes:
            nextValid = cleanSubtexts1.size()-1
            for  j in range( len(alignments)):
                if j in validIndexes:
                    nextValid = alignments[j].getTargetIndex()
                    break
            bestSim = sims[prevValid][alignment2fix.getSourceIndex()]
            bestIndex = prevValid
            for j  in range(prevValid+1, nextValid):
                if sims[j][alignment2fix.getSourceIndex()] > bestSim:
                    bestSim = sims[j][alignment2fix.getSourceIndex()]
                    bestIndex = j
            alignment2fix.setTarget(cleanSubtexts1.get(bestIndex).getText(), bestIndex, bestSim)
        prevValid = alignment2fix.getTargetIndex()
    return alignments

def getLongestIncreassingTargetSequenceIndexes(alignments):
    lengthLongestIncreassing = []
    globalMax = -1 
    globalMaxIndex = -1
    for i in range(len(alignments)):
        max = 1
        for j in range(i): 
            if alignments[i].getTargetIndex() > alignments[j].getTargetIndex() and (max == 1 or max < lengthLongestIncreassing[j] + 1):
                    max = 1 + lengthLongestIncreassing[j]
        lengthLongestIncreassing[i] = max
        if globalMax < max:
            globalMax = lengthLongestIncreassing[i]
            globalMaxIndex = i
    
    pos = set()
    pos.add(globalMaxIndex)
    currentMax = globalMax-1 
    lastAdded = -1
    for i in reversed(range(globalMaxIndex-1)): 
        target = alignments[i].getTargetIndex()
        if lengthLongestIncreassing[i]==currentMax:
            pos.add(i)
            lastAdded = target
            currentMax-=1
        elif target == lastAdded:
            pos.add(i)
    return pos

def getSubLevelAlignments(alignments, subtexts1,subtexts2, similarityStrategy,  alignmentStrategy,  model):
    subLvAlignments = []
    total1 = 0 
    total2 = 0
    for alignment in alignments:
        rep1 = subtexts1.get(alignment.getTargetIndex()).getSubLevelRepresentation()
        rep2 = subtexts2.get(alignment.getSourceIndex()).getSubLevelRepresentation()
        subLvAlignmentsAux = alignUsingStrategy(rep1,rep2, similarityStrategy, alignmentStrategy, model)
        for  subLvAlignment in subLvAlignmentsAux:
            subLvAlignment.setSourceIndex(total2+subLvAlignment.getSourceIndex())
            subLvAlignment.setTargetIndex(total1+subLvAlignment.getTargetIndex())
        subLvAlignments.extend(subLvAlignmentsAux)
        total1+=len(rep1)
        total2+=len(rep2)
    return subLvAlignments
