from Utils import DefinedConstants, VectorUtils

from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
import re
from Representations import Text2abstractRepresentation

def getCleanEmbeddingModelTokens( text):
    #tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+|'")
    #blob_object = TextBlob(text, tokenizer = tokenizer)
    #corpus_words = blob_object.tokens
    corpus_words = re.split(r' |_|=|;|\.|\,|\"|\'|\:|;|\*|%|\=|\!|\?|`|\-|&|\\\\|/',text)
    cleanTokens = []
    for token in corpus_words:
        if isValidTokenForEmbeddingModel(token.lower()):
            cleanTokens.append(token.lower())
    return cleanTokens


def getCleanText( text,  alignmentStrategy, similarityStrategy,  model):
    subtexts = getSubtexts(text,alignmentStrategy)
    cleanSubtexts_ = cleanSubtexts(subtexts, similarityStrategy, model)
    if similarityStrategy == DefinedConstants.WAVGstrategy:
        VectorUtils.calculateWAVGs(cleanSubtexts_,model.em)		
    if alignmentStrategy == DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel:
        getCleanSublevelText(cleanSubtexts_, DefinedConstants.SentenceLevel, similarityStrategy, model)
    return cleanSubtexts_
	
def getCleanSublevelText(cleanSubtexts,  alignmentStrategy,
			 similarityStrategy,  model):
	for cleanText in  cleanSubtexts:
		cleanText.setSubLevelRepresentations(getCleanText(cleanText.getText(), alignmentStrategy, similarityStrategy, model))

def getSubtexts( text,  alignemntStrategy):
    subtexts = []
    if alignemntStrategy == DefinedConstants.ParagraphSepEmptyLineLevel or alignemntStrategy == DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel:
        ar = re.split(r'\n\n', text)
        for subtext in ar:
            if len(subtext.strip())>0:
                subtexts.append(subtext)
    elif alignemntStrategy == DefinedConstants.SentenceLevel:
        blob_object = TextBlob(text)
        sentences = blob_object.sentences
        #sentences = re.split(r'\r?\n', text)
        for s in sentences:
            if len(s.strip())>0:
                subtexts.append(s)
    else:
        print("Error: alignment level not recognized.")
        exit(1)
    return subtexts


def cleanSubtexts(subtexts,  similarityStrategy,  model):
    cleanSubtexts = []
    for  subtext in  subtexts:
        if similarityStrategy == DefinedConstants.WAVGstrategy or similarityStrategy == DefinedConstants.CWASAstrategy:
            cleanSubtexts.append(cleanSubtextForEmbeddingModel(subtext, model.em))
        elif similarityStrategy == DefinedConstants.CNGstrategy:
            cleanSubtexts.append(cleanSubtextForCNGmodel(subtext, model.nm))
    return cleanSubtexts
	
def cleanSubtextForCNGmodel( subtext,  nm):
    cleanTokenIndices = nm.getCharNgramTFIDFmap(subtext)
    return Text2abstractRepresentation(subtext,	None, cleanTokenIndices)
	

def cleanSubtextForEmbeddingModel( subtext,  em):
    #StringTokenizer tokenizer = new StringTokenizer(subtext, " _&%=;.,-!?¡¿:;*/\\\"`''");
    #tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
    #blob_object = TextBlob(subtext, tokenizer = tokenizer)
    #corpus_words = blob_object.tokens
    corpus_words = re.split(r' |_|=|;|\.|\,|\"|\'|\:|;|\*|%|\=|\!|\?|`|\-|&|\\\\|/',str(subtext))
    cleanTokenIndices = []
    for token in corpus_words:
        index = em.getIndex(token.lower())
        if isValidTokenForEmbeddingModel(token.lower()) and index is not None:
            cleanTokenIndices.append(index)
    return Text2abstractRepresentation(subtext,	cleanTokenIndices, None)

def isValidTokenForEmbeddingModel( token):
    return len(token) > 1 and  hasNoNumbers(token)

def hasNoNumbers( token):
    for char in token:
        if not char.isalpha():
            return False

    return True