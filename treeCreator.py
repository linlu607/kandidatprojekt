import os
import json

import propagationTree
import titleExtractor
from pathlib import Path

TWEETSPATH = './data/tweets/'
COLLECTIONPATH = './data/links/collectionByLink/'

'''What should the code do?'''
def settingsInput():
    collectData = "n"  # raw_input("Would you like to collect data from dataset? (y/n) ")
    constructTree = "n"  # raw_input("Would you like to construct propagation trees from knownLinks? (y/n) ")
    printTree = "y"  # raw_input("Would you like to print a propagation tree from file? (y/n) ")
    minTreeAmount = 30  # input("Enter minimum tweets to construct tree ", )
    maxTreeAmount = 50  # input("Enter maximum tweets to construct tree ", )

    return [collectData, constructTree, printTree, minTreeAmount, maxTreeAmount]

def main():
    settings = settingsInput()
    if settings[0] == 'y':
        collectFiles()
        findLinks()

    if settings[1] == "y":
        for line in open('./data/tree/knownLinks.txt', 'r'):
            bitly = line.split(',')[0]
            nr = line.split(',')[1]
            if settings[3] < int(nr) < settings[4]:
                # for testing one file: bitly == "http://bit.ly/2F8OHSP":
                # for testing files with X links: int(nr) > settings[2] and int(nr) < settings[3]:
                collectionFile = extractTweeters(bitly)
                path = Path(('./data/tree/trees/' + collectionFile[30:-4] + '.txt'))
                if not path.is_file():
                    propagationTree.create(collectionFile)
    elif settings[2] == "y":
        propagationTree.printTree("Xbox_One_S_To")

'''Writes two files that contain all Twitter posts, one to be changed whenever tweets in them are 
written to another file'''
def collectFiles():
    tweetsCollection = open('./data/tree/collectedTweets.txt', 'w')
    collectionToChange = open('./data/tree/unExtractedTweets.txt', 'w')

    for file in os.listdir(TWEETSPATH):
        for line in open(TWEETSPATH + file):
            tweetsCollection.write(line)
            collectionToChange.write(line)

'''Writes all found links and their number of occurances into a file'''
def findLinks():
    open('./data/tree/knownLinks.txt', 'w').close()
    foundBitlys = open('./data/tree/knownLinks.txt', 'r+')
    foundRetweetsAndQuotes = open('./data/tree/foundRetweetsAndQuotes.txt', 'w')
    tweets = []
    linkDictionary = {}
    for line in open('./data/tree/collectedTweets.txt', 'r'):
        tweets.append(json.loads(line))
    for line in tweets:
        url = line['entities']['urls'][0]['expanded_url']
        if 'retweeted_status' or 'quoted_status' in line:
            if url + "\n" not in open('./data/tree/foundRetweetsAndQuotes.txt', 'r'):
                foundRetweetsAndQuotes.write(url + "\n")
        if url in linkDictionary:
            linkDictionary[url] += 1
        else:
            linkDictionary[url] = 1

    for key, val in linkDictionary.items():
        try:
            foundBitlys.write(str(key) + "," + str(val) + "\n")
        except UnicodeEncodeError:
            print("ERROR")
            foundBitlys.write(key.encode("utf-8") + ", " + str(val) + "\n")


'''Creates a file containing all posts regarding a certain URL'''
def extractTweeters(expandedURL):
    headline = titleExtractor.saveText(expandedURL)
    if os.path.exists(COLLECTIONPATH+headline):
        return COLLECTIONPATH+headline
    savefile = open(COLLECTIONPATH+headline, 'w')
    unExtractedTweets = open('./data/tree/unExtractedTweets.txt', 'r')
    lines = unExtractedTweets.readlines()
    unExtractedTweets.close()
    unExtractedTweets = open('./data/tree/unExtractedTweets.txt', 'w')
    for line in lines:
        thisTweet = json.loads(line)
        if expandedURL == thisTweet['entities']['urls'][0]['expanded_url']:
            savefile.write(line)
        else:
            unExtractedTweets.write(line)
    return COLLECTIONPATH+headline


main()
