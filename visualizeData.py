'''
Filename: visualizeData.py
Author: David Owens
'''

import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.stats import pearsonr

DATA_DIR = 'output'
plt.style.use('ggplot')

allLabels = []
allSubscriberCount = []
allVocabSize = []

def makePlots(dataCsv):
    labels = []
    subscriberCounts = []
    vocabSizes = []
    mostFrequent = []

    # Get data from csv
    with open(os.path.join(DATA_DIR, dataCsv), 'r') as csvFile:
        r = csv.reader(csvFile, delimiter=',')
        for row in r:
            labels.append(row[0])
            subscriberCounts.append(row[1])
            vocabSizes.append(row[2])

            allLabels.append(row[0])
            allSubscriberCount.append(row[1])
            allVocabSize.append(row[2])

    # Do im
    fig = plt.figure()
    plt.scatter(subscriberCounts, vocabSizes, s = 15)
    fig.suptitle(labels, fontsize = 12)
    plt.suptitle('Relationship between subscriber count and vocab size for '
                 + dataCsv[:-4] + '\n related subreddits')
    plt.xlabel('Subscriber Count')
    plt.ylabel('Vocabulary Size')
    plt.show()


###############################################################################

if __name__ == '__main__':

    # List the various subreddit lists
    topics = os.listdir(DATA_DIR)
    topics.pop(0)

    makePlots(topics[1])

    '''
    allSubscriberCount = list(map(int, allSubscriberCount))
    allVocabSize = list(map(int, allVocabSize))

    bestFit = np.polyfit(x = subscriberCount, y = vocabSize, deg=1)
    p = np.poly1d(bestFit)
    bestFitX = np.arange(min(subscriberCount), max(subscriberCount))
    bestFitY = p(bestFitX)
    '''
