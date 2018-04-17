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
    collectData = raw_input("Would you like to gather all tweets in one file? (y/n) ")
    if collectData == "y":
        collectFiles()
        findLinks()
    while True:
        userInput()

def showInfoOnBitlys():
    bitlys = []
    lineNr = 0
    for line in open('./data/links/BitlyInfo.txt', 'r'):
        print(str(lineNr)+": " + line)
        bitlys.append(line)
        lineNr += 1
    createTree = raw_input("Create tree from specific bitly? ")
    if createTree == "y":
        chosenBitly = input("Choose the line that has the interesting link: ")
        headline = bitlys[chosenBitly].split(",")[0]
        print("Headline is " + str(headline))
        path = Path(('.data/tree/trees/' + headline + ".txt"))
        if path.is_file():
            print("Tree exists")
        else:
            if isAlreadyExtracted(headline):
                propagationTree.create(COLLECTIONPATH+headline)
            else:
                bitly = bitlys[chosenBitly].split(", ")[1]
                collectionFile = extractTweeters(bitly)
                propagationTree.create(collectionFile)

def userInput():
    option = input("What would you like to do now? \n1: Get info on bitlys \n2: Construct multiple trees \n")
    if option == 1:
        showInfoOnBitlys()
    elif option == 2:
        startConstructing()
    else:
        return

def startConstructing():
    bitlys = open('./data/links/BitlyInfo.txt', 'r')
    minTreeAmount = input("Enter minimum amount of tweets to construct tree: ")
    maxTreeAmount = input("Enter maximum amount of tweets to construct tree: ")
    for line in bitlys:
        occurances = line.split(", ")[2]
        if minTreeAmount < int(occurances) < maxTreeAmount:
            # headline = line.split(", ")[0]
            bitly = line.split(", ")[1]
            collectionFile = extractTweeters(bitly)
            propagationTree.create(collectionFile)


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
    open('./data/links/BitlyInfo.txt', 'w').close()
    foundBitlys = open('./data/tree/knownLinks.txt', 'r+')
    bitlyInfoFile = open('./data/links/BitlyInfo.txt', 'r+')
    foundRetweetsAndQuotes = open('./data/tree/foundRetweetsAndQuotes.txt', 'w')
    tweets = []
    linkDictionary = {}
    occurancesDictionary = {}
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

        if url in occurancesDictionary:
            occurancesDictionary[url] += 1
        else:
            occurancesDictionary[url] = 1

    for key, val in linkDictionary.items():
        try:
            foundBitlys.write(str(key) + "," + str(val) + "\n")
        except UnicodeEncodeError:
            print("ERROR")
            encodedKey = key.encode("utf-8")
            foundBitlys.write(str(getHeadline(encodedKey)) + ", " + encodedKey + ", " + str(val) + "\n")
    nrOfIterations = 0
    for key, val in occurancesDictionary.items():
        nrOfIterations += 1
        encodedKey = key.encode("utf-8")
        headline = getHeadline(encodedKey)
        if headline is not None:
            toBitlyInfo = headline + ", " + encodedKey + ", " + str(val) + "\n"
            bitlyInfoFile.write(toBitlyInfo)
        if nrOfIterations > 5:
            return
    bitlyInfoFile.close()
    foundBitlys.close()

'''Creates a file containing all posts regarding a certain URL'''
def extractTweeters(expandedURL):
    headline = titleExtractor.saveText(expandedURL)
    if isAlreadyExtracted(headline):
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

def getHeadline(url):
    return titleExtractor.saveText(url)

def isAlreadyExtracted(headline):
    if os.path.exists(COLLECTIONPATH+headline):
        return True

main()
