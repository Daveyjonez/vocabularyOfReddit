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


###############################################################################

if __name__ == '__main__':

    # List the various subreddit lists
    topics = os.listdir(DATA_DIR)
    topics.pop(0)

    labels = []
    allLabels = []

    subscriberCount = []
    allSubscriberCount = []

    vocabSize = []
    allVocabSize = []

    mostFrequent = []

    for topic in topics:
        with open(os.path.join(DATA_DIR, topic), 'r') as csvFile:
            r = csv.reader(csvFile, delimiter=',')
            for row in r:
                allLabels.append(row[0])
                allSubscriberCount.append(row[1])
                allVocabSize.append(row[2])

    # Save vocabulary data
    with open(os.path.join(DATA_DIR, topics[1]), 'r') as csvFile:
        r = csv.reader(csvFile, delimiter=',')
        for row in r:
            labels.append(row[0])
            subscriberCount.append(row[1])
            vocabSize.append(row[2])
            mostFrequent.append(eval(row[3]))

    subscriberCount = list(map(int, allSubscriberCount))
    vocabSize = list(map(int, allVocabSize))

    print(pearsonr(subscriberCount, vocabSize))

    bestFit = np.polyfit(x = subscriberCount, y = vocabSize, deg=1)
    p = np.poly1d(bestFit)
    bestFitX = np.arange(min(subscriberCount), max(subscriberCount))
    bestFitY = p(bestFitX)

    print(p)

    fig = plt.figure()
    plt.scatter(subscriberCount, vocabSize, s = 15)
    plt.plot(bestFitX, bestFitY, color = 'k')
    fig.suptitle('Relationship between subreddit size and vocabulary size',
                 fontsize = 15)
    plt.xlabel('Subscriber Count')
    plt.ylabel('Vocabulary Size')
    plt.show()
