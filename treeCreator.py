import os
import json

import time
import fileSorter
import propagationTree
import titleExtractor
from pathlib import Path

TWEETSPATH_REG = './data/tweets/'
COLLECTIONPATH = './data/links/collectionByLink/'
TREEPATH = './data/tree/'
SORTEDPATH = './data/tweets/sortedFiles/'

'''What should the code do?'''
def settingsInput():
    collectData = "n"  # raw_input("Would you like to collect data from dataset? (y/n) ")
    constructTree = "n"  # raw_input("Would you like to construct propagation trees from knownLinks? (y/n) ")
    printTree = "y"  # raw_input("Would you like to print a propagation tree from file? (y/n) ")
    minTreeAmount = 30  # input("Enter minimum tweets to construct tree ", )
    maxTreeAmount = 50  # input("Enter maximum tweets to construct tree ", )

    return [collectData, constructTree, printTree, minTreeAmount, maxTreeAmount]

def changeTime():
    PATH = './data/tree/trees/TDS/'
    for treeFile in os.listdir(PATH):
        if os.path.isfile(PATH+treeFile):
            tree = propagationTree.printTree(PATH + treeFile)
            time_ = tree.getTimePeriodRedo()
            propagationTree.changeInFile(treeFile, 'time', time_)

def changeLevels():
    PATH = './data/tree/trees/top/'
    for treeFile in os.listdir(PATH):
        if os.path.isfile(PATH + treeFile):
            tree = propagationTree.printTree(PATH + treeFile)
            timeLevels = tree.getTimeForLevels()
            propagationTree.changeInFile(treeFile, 'levelTimes', timeLevels)

def findTotalNrOfTweets():
    totalTweets = 0
    totalLinks = 0
    tweetsperfile = []
    linksperfile = []
    for file in ['generalTreeData.txt', 'generalTreeDataRandom.txt', 'generalTreeDataTop.txt']:
        print(file)
        for line in open(TREEPATH + file, 'r'):
            jsonLine = json.loads(line)
            totalTweets += jsonLine['size']
            totalLinks += 1
        tweetsperfile.append(totalTweets-sum(tweetsperfile))
        linksperfile.append(totalLinks-sum(linksperfile))
    print("Totalt antal tweets: " + str(totalTweets))
    print("Totalt antal lankar: " + str(totalLinks))
    print("Per fil:")
    print(tweetsperfile)
    print(linksperfile)

def findMissingPosts(outerFolder):
    OUTERPATH = './data/topAndRand/sortedTweets/'
    FOLDERPATH = OUTERPATH + outerFolder + '/'
    total = 0
    found = 0
    for folder in os.listdir(FOLDERPATH):
        INNERPATH = FOLDERPATH + folder + '/'
        for innerFolder in os.listdir(INNERPATH):
            for tweetsFile in os.listdir(INNERPATH + innerFolder + '/'):
                tweetsFileAndPath = INNERPATH + innerFolder + '/' + tweetsFile
                #print(os.path.isfile(tweetsFile))
                if os.path.isfile(tweetsFileAndPath):
                    with open(tweetsFileAndPath, 'r') as thisFile:
                        foundInFile = 0
                        rootIDs = []
                        counts = []
                        for line in thisFile:
                            jsonLine = json.loads(line)
                            if 'retweeted_status' in jsonLine:
                                foundInFile += 1
                                rootID = jsonLine['retweeted_status']['user']['id_str']
                                quoteCount = jsonLine['retweeted_status']['quote_count']
                                retweetCount = jsonLine['retweeted_status']['retweet_count']
                                if rootID not in rootIDs:
                                    rootIDs.append(rootID)
                                    counts.append(int(quoteCount) + int(retweetCount))
                                else:
                                    index = rootIDs.index(rootID)
                                    counts[index] = (int(quoteCount) + int(retweetCount))
                            elif 'quoted_status' in jsonLine:
                                foundInFile += 1
                                rootID = jsonLine['quoted_status']['user']['id_str']
                                quoteCount = jsonLine['quoted_status']['quote_count']
                                retweetCount = jsonLine['quoted_status']['retweet_count']
                                if rootID not in rootIDs:
                                    rootIDs.append(rootID)
                                    counts.append(int(quoteCount) + int(retweetCount))
                                else:
                                    index = rootIDs.index(rootID)
                                    counts[index] = (int(quoteCount) + int(retweetCount))
                        total += sum(counts)
                        found += foundInFile
                        print("Found in file: " + str(foundInFile) + " Total: " + str(sum(counts)))
    print("Found: " + str(found) + " Total: " + str(total))

def makeOtherTrees():
    skip = []
    filesDone = open('./data/topAndRand/filesDone.txt', 'a+')
    for line in filesDone:
        skip.append(line)

    PATH = './data/topAndRand/sortedTweets/other/'
    for folder in os.listdir(PATH):
        for innerFolder in os.listdir(PATH + folder + '/'):
            for tweetsFile in os.listdir(PATH + folder + '/' + innerFolder + '/'):
                fileAndFolder = PATH + folder + '/' + innerFolder + '/' + tweetsFile
                if os.path.isfile(fileAndFolder) and tweetsFile not in skip:
                    try:
                        print(tweetsFile)
                        propTree = propagationTree.create(fileAndFolder, 'generalTreeDataOther.txt')
                        print(propTree.getLink())
                        propTree.makeNodeTree()
                        filesDone.write(tweetsFile + '\n')
                        filesDone.flush()
                    except AttributeError:
                        print("Attribute error for " + str(tweetsFile) + "")


def main():
    makeOtherTrees()
    return
    PATH = './data/topAndRand/other/'
    for tweetsFile in os.listdir(PATH):
        if os.path.isfile(PATH + tweetsFile):
            try:
                print(tweetsFile)
                propTree = propagationTree.create(PATH+tweetsFile)
                print(propTree.getLink())
                propTree.makeNodeTree()
            except AttributeError:
                print("Attribute error for " + str(tweetsFile) + "")
    return

def linkURLs():
    BITLYPATH = './data/topAndRand/bitlys/'
    shortAndLongs = open('./data/shortAndLongs.txt', 'w+')
    URLs = []
    for line in open('./data/topAndRand/topSetURLs.txt', 'r'):
        URLs.append(line.replace("\n", ""))
    for line in open('./data/topAndRand/randomSetURLs.txt', 'r'):
        URLs.append(line.replace("\n", ""))
    for file in os.listdir(BITLYPATH):
        #print(file)
        if file.endswith("_news01h.txt") or file.endswith("_news24h.txt"):
          #  print("In file")
            for line in open(BITLYPATH+file, 'r'):
                longURL = line.split(", ")[1].split(": ")[1].replace("\'", "")
                if longURL in URLs:
           #         print("Url in urls")
                    shortAndLongs.write(line.split(", ")[4].split(": u")[1].replace("\'", "") + ", " + longURL + "\n")
    shortAndLongs.close()

def classifyLinks():
    files = ['generalTreeDataTop.txt', 'generalTreeDataRandom.txt']
    classes = {1: 'bbc', 2: 'bre', 3: 'fox', 4: 'huf', 5: 'gua', 6: 'other'}
    URLLinks = open('./data/shortAndLongs.txt', 'r')
    classified = []
    for line in open('./data/classifiedLinks.txt', 'r'):
        classified.append(line.replace("\n", ""))
    classifiedLinks = open('./data/classifiedLinks.txt', 'a')
    urlDict = {}
    for line in URLLinks:
        urls = line.split(", ")
        urlDict[urls[0]] = urls[1]
    with open('./data/tree/classifiedTweets.txt', 'a') as classFile:
        for generalFile in files:
            for line in open(TREEPATH + generalFile, 'r'):
                jsonLine = json.loads(line)
                link = jsonLine['link']
                if link not in classified:
                    print(link + ": " + urlDict[link])
                    classOption = input("Set class to: 1: bbc  2: bre  3: fox  4: huf  5: gua  6: other  7: return")
                    if classOption == 6:
                        linkClass = raw_input("Write class name: ")
                    elif classOption == 7:
                        classFile.close()
                        return
                    else:
                        linkClass = classes[classOption]
                    jsonLine['class'] = linkClass
                    classFile.write(json.dumps(jsonLine) + "\n")
                    classifiedLinks.write(link + "\n")

def makeTopTrees():
    startTime = time.time()
    treesToCreate = open('./data/topAndRand/smallerFiles.txt', 'r')
    for line in treesToCreate:
        if "top" in line.split("/")[4]:
            try:
                fileName = line.split(" ")[0]
                tree = propagationTree.create(fileName)
                print(tree.getLink())
                tree.makeNodeTree()
            except AttributeError:
                if fileName is not None:
                    print("Attribute error for " + str(fileName) + "")
                else:
                    print("Some error")
            print("Time: " + str(time.time() - startTime))

def gatherLargeFiles():
    saveFolder = SORTEDPATH+"Sorted_of_interest/"
    foldersChecked = 0
    filesChecked = 0
    for folder in os.listdir(SORTEDPATH):
        foldersChecked += 1
        if folder != "Sorted_of_interest":
            for innerFolder in os.listdir(SORTEDPATH+folder+"/"):
                for textFile in os.listdir(SORTEDPATH+folder+"/"+innerFolder+"/"):
                    filesChecked += 1
                    filePathAndName = SORTEDPATH+folder+"/"+innerFolder+"/"+textFile
                    fileSize = int(os.path.getsize(filePathAndName))
                    fileFound = True
                    if fileSize in range(0, 9999):
                        fileFound = False
                    if fileSize in range(10000, 20000):
                        saveLocation = open(saveFolder + "ten_twenty/" + textFile, 'a+')
                    elif fileSize in range(50000, 70000):
                        saveLocation = open(saveFolder + "fifty_sixty/" + textFile, 'a+')
                    elif fileSize in range(100000, 300000):
                        saveLocation = open(saveFolder + "hundred_hundredtwenty/" + textFile, 'a+')
                    elif fileSize in range(500000, 100000000):
                        saveLocation = open(saveFolder + "huge/" + textFile, 'a+')
                    else:
                        fileFound = False
                    if fileFound:
                        origFile = open(filePathAndName, 'r')
                        for line in origFile:
                            saveLocation.write(line)
                        saveLocation.close()
        print("Done with folder")
        print(foldersChecked)
    print(filesChecked)

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

def decreaseJSON(TWEETSPATH):
    nrOfErrors = 0
    fileCounter = 0
    startTime = time.time()
    for file in os.listdir(TWEETSPATH):
        with open(TWEETSPATH+file) as tweetsFile:
            for line in tweetsFile:
                jsonLine = json.loads(line)
                reducedTweet = fileSorter.makeMiniTweet(jsonLine)
                if reducedTweet is None:
                    break
                innerFolderName = json.dumps(reducedTweet['fileName'])[1:8]+"/"
                folderName = innerFolderName[:6]+"/"
                folderName = SORTEDPATH + folderName
                innerFolderName = folderName + innerFolderName
                try:
                    if not os.path.exists(innerFolderName):
                        nameLength = len(json.dumps(reducedTweet['fileName']))
                        if nameLength < 6:
                            folderName = folderName[:nameLength - 3]
                            innerFolderName = innerFolderName[:nameLength - 2]
                        if not os.path.exists(folderName):
                                os.makedirs(folderName)
                        os.makedirs(innerFolderName)
                    fileName = innerFolderName+json.dumps(reducedTweet['fileName'])+'.txt'
                    fileName = fileName.replace("\"", "")
                    try:
                        open(fileName, 'a+').write(json.dumps(reducedTweet) + "\n")
                    except IOError:
                        nrOfErrors += 1
                        break
                except WindowsError:
                    nrOfErrors += 1
        fileCounter += 1
        print(fileCounter)
        print(time.time()-startTime)
    print("Done")
    print("Nr of errors: " + str(nrOfErrors) + "")

def listTrees():
    with open(TREEPATH+"generalTreeData.txt", 'r') as treeInfo:
        for line in treeInfo:
            print line

def setClasses():
    minNodes = input("Insert minimum amount of nodes to classify: ")
    with open(TREEPATH+"generalTreeData.txt", 'r') as treeInfo, open(TREEPATH+"generalTreeDataClassified.txt", 'w') as newFile:
        for line in treeInfo:
            jsonLine = json.loads(line)
            if jsonLine['size'] >= minNodes:
                print(line)
                newClass = raw_input("Class: ")
                jsonLine['class'] = newClass
                newFile.write(json.dumps(jsonLine))

def userInput():
    option = input("What would you like to do now? \n1: Get info on bitlys \n2: Construct multiple trees \n3: Show tree data \n4: Set classes \n5: Make trees from folder\n")
    if option == 1:
        showInfoOnBitlys()
    elif option == 2:
        startConstructing()
    elif option == 3:
        listTrees()
    elif option == 4:
        setClasses()
    elif option == 5:
        folderPath = raw_input("File path to the folder: ")
        makeTreesFromFolder(folderPath)
    else:
        return

'''Creates trees from sorted files (by link))'''
def makeTreesFromFolder(folderPath):
    for tweetsFile in os.listdir(folderPath):
            propagationTree.create(folderPath+tweetsFile)


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

    for file in os.listdir(TWEETSPATH_REG):
        for line in open(TWEETSPATH_REG + file):
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
