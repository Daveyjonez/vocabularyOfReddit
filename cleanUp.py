import os
import string

'''
Fxn signature: removeStopWords(inList, stopWordsFile)
Description: This function cleans up a list of all stopWords contained in
    the stopWords file passed in
Params:
    inList - list - the list to filter out stopWords from
    stopWordsFile - string - the contents of the stop words file
Returns:
    list - The cleaned up list
'''
def removeStopWords(inList, stopWords):
    stopWordsList = stopWords.lower().split()
    return [word for word in inList if word not in stopWordsList]

'''
Fxn signature: cleanVocab(inoutString, removeFile)
Description: This function cleans up a string of punctuation, digits, obvious
    URLs and any other words contained within a stopwords file
Params:
    inoutString - string - The string to clean up
    removeFile - string - The name of the file containing all stopWords
        to remove from the string to clean up.
Returns:
    string - The cleaned up string
'''
def cleanComment(inString, stopWordsString):

    outString = inString.lower()

    # Filter out removed or deleted comments
    for word in outString:
        outString = outString.replace('[removed]', '')
        outString = outString.replace('[deleted]', '')

    # Remove punctuation
    for mark in string.punctuation:
        outString = outString.replace(mark, '')

    # Remove numbers
    for digit in string.digits:
        outString = outString.replace(digit, '')

    outWords = removeStopWords(outString.split(), stopWordsString)

    # Remove any obvious URLs
    for word in outWords:
        if 'http' in word or 'www' in word:
            outWords.remove(word)

    return outWords
