import os
import json

import propagationTree
import titleExtractor

TWEETSPATH = 'C:/Users/linne/Documents/LiU/TDDD82/Kandidatprojekt/kandidat/data/tweets/'
COLLECTIONPATH = 'C:/Users/linne/Documents/LiU/TDDD82/Kandidatprojekt/kandidat/data/links/collectionByLink/'

'''Writes two files that contain all Twitter posts, one to be changed whenever tweets in them are 
written to another file'''
def collectFiles():
    tweetsCollection = open('collectedTweets.txt', 'w')
    collectionToChange = open('unExtractedTweets.txt', 'w')

    for file in os.listdir(TWEETSPATH):
        for line in open(TWEETSPATH + file):
            tweetsCollection.write(line)
            collectionToChange.write(line)

def main():
    collectData = True
    if collectData:
        collectFiles()
        findLinks()
    collectionFile = extractTweeters('http://bit.ly/2FFIoaz')
    print(collectionFile)
    propagationTree.create(collectionFile)


'''Writes all found links and their number of occurances into a file'''
def findLinks():
    open('knownLinks.txt', 'w').close()
    foundBitlys = open('knownLinks.txt', 'r+')
    foundRetweetsAndQuotes = open('foundRetweetsAndQuotes.txt', 'w')
    tweets = []
    linkDictionary = {}
    for line in open('collectedTweets.txt', 'r'):
        tweets.append(json.loads(line))
    for line in tweets:
        url = line['entities']['urls'][0]['expanded_url']
        if 'retweeted_status' or 'quoted_status' in line:
            if url + "\n" not in open('foundRetweetsAndQuotes.txt', 'r'):
                foundRetweetsAndQuotes.write(url + "\n")
        if url in linkDictionary:
            linkDictionary[url] += 1
        else:
            linkDictionary[url] = 1

    for key, val in linkDictionary.items():
        try:
            foundBitlys.write(str(key) + ", " + str(val) + "\n")
        except UnicodeEncodeError:
            print("ERROR")
            foundBitlys.write(key.encode("utf-8") + ", " + str(val) + "\n")


'''Creates a file containing all posts regarding a certain URL'''
def extractTweeters(expandedURL):
    headline = titleExtractor.saveText(expandedURL)
    savefile = open(COLLECTIONPATH+headline, 'w')
    unExtractedTweets = open('unExtractedTweets.txt', 'r')
    lines = unExtractedTweets.readlines()
    unExtractedTweets.close()
    unExtractedTweets = open('unExtractedTweets.txt', 'w')
    for line in lines:
        thisTweet = json.loads(line)
        if expandedURL == thisTweet['entities']['urls'][0]['expanded_url']:
            savefile.write(line)
        else:
            unExtractedTweets.write(line)
    return COLLECTIONPATH+headline


main()
