'''
Filename: vocabularyOfReddit.py
Author: David Owens
'''

import csv
import os
import praw
import string
import time
from cleanUp import cleanComment
from cleanUp import removeStopWords
from collections import Counter

# Number of comments to collect words from
WORD_LIMIT = 25000
# Max number of comments to process from each submission
COMMENT_LIMIT = 75
# File containing all names and emojis to remove from comments
COMMENT_STOPWORDS = 'commentStopWords'
# File to remove non interesting words for most common
FREQUENCY_STOPWORDS = 'frequencyStopWords'
# Directory containing all the subreddits to visit
TOPICS_DIR = 'subredditLists'
# Directory to write data .csv's to
OUTPUT_DIR = 'output'

################################################################################

'''
Fxn signature: listdir_nohidden(path)
Description: Lists all files in the path directory which are not hidden
Params:
    path - string - The directory to list files from
Returns: list, all files in the path directory which are not hiddent
'''
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

'''
Fxn signature: listdir_nohidden(path)
Description: Lists all files in the path directory which are not hidden
Params:
    path - string - The directory to list files from
Returns: list, all files in the path directory which are not hiddent
'''
def processSubreddit(sub, wordLimit, commentLimit):

    print('\nCURRENT SUBREDDIT: {}'.format(sub))
    print(50*'-')
    print('processing...')

    with open(COMMENT_STOPWORDS + '.txt', 'r') as cmtStpWrdsFile:
        cmtStpWrds = cmtStpWrdsFile.read()

    # Tracker for number of words processed
    wordCount = 0;
    allWords = []

    # Get submissions and other data from subreddit
    try:
        # Get instance of the current subreddit in topic list
        submissions = sub.search(query = None, sort = 'comments')
        subscriberCount = sub.subscribers

    except:
        print('Subreddit failure: {}'.format(sub))
        return

    # Loop thru the submissions and gather the top comments
    for submission in submissions:
        # Loop thru all comments
        commentCount = 0;
        # Ignore stickies
        if not submission.stickied:
            submission.comments.replace_more(limit = 0)
            comments = submission.comments.list()
            for comment in comments:
                if commentCount < commentLimit:
                    if wordCount < wordLimit:
                        # If username ends in bot just ignore comment
                        try:
                            if not comment.author.name.lower().endswith('bot'):
                                cmt = cleanComment(comment.body, cmtStpWrds)
                                if len(cmt) + wordCount > WORD_LIMIT:
                                    cmt = cmt[:(WORD_LIMIT - wordCount) - 1]

                                # Increment number of words processed
                                wordCount += len(cmt)
                                allWords += cmt
                                commentCount += 1

                        except:
                            continue

        if wordCount >= WORD_LIMIT:
            break

    # Process list of all words
    vocab = set(allWords)
    with open(FREQUENCY_STOPWORDS + '.txt', 'r') as freqStpWrdsFile:
        freqStpWrds = freqStpWrdsFile.read()

    filteredAllWords = removeStopWords(allWords, freqStpWrds)
    filteredCount = Counter(filteredAllWords)

    # Build and return row for csv saving
    return [sub, subscriberCount, len(vocab), filteredCount.most_common(5)]


'''
Fxn signature: processTopic(redditInst, subList, wordLimit, outputDir)
Description:
Params:
    redditInst - reddit - An instance of reddit for PRAW to function
    subList - string - Directory name containing the lists of subreddits
    wordLimit - number - Number of words to process for each subreddit
    outputDir - string - Directory name of where to save the data
Returns: None, writes a .csv file containing data about a group of subreddits in
    a certain topic
'''
def processTopic(redditInst, topicDir, topic, wordLimit, commentLimit, outputDir):

    print(50*'=')
    print("CURRENT TOPIC: {}".format(topic[:-4]))
    print(50*'=')

    topicData = []
    # Open each list of subreddit topics
    with open(os.path.join(topicDir, topic), 'r') as currFile:

        # Get subreddits in file as a list
        subreddits = eval(currFile.readline())

        # Loop thru each subreddit in a certain topic group
        for sub in subreddits:
            currSubreddit = reddit.subreddit(sub)
            currSubData = processSubreddit(currSubreddit, wordLimit, commentLimit)
            topicData.append(currSubData)

    # Save vocabulary data
    with open(os.path.join(outputDir, topic[:-4] + '.csv'), 'w') as csvFile:
        w = csv.writer(csvFile)
        for sub in topicData:
            try:
                w.writerow(sub)
            except:
                pass

    # Sleep for 5 min to give Reddit API calls a break
    print('SLEEPING FOR 3 MIN\n')
    time.sleep(180)

###############################################################################

if __name__ == '__main__':
    # Initialize reddit instance
    reddit = praw.Reddit(client_id = 'DXVi5zl--THwVw',
                         client_secret = 'Li7wiLM-JkhfTKnLgTdhNwrYuZM',
                         username = 'vocabularyOfReddit',
                         password = 'tiddeRfOyralubacov',
                         user_agent = 'vocabularyOfReddit1')

    # List the various subreddit lists
    topics = listdir_nohidden(TOPICS_DIR)

    for topic in topics:
        # Collect all unique words
        processTopic(reddit,
                     TOPICS_DIR,
                     topic,
                     WORD_LIMIT,
                     COMMENT_LIMIT,
                     OUTPUT_DIR)
