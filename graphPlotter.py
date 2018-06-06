import json

import scipy
from anytree import RenderTree, LevelOrderGroupIter
from matplotlib import pyplot as plt
from matplotlib import dates as dt
import datetime
import xlwt
from scipy.interpolate import spline, interp1d

import propagationTree
import os
import numpy as np
import pylab

GENERAL = './data/tree/'
TREEPATH = './data/tree/trees/'

def makeLevelGraph():
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("BBC_Fox", cell_overwrite_ok=True)
    dataFile = open('./data/tree/generalTreeData.txt', 'r')
    index = 0
    for line in dataFile:
        jsonLine = json.loads(line)
        sheet1.write(0, index, jsonLine['fileName'])
        levelDict = jsonLine['levelTimes']
        for key, val in levelDict.items():
            print(key)
            sheet1.write(int(key)+1, index, val)
        index += 1

    book.save("plots.xls")

def CDFRetweetsDepth(generalFiles):
    colors = ['teal', 'salmon', 'orange']
    colorIndex = 0
    yValsAll = []
    xValsAll = []
    fullSize = 0
    fullCounts = []

    for generalFile in generalFiles:
        restValues = []
        for i in range(0, 11):
            restValues.append(0)
        nodeCounts = []
        totalSize = 0
        if generalFile.endswith('Top.txt'):
            folder = 'top/'
            label = "Top set"
        elif generalFile.endswith('Random.txt'):
            folder = 'random/'
            label = "Random set"
        else:
            folder = 'TDS/'
            label = "Three day set"

        color = colors[colorIndex]
        colorIndex += 1
        for line in open(GENERAL + generalFile, 'r'):

            jsonLine = json.loads(line)
            size = jsonLine['size']
            tree = propagationTree.printTree(TREEPATH + folder + jsonLine['fileName'] + '.txt')
            newCounts = tree.getNodesOnTimeLevels()
            for i in range(0, len(newCounts)):
                if len(nodeCounts) > i:
                    nodeCounts[i] += newCounts[i]
                else:
                    nodeCounts.append(newCounts[i])

            #if len(nodeCounts) > i:
            #    nodeCounts[i] += size - sum(newCounts)
            #else:
            #    nodeCounts.append(size - sum(newCounts))
            #restValues[i] += size - sum(newCounts)
            totalSize += size

        for i in range(0, len(nodeCounts)):
            if len(fullCounts) > i:
                fullCounts[i] += nodeCounts[i]
            else:
                fullCounts.append(nodeCounts[i])
        yVals = []
        xVals = []
        totalNodesDone = []
        xVals.append(0)
        yVals.append(0)
        for i in range(0, len(nodeCounts) - 1):
            nodeCounts[i+1] += nodeCounts[i]
        print(nodeCounts)
        for i in range(0, len(nodeCounts)):
            if i != 0:
                value = nodeCounts[i]
                totalNodesDone.append(value)
                yVals.append(value/float(totalSize))
            else:
                yVals.append(nodeCounts[i]/float(totalSize))
                totalNodesDone.append(nodeCounts[i])
            xVals.append(i+1)
        print(xVals)
        print(yVals)
        plt.plot(xVals, yVals, color=color, marker='.', label=label)
        #print(restValues)
        #for i in range(0, len(restValues) - 1):
        #    restValues[i+1] += restValues[i]
        #restFracs = map(lambda x: x / float(totalSize), restValues)
        #plt.plot(range(0, len(restValues)), restFracs, color=color, linestyle='--')
        fullSize += totalSize
    for i in range(0, len(fullCounts)-1):
        fullCounts[i+1] += fullCounts[i]

    yValsAll.append(0)
    xValsAll.append(0)
    for i in range(0, len(fullCounts)):
        yValsAll.append(fullCounts[i]/float(fullSize))
        xValsAll.append(i+1)

    print(fullCounts)
    print(yValsAll)
    plt.plot(xValsAll, yValsAll, color='black', marker='.', linestyle='--', label="All")


    print(fullSize)
    plt.xticks(range(0, 11))
    plt.legend(fontsize='x-large')
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=17)
    plt.grid(axis='x', linestyle='dashed')
    #plt.semilogy()
    plt.show()

def CDFRetweetTime(generalFiles):
    fullNodes = []
    for generalFile in generalFiles:
        setCounts = []
        totalSize = 0
        if generalFile.endswith('Top.txt'):
            folder = 'top/'
            label = "Top set"
            maxDays = 12
        elif generalFile.endswith('Random.txt'):
            folder = 'random/'
            label = "Random set"
            maxDays = 12
        elif generalFile.endswith("Other.txt"):
            folder = 'other/'
            label = "Bottom set"
            maxDays = 12
        else:
            folder = 'TDS/'
            label = "Three day set"
            maxDays = 3
        for line in open(GENERAL + generalFile, 'r'):
            jsonLine = json.loads(line)
            if jsonLine['depth'] > 1:
                if 'days' in jsonLine['time']:
                    days = jsonLine['time'].split(" ")[0]
                    if int(days) <= maxDays:
                        tree = propagationTree.printTree(TREEPATH + folder + jsonLine['fileName'] + '.txt')
                        nodesAtTimes = tree.getNodesAtTimes(maxDays)
                        totalSize += nodesAtTimes[-1]
                        setCountsLen = len(setCounts)
                        for i in range(0, len(nodesAtTimes)):
                            if setCountsLen > i:
                                setCounts[i] += nodesAtTimes[i]
                            else:
                                setCounts.append(nodesAtTimes[i])

        for i in range(0, len(setCounts) - 1):
            setCounts[i+1] += setCounts[i]
        totalSize = float(setCounts[-1])
        normedCounts = map(lambda x: 100*round(x/totalSize, 2), setCounts)
        if folder == 'other/':
            plt.plot(range(0, len(setCounts)), normedCounts, color='orchid', label=label, linewidth=2)
        else:
            plt.plot(range(0, len(setCounts)), normedCounts, label=label, linewidth=2)
        for i in range(0, len(setCounts)):
            if len(fullNodes) > i:
                fullNodes[i] += setCounts[i]
            else:
                if i > 0:
                    fullNodes.append(setCounts[i]+fullNodes[-1] - setCounts[i-1])
                else:
                    fullNodes.append(setCounts[i])
        if len(fullNodes) > len(setCounts):
            for i in range(len(setCounts), len(fullNodes)):
                fullNodes[i] += setCounts[-1]
        #print(setCounts)
        #print(len(setCounts))
    #print(fullNodes)
    fullSize = float(fullNodes[-1])
    normedFull = map(lambda x: 100*round(x/fullSize, 2), fullNodes)
    #normedFull = [round(elem, 2) for elem in normedFull]
    plt.plot(range(0, len(fullNodes)), normedFull, label="All", color='black', linestyle='--', linewidth=2)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=17)
    plt.xticks(range(0, 13*24, 6))
    #plt.xticks([0, 6, 24, 48, 72, 96])
    plt.legend(fontsize='xx-large')
    plt.grid()
    plt.show()

def CDFRetweetDepth2(generalFiles):
    fullNodes = []
    for generalFile in generalFiles:
        setCounts = []
        totalSize = 0
        if generalFile.endswith('Top.txt'):
            folder = 'top/'
            label = "Top set"
            maxDays = 12
        elif generalFile.endswith('Random.txt'):
            folder = 'random/'
            label = "Random set"
            maxDays = 12
        elif generalFile.endswith("Other.txt"):
            folder = 'other/'
            label = "Bottom set"
            maxDays = 12
        else:
            folder = 'TDS/'
            label = "Three day set"
            maxDays = 3
        for line in open(GENERAL + generalFile, 'r'):
            jsonLine = json.loads(line)
            if jsonLine['depth'] > 1:
                if 'days' in jsonLine['time']:
                    days = jsonLine['time'].split(" ")[0]
                    if int(days) <= maxDays:
                        tree = propagationTree.printTree(TREEPATH + folder + jsonLine['fileName'] + '.txt')
                        nodesAtTimes = tree.getNodesAtDepths()
                        totalSize += nodesAtTimes[-1]
                        setCountsLen = len(setCounts)
                        for i in range(0, len(nodesAtTimes)):
                            if setCountsLen > i:
                                setCounts[i] += nodesAtTimes[i]
                            else:
                                if i > 0:
                                    setCounts.append(nodesAtTimes[i] - nodesAtTimes[i-1] + setCounts[-1])
                                else:
                                    setCounts.append(nodesAtTimes[i])
                        if len(setCounts) > len(nodesAtTimes):
                            for i in range(len(nodesAtTimes), len(setCounts)):
                                setCounts[i] += nodesAtTimes[-1]
        totalSize = float(setCounts[-1])
        normedCounts = map(lambda x: round(x/totalSize, 2), setCounts)
        if folder == 'other/':
            plt.plot(range(0, len(setCounts)), normedCounts, color='orchid', label=label, linewidth=2, marker='D')
        else:
            plt.plot(range(0, len(setCounts)), normedCounts, label=label, linewidth=2, marker='D')
        for i in range(0, len(setCounts)):
            if len(fullNodes) > i:
                fullNodes[i] += setCounts[i]
            else:
                if i > 0:
                    fullNodes.append(setCounts[i]+fullNodes[-1] - setCounts[i-1])
                else:
                    fullNodes.append(setCounts[i])
        if len(fullNodes) > len(setCounts):
            for i in range(len(setCounts), len(fullNodes)):
                fullNodes[i] += setCounts[-1]
        print(setCounts)
        print(len(setCounts))
    print(fullNodes)
    fullSize = float(fullNodes[-1])
    normedFull = map(lambda x: round(x/fullSize, 2), fullNodes)
    plt.plot(range(0, len(fullNodes)), normedFull, label="All", color='black', linestyle='--', linewidth=2, marker='D')
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=17)
    plt.xticks(range(0, 12))
    plt.legend(fontsize='xx-large', loc='lower right')
    plt.grid()
    plt.show()

def getFollowerCount(jsonLine):
    fileName = jsonLine['fileName']
    tree = propagationTree.printTree(TREEPATH + '/other/' + fileName + '.txt')
    return tree.findRootFollowerCount()

def plotTimeSeriesMediumFollowers():
    dataFile = open('./data/tree/generalTreeData.txt', 'r')
    maxTimes = []
    maxLevels = []
    maxX = "00:00:00"
    maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
    minX = maxX
    for line in dataFile:
        times = []
        levels = []
        jsonLine = json.loads(line)
        followerCount = getFollowerCount(jsonLine)
        followers = 0
        for i in followerCount:
            followers += i
        mediumCount = followers/len(followerCount)
        name = str(len(followerCount)) + "/ " + str(mediumCount)
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "00:00:00"
            stripedStamp = stripTime(str(timeStamp))
            times.append(stripedStamp)
        maxTimes.append(max(times))
        maxLevels.append(len(levelDict))
        newTimes = []
        for time in times:
            if time == times[0]:
                zeroTime = time
            elif time == times[1]:
                firstTime = time
                newTimes.append(zeroTime)
            else:
                newTimes.append(zeroTime + (time-firstTime))
        if mediumCount > 2000000:
            color='maroon'
        elif mediumCount > 1000000:
            color = 'darkred'
        elif mediumCount > 200000:
            color='firebrick'
        elif mediumCount > 100000:
            color='red'
        elif mediumCount > 10000:
            color = 'orangered'
        elif mediumCount > 1000:
            color = 'darkorange'
        else:
            color='orange'
        if len(newTimes) != 0:
            print(newTimes)
            plt.plot(newTimes, levels[1:], marker='o', markersize=4, color=color, linestyle='--', linewidth=0.8)
    plt.legend(loc='center right')
    plt.title("Color coded by medium amount of followers")
    xax = plt.gca().get_xaxis()
    xax.set_major_formatter(dt.DateFormatter('%d' + " days, " + '%H:%M:%S'))
    plt.ylim(0, max(maxLevels))
    maxX = datetime.datetime.strptime("3, 20:00:00", '%d, %H:%M:%S')
    plt.xticks(rotation=45)
    plt.xlim(minX, maxX)
    plt.grid(True)
    plt.show()

def plotTimeSeriesBlack(fileAndPath, title):
    dataFile = open(fileAndPath, 'r')
    maxTimes = []
    maxLevels = []
    maxX = "00:00:00"
    maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
    minX = maxX
    for line in dataFile:
        times = []
        levels = []
        jsonLine = json.loads(line)
        name = jsonLine['fileName']
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "00:00:00"
            stripedStamp = (stripTime(str(timeStamp)) - minX).total_seconds()/3600
            times.append(stripedStamp)
        maxTimes.append(max(times))
        maxLevels.append(len(levelDict))
        plt.plot(times, levels, markersize=3, linewidth=1.5, linestyle='--', marker='D')
        print(times)
        print(levelDict)
   # plt.legend(loc='center right')
    #xax = plt.gca().get_xaxis()
    #xax.set_major_formatter(dt.DateFormatter('%H' + " hours"))
    #plt.ylim(0, max(maxLevels))
    #maxX = datetime.datetime.strptime("3, 20:00:00", '%d, %H:%M:%S')
    #maxX = max(maxTimes)
    plt.xticks(range(0, 1024, 12))
    #plt.xlim(minX, maxX)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=17)
    #plt.title(title)
    plt.grid()
    plt.show()

def plotTimeSeriesRoots():
    dataFile = open('./data/tree/generalTreeData.txt', 'r')
    maxTimes = []
    maxLevels = []
    maxX = "00:00:00"
    maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
    minX = maxX
    for line in dataFile:
        times = []
        levels = []
        jsonLine = json.loads(line)
        followerCount = getFollowerCount(jsonLine)
        followers = 0
        for i in followerCount:
            followers += i
        mediumCount = followers/len(followerCount)
        name = str(len(followerCount)) + "/ " + str(mediumCount)
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "00:00:00"
            stripedStamp = stripTime(str(timeStamp))
            times.append(stripedStamp)
        maxTimes.append(max(times))
        maxLevels.append(len(levelDict))
        newTimes = []
        for time in times:
            if time == times[0]:
                zeroTime = time
            elif time == times[1]:
                firstTime = time
                newTimes.append(zeroTime)
            else:
                newTimes.append(zeroTime + (time-firstTime))
        if len(followerCount) > 299:
            color='darkred'
        elif len(followerCount) > 9:
            color='firebrick'
        elif len(followerCount) > 5:
            color='red'
        elif len(followerCount) > 1:
            color='orangered'
        else:
            color='orange'
        if len(newTimes) != 0:
            print(newTimes)
            plt.plot(newTimes, levels[1:], label=name, marker='o', color=color, linestyle='--', linewidth=0.5)
    plt.legend(loc='center right')
    plt.title("Color coded by amount of roots")
    xax = plt.gca().get_xaxis()
    xax.set_major_formatter(dt.DateFormatter('%d' + " days, " + '%H:%M:%S'))
    plt.ylim(0, max(maxLevels))
    maxX = datetime.datetime.strptime("3, 20:00:00", '%d, %H:%M:%S')
    plt.xticks(rotation=45)
    plt.xlim(minX, maxX)
    plt.grid(True)
    plt.show()
def plotTimeSeriesFirstRetweet():
    dataFile = open('./data/tree/generalTreeDataOther.txt', 'r')
    maxTimes = []
    maxLevels = []
    maxX = "00:00:00"
    maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
    minX = maxX
    for line in dataFile:
        times = []
        levels = []
        jsonLine = json.loads(line)
        followerCount = getFollowerCount(jsonLine)
        followers = 0
        for i in followerCount:
            followers += i
        mediumCount = followers/len(followerCount)
        name = str(len(followerCount)) + "/ " + str(mediumCount)
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "00:00:00"
            stripedStamp = (stripTime(str(timeStamp)) - minX).total_seconds()/3600
            times.append(stripedStamp)
        maxTimes.append(max(times))
        maxLevels.append(len(levelDict))
        newTimes = []
        for time in times:
            if time == times[0]:
                zeroTime = time
            elif time == times[1]:
                firstTime = time
                newTimes.append(zeroTime)
            else:
                newTimes.append(zeroTime + (time-firstTime))
        if len(newTimes) != 0:
            plt.plot(newTimes, levels[1:], marker='D', markersize=3, linestyle='--', linewidth=1.4)
    #plt.legend(loc='center right')
    #xax = plt.gca().get_xaxis()
    #xax.set_major_formatter(dt.DateFormatter('%d' + " days, " + '%H' + " hours"))
    #plt.ylim(0, max(maxLevels))
    #maxX = datetime.datetime.strptime("4, 00:00:00", '%d, %H:%M:%S')
    plt.xticks(range(0, 1024, 24))
    #plt.xlim(minX, maxX)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=17)
    plt.grid(True)
    plt.show()

def plotLevelPatterns(generalFile, TREEPATH):
    for line in open(GENERAL + generalFile, 'r'):
        jsonLine = json.loads(line)
        depth = jsonLine['depth']
        tree = propagationTree.printTree(TREEPATH + jsonLine['fileName'] + '.txt')
        nodeCounts = []
        try:
            for i in range(0, depth):
                nodeCounts.append(tree.findNodesOnLevel(i))
            scaledDepths = []
            scaledDepths.append(0)
            print(depth)
            for x in range(1, depth-1):
                scaledDepths.append(x*10/float(depth-1))
            if depth > 1:
                scaledDepths.append(10)
            scaledCounts = [y*10 / float(depth) for y in nodeCounts]
            size = jsonLine['size']
            if size > 500:
                color = 'teal'
            elif size > 100:
                color = 'firebrick'
            elif size > 50:
                color = 'green'
            else:
                color = 'orchid'
            plt.plot(scaledDepths, scaledCounts, color=color, marker='o', markersize=2, linestyle='--', linewidth=1)
            #plt.plot(range(0, depth), nodeCounts, color=color, linestyle='--')
        except WindowsError:
            print("Error for " + str(jsonLine['fileName']))
            print(depth)
            #tree.makeNodeTree()
    plt.grid(True)
    plt.show()

def depthsForAll(generalFiles):
    depths = []
    for generalFile in generalFiles:
        for line in open(GENERAL + generalFile, 'r'):
            depth = json.loads(line)['depth']
            depths.append(depth)
    final = []
    sortedDepths = sorted(depths)
    for i in range(0, sortedDepths[-1] + 1):
        final.append(0)
    for value in sortedDepths:
        final[value] += 1
    total = float(sum(final))
    finalTot = list(final)
    for i in range(len(final) - 2, 0, -1):
        finalTot[i] += finalTot[i+1]
    fractionsTot = map(lambda y: y / total, finalTot)
    fractions = map(lambda x: x / total, final)
    plt.bar(range(0, sortedDepths[-1] + 1), fractionsTot, color='teal', label="Total links that reached this depth")
    plt.bar(range(0, sortedDepths[-1] + 1), fractions, color='skyblue', label="Links that reached only to this depth")
    plt.legend(fontsize='xx-large')
    plt.tick_params(axis='both', labelsize=16)
    plt.grid(axis='y', linestyle='dashed')
    plt.xticks(range(0, sortedDepths[-1] + 1))
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.show()


def makeScatter(PATH):
    dataPoints = 0
    for treeFile in os.listdir(PATH):

        if os.path.isfile(PATH + treeFile):
            print("Tree: " + str(treeFile))
            tree = propagationTree.printTree(PATH + treeFile)
            scatterData = tree.getDiffusionConstants()
            if len(scatterData) > 0:
                print("Had scatterdata")
                print(scatterData)
                plt.scatter(*zip(*scatterData), marker=".", color='#000000')
                dataPoints += 1

        else:
            print("Folder: " + str(treeFile))
            for subTreeFile in os.listdir(PATH + treeFile + "/"):
                if os.path.isfile(PATH + treeFile + "/" + subTreeFile):
                    print("Subtree: " + str(subTreeFile))
                    subTree = propagationTree.printTree(PATH + treeFile + "/" + subTreeFile)
                    subScatterData = subTree.getDiffusionConstants()
                    if len(subScatterData) > 0:
                        print("Had data")
                        print(subScatterData)
                        plt.scatter(*zip(*subScatterData), marker=".", color='#000000')
                        dataPoints += 1
                    else:
                        print("Had no data")
                        print(subScatterData)
    print(dataPoints)
    plt.xlabel("Followers")
    plt.ylabel("Retweeters")
    plt.show()

def makeWhisker(PATH):
   fig, ax= plt.subplots(1)
   fold = 0
   zones = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
   for folder in os.listdir(PATH):
       for treeFile in os.listdir(PATH + folder + "/"):
           if os.path.isfile(PATH + folder + "/" + treeFile):
               tree = propagationTree.printTree(folder + "/" + treeFile)
               data = tree.getDiffusionConstants()
               for node in data:
                   if 1 <= node[0] < 10:
                       zones[0+fold].append(node[1])
                   elif 11 <= node[0] < 100:
                       zones[1+fold].append(node[1])
                   elif 101 <= node[0] < 1000:
                       zones[2+fold].append(node[1])
                   elif 1001 <= node[0] < 10000:
                       zones[3+fold].append(node[1])
                   elif 10001 <= node[0] < 100000:
                       zones[4+fold].append(node[1])
                   elif 100001 <= node[0] < 1000000:
                       zones[5+fold].append(node[1])
       fold += 6
   for x in range(0, 6):
       zoneGroups = [zones[x], zones[x+6], zones[x+12]]
       bp = ax.boxplot(zoneGroups, 0, '', positions=[x+(2*x), x+1+(2*x), x+2+(2*x)], widths=0.2)
       setBoxColors(bp)
   ax.set_xticklabels([' ', 'A', '', ' ', 'B', '', ' ', 'C', '', ' ', 'D', '', ' ', 'E', '', ' ', 'F', ''])
   ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
   ax.tick_params(axis="both", labelsize=15)
   plt.show()

def followerRetweetScatter(PATH):
    dataPoints = 0
    for folder in os.listdir(PATH):
        for treeFile in os.listdir(PATH + folder + '/'):
            tree = propagationTree.printTree(PATH + folder + '/' + treeFile)
            retweetCounts = tree.getFollowersAndChildren()
            if retweetCounts is not None:
                plt.scatter(retweetCounts[0], retweetCounts[1], marker=".", color='black')
                dataPoints += 1
    print(dataPoints)
    plt.xlabel("Followers")
    plt.ylabel("Children")
    plt.show()

def followerRetweetBox():
    labelVal = 0
    sets = 4
    labels = []
    for i in range(0, sets + 1):
        labels.append(range(i, 26 + i, sets + 1))
    print(labels)
    #labels = [range(0, 21, 4), range(1, 22, 4), range(2, 23, 4), range(3, 24, 4)]
    for folder in os.listdir(TREEPATH):
        reposts = [[], [], [], [], [], []]
        if folder == 'TDS':
            color = 'steelblue'
            label = "Three day set"
        elif folder == "top":
            color = 'salmon'
            label = "Top set"
        elif folder == "other":
            color = 'goldenrod'
            label = "Bottom set"
        else:
            color = 'darkolivegreen'
            label = "Random set"
        for treeFile in os.listdir(TREEPATH+folder + '/'):
           # print(reposts)
            tree = propagationTree.printTree(TREEPATH + folder + '/' + treeFile)
            retweetCounts = tree.getFollowersAndChildren()
            if retweetCounts is not None:
                for i in range(0, len(retweetCounts[0])):
                    counts = retweetCounts[0][i]
                    children = retweetCounts[1][i]
                    if children != 0:
                        if counts < 10:
                            index = 0
                        elif counts < 100:
                            index = 1
                        elif counts < 1000:
                            index = 2
                        elif counts < 10000:
                            index = 3
                        elif counts < 100000:
                            index = 4
                        else:
                            index = 5

                        reposts[index].append(retweetCounts[1][i])
        positions = labels[labelVal]
        print(len(reposts))
        plt.boxplot(reposts, positions=positions, boxprops=dict(color=color, linewidth=2), medianprops=dict(linewidth=2), showfliers=False) #, labels=labels[labelVal])
        plt.bar([0], [0], color='white', edgecolor=color, label=label, linewidth=2, width=10)
        labelVal += 1
    plt.semilogy()

    plt.legend(fontsize='xx-large')
    plt.tick_params(axis='y', labelsize=17)
    plt.tick_params(axis='x', labelsize=15)
    plt.xticks(labels[4], [10, 100, 1000, 10000, 100000, 1000000])
    plt.grid(linestyle='dashed')
    plt.show()

def followerRetweetScatterTop():
    PATH = './data/tree/trees/top/'
    for treeFile in os.listdir(PATH):
        tree = propagationTree.printTree(PATH + treeFile)
        retweetCounts = tree.getFollowersAndChildren()
        if retweetCounts is not None:
            plt.scatter(retweetCounts[0], retweetCounts[1], marker=".", color='black')
    plt.xlabel("Followers")
    plt.ylabel("Children")
    plt.show()

def followerDepthWidthScatter(PATH):
    followers = []
    values = []
    addedFollowers = {}
    for folder in os.listdir(PATH):
        for treeFile in os.listdir(PATH + folder + '/'):
            if not treeFile.endswith('TDSretry'):
                tree = propagationTree.printTree(PATH + folder + '/' + treeFile)
                for root in tree.roots:
                    followerCount = root.followerCount
                    fraction = float(tree.getHighestChildCount(root))/float(tree.getSubTreeDepth(root))
                    followers.append(followerCount)
                    values.append(fraction)
                    if followerCount in addedFollowers:
                        addedFollowers[followerCount][0] += fraction
                        addedFollowers[followerCount][1] += 1
                    else:
                        addedFollowers[followerCount] = [fraction, 1]
    followerCounts = []
    meanFracs = []
    iteration = 0
    keys = []
    counts = []

    item = 0
    totalLength = len(addedFollowers)
    print(totalLength)
    groupLength = int(totalLength/50) + 1
    print(groupLength)
    keys.append(0)
    counts.append(0)
    for key, val in sorted(addedFollowers.items()):
        iteration += 1
        if item < groupLength and iteration < totalLength:
            item += 1
        else:
            followerCounts.append(sum(keys)/len(keys))
            meanFracs.append(sum(counts)/len(counts))
            item = 0
            keys = []
            counts = []
        keys.append(key)
        counts.append(val[0] / val[1])

    newMeans = []
    start = 3
    averageLength = start*2

    newMeans.append(meanFracs[0])
    for i in range(start, len(meanFracs) - averageLength):
        newMean = 0
        index = -averageLength + start
        while index <= averageLength:
            newMean += meanFracs[i + index]
            index += 1
        newMeans.append(newMean/averageLength)

    print(len(followerCounts))
    print(len(newMeans))
    newFollowers = followerCounts[:-(averageLength+start-1)]
    f2 = scipy.interpolate.interp1d(newFollowers, newMeans, kind='slinear')
    fnew = np.logspace(np.log10(newFollowers[0])+0.1, np.log10(newFollowers[-1])-0.1)

    plt.tick_params(axis='x', labelsize=16)
    plt.tick_params(axis='y', labelsize=17)
    plt.scatter(followers, values, marker='.', color='teal', s=15) #13, steelgrey?
    #plt.semilogx()
    #plt.plot([0], [0], color='white')
    #plt.plot(fnew, f2(fnew), color='black', linewidth=2)
    plt.show()

def followerSizeScatter(PATH):
    sizes = []
    followers = []
    for folder in os.listdir(PATH):
        for treeFile in os.listdir(PATH + folder + '/'):
            tree = propagationTree.printTree(PATH + folder + '/' + treeFile)
            for root in tree.roots:
                followers.append(root.followerCount)
                sizes.append(tree.getNrOfDescendants(root))
    plt.scatter(followers, sizes)
    plt.show()

def plotTimeSeries():
    dataFile = open('./data/tree/generalTreeData.txt', 'r')

    for line in dataFile:
        maxY = 0
        maxX = "00:00:00"
        maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
        minX = maxX
        times = []
        levels = []
        jsonLine = json.loads(line)
        name = jsonLine['fileName']
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "0:00:00"
            times.append(stripTime(str(timeStamp)))
        maxY = max(maxY, len(levels))
        maxX = max(maxX, times[-1])
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
     #          ncol=2, mode="expand", borderaxespad=0.)

    xax = plt.gca().get_xaxis()
    xax.set_major_formatter(dt.DateFormatter('%H:%M:%S'))
    print("Maxx")
    print(maxX)
    plt.ylim(0, maxY)
    #plt.xlim(minX, maxX)
    plt.show()
    return
    plt.gcf().autofmt_xdate()
    plt.show()

def plotTimeSeriesAll():
    dataFile = open('./data/tree/generalTreeData.txt', 'r')
    for line in dataFile:
        maxY = 0
        maxX = "00:00:00"
        maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
        minX = maxX
        times = []
        levels = []
        jsonLine = json.loads(line)
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "00:00:00"
            times.append(stripTime(str(timeStamp)))
    fig, ax = plt.subplots()
    ax.plot(times)
    ax.xaxis.set_major_formatter(dt.DateFormatter('%H'))
    ax.format_xdata = dt.DateFormatter('%H:%M:%S')
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    plt.show()

def retweetRate(generalFile):
    topfiles = []
    randomfiles = []
    otherfiles = []
    generalFiles = ['generalTreeDataTop.txt', 'generalTreeDataRandom.txt', 'generalTreeDataOther.txt']
    for line in open(GENERAL + generalFiles[0], 'r'):
        topfiles.append(json.loads(line)['fileName'])
    for line in open(GENERAL + generalFiles[1], 'r'):
        randomfiles.append(json.loads(line)['fileName'])
    for line in open(GENERAL + generalFiles[2], 'r'):
        otherfiles.append(json.loads(line)['fileName'])
    data = {}
    counter = {'bbc': 0, 'bre': 0, 'fox': 0, 'huf': 0, 'cnn': 0, 'tim': 0, 'gua': 0, 'reu': 0, 'cbs': 0, 'was': 0}
    labels = {'bre': 'Breitbart', 'bbc': 'BBC', 'fox': 'Fox News', 'huf': 'Huffington Post', 'cnn': 'CNN',
              'tim': 'The Times', 'gua': 'The Guardian', 'cbs': 'CBS', 'reu': 'Reuters', 'was': 'Washington Post'}
    colors = {'bre': 'tomato', 'bbc': 'palegreen', 'fox': 'lightsteelblue', 'huf': 'plum', 'cnn': 'lightpink',
              'tim': 'khaki', 'gua': 'teal', 'cbs': 'firebrick', 'reu': 'magenta', 'was': 'goldenrod'}

    for line in open('./data/tree/' + generalFile, 'r'):
        ignore = False
        print(line)
        jsonLine = json.loads(line)
        contentClass = jsonLine['class']
        if contentClass not in counter:
            if contentClass == 'other':
                ignore = True
                counter[contentClass] = 0
            else:
                counter[contentClass] = 0
                print(contentClass)
                print(jsonLine['link'])
                ignore = raw_input("Ignore?")
                if ignore == 'n':
                    labels[contentClass] = raw_input("Set name for class: ")
                    colors[contentClass] = raw_input("Set color for class: ")
        counter[contentClass] += 1
        link = jsonLine['fileName']
        if link in topfiles:
            pathEnding = '/top/'
        elif link in randomfiles:
            pathEnding = '/random/'
        elif link in otherfiles:
            pathEnding = '/other/'
        else:
            print("Not found")
            ignore = True
        if not ignore:
            PATH = './data/tree/trees' + pathEnding
            tree = propagationTree.printTree(PATH + link + '.txt')
            originals = tree.getOriginalCount()
            retweets = int(jsonLine['size']) - originals
            retweetRate = float(retweets)/float(originals)
            labelName = contentClass + " " + str(counter[contentClass])
            data[labelName] = retweetRate
    sortedData = sorted(data.items(), key=lambda x: x[1])
    for tuple_ in sortedData:
        if int(tuple_[0][3:]) == 0:
            label = labels[tuple_[0][:3]]
            plt.bar(tuple_[0], tuple_[1], color=colors[tuple_[0][:3]], label=label)
        else:
            plt.bar(tuple_[0], tuple_[1], color=colors[tuple_[0][:3]])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', labelsize=15)
    plt.legend(fontsize='x-large', loc='upper left')
    plt.grid(axis='y', alpha=0.5, linestyle='dashed')
    plt.semilogy()
    #plt.ylabel("Retweet rate")
    #plt.xlabel("Tweets color coded by news outlet")
    plt.show()

def retweetRateBox(generalFile):
    dataTop = {'bbc': [], 'bre': [], 'fox': [], 'huf': [], 'cnn': [], 'tim': [], 'gua': [], 'cbs': [], 'was': []}
    dataRandom = {'bbc': [], 'bre': [], 'fox': [], 'huf': [], 'cnn': [], 'tim': [], 'gua': [], 'cbs': [], 'was': []}
    dataOther = {'bbc': [], 'bre': [], 'fox': [], 'huf': [], 'cnn': [], 'tim': [], 'gua': [], 'cbs': [], 'was': []}
    topfiles = []
    randomfiles = []
    otherfiles = []
    generalFiles = ['generalTreeDataTop.txt', 'generalTreeDataRandom.txt', 'generalTreeDataOther.txt']
    for line in open(GENERAL + generalFiles[0], 'r'):
        topfiles.append(json.loads(line)['fileName'])
    for line in open(GENERAL + generalFiles[1], 'r'):
        randomfiles.append(json.loads(line)['fileName'])
    for line in open(GENERAL + generalFiles[2], 'r'):
        otherfiles.append(json.loads(line)['fileName'])
    data = {}
    counter = {'bbc': 0, 'bre': 0, 'fox': 0, 'huf': 0, 'cnn': 0, 'tim': 0, 'gua': 0, 'cbs': 0, 'was': 0}
    labels = {'bre': 'Breitbart', 'bbc': 'BBC', 'fox': 'Fox News', 'huf': 'Huffington Post', 'cnn': 'CNN',
              'tim': 'The Times', 'gua': 'The Guardian', 'cbs': 'CBS', 'was': 'Washington Post'}
    colors = {'bre': 'tomato', 'bbc': 'palegreen', 'fox': 'lightsteelblue', 'huf': 'plum', 'cnn': 'lightpink',
              'tim': 'khaki', 'gua': 'teal', 'cbs': 'firebrick', 'reu': 'magenta', 'was': 'goldenrod'}
    toBox = {'bbc': [], 'bre': [], 'fox': [], 'huf': [], 'cnn': [], 'tim': [], 'gua': [], 'reu': [], 'cbs': [], 'was': []}
    for line in open('./data/tree/' + generalFile, 'r'):
        ignore = False
        jsonLine = json.loads(line)
        contentClass = jsonLine['class']
        if contentClass not in counter:
            if contentClass == 'other' or contentClass == 'twi' or contentClass == 'reu':
                ignore = True
                counter[contentClass] = 0
            else:
                counter[contentClass] = 0
                print(contentClass)
                print(jsonLine['link'])
                ignore = raw_input("Ignore?")
                if ignore == 'n':
                    labels[contentClass] = raw_input("Set name for class: ")
                    colors[contentClass] = raw_input("Set color for class: ")
        counter[contentClass] += 1
        link = jsonLine['fileName']
        if link in topfiles:
            pathEnding = '/top/'
            toDict = dataTop
        elif link in randomfiles:
            pathEnding = '/random/'
            toDict = dataRandom
        elif link in otherfiles:
            pathEnding = '/other/'
            toDict = dataOther
        else:
            print("Not found")
            ignore = True
        if not ignore:
            PATH = './data/tree/trees' + pathEnding
            tree = propagationTree.printTree(PATH + link + '.txt')
            originals = tree.getOriginalCount()
            retweets = int(jsonLine['size']) - originals
            if int(jsonLine['size'] != tree.getTreeSize()):
                print(link)
                if link in topfiles:
                    print("toperror")
                elif link in randomfiles:
                    print("randerror")
                elif link in otherfiles:
                    print("othererror")
                else:
                    print("error")
                retweets = tree.getTreeSize() - originals
                print(retweets)
            retweetRate = float(retweets)/float(originals)
            if contentClass != 'reu':
                toDict[contentClass].append(retweetRate)
            labelName = contentClass + " " + str(counter[contentClass])
            data[labelName] = retweetRate
            toBox[contentClass].append(retweetRate)
            if int(retweetRate) == 57:
                print(link)
                print("57 found")
    position = 5
    positions2 = []
    vals = []
    toshow = []
    colorstoshow = []
    names = []
    for key, val in toBox.items():
        if key != 'reu':
            toshow.append(val)
            colorstoshow.append(colors[key])
            positions = [0, position]
            position += 2
            newVal = []
            newVal.append([0])
            newVal.append(val)
            names.append(labels[key])
            positions2.append(positions)
            plt.boxplot(newVal, positions=positions, widths=0.7, boxprops=dict(color=colors[key], linewidth=2),
                        medianprops=dict(linewidth=2), showfliers=False)

    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=16)
    plt.xticks(range(5, 25, 2), names, rotation=45)
    totalDict = {'bbc': [], 'bre': [], 'fox': [], 'huf': [], 'cnn': [], 'tim': [], 'gua': [], 'cbs': [], 'was': []}
    dicts = [dataTop, dataRandom, dataOther]
    print(dataOther)
    for dictionary in dicts:
        print("New")
        for key, val in dictionary.items():
            if len(val) != 0:
                medium = round(sum(val)/len(val), 2)
                #print(str(labels[key]) + ": " + str(medium) + "  " + str(len(val)))
                totalDict[key].extend(val)
    print("Total")
    for key, val in totalDict.items():
        if len(val) != 0:
            medium = round(sum(val)/len(val), 2)
            print(str(labels[key]) + ": " + str(medium) + "  " + str(len(val)))
            if key == 'tim':
                print(val)
                print(sorted(val))

    #print(dataTop)
    #print(dataRandom)
    #print(dataOther)

    #plt.show()


def mediumRateURL(generalFile, PATH):
    data = {}
    counter = {'bbc': 0, 'bre': 0, 'fox': 0, 'huf': 0, 'cnn': 0, 'tim': 0, 'gua': 0}
    for line in open('./data/tree/' + generalFile, 'r'):
        jsonLine = json.loads(line)
        contentClass = jsonLine['class']
        labelName = contentClass + " " + str(counter[contentClass])
        counter[contentClass] += 1
        link = jsonLine['fileName']
        tree = propagationTree.printTree(PATH + link + '.txt')
        originals = tree.getOriginalCount()
        retweets = int(jsonLine['size']) - originals
        retweetRate = float(retweets) / float(originals)
        data[labelName] = retweetRate
    sortedData = sorted(data.items(), key=lambda x: x[1])
    labels = {'bre': 'Breitbart', 'bbc': 'BBC', 'fox': 'Fox News', 'huf': 'Huffington Post', 'cnn': 'CNN',
              'tim': 'The Times', 'gua': 'The Guardian'}
    colors = {'bre': 'red', 'bbc': 'green', 'fox': 'blue', 'huf': 'purple', 'cnn': 'pink', 'tim': 'orange',
              'gua': 'grey'}
    sourceValues = {}
    for tuple_ in sortedData:
        if tuple_[0][3:] not in sourceValues:
            print(int(tuple_[0][3:]))
            sourceValues[tuple_[0][:3]] = tuple_[1]
        else:
            print(int(tuple_[0][3:]))
            sourceValues[tuple_[0][:3]] += tuple_[1]
    values = []
    keys = []
    colorChoice = []
    for key, val in sourceValues.items():
        values.append(val/counter[key])
        keys.append(key)
        colorChoice.append(colors[key])
    #plt.bar(keys, values, color=colorChoice)
    data = []
    valueFile = open('./data/newsSourceData.txt', 'w+')
    for i in range(0, len(values)):
        valueFile.write(labels[keys[i]] + " " + str(round(values[i], 1)) + " " + str(counter[keys[i]]) + "\n")

    #plt.table(cellText=data, colLabels=["Medium rate", "Occurances"], rowLabels=keys, loc='top')
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.legend()
    plt.ylabel("Retweet rate")
    plt.xlabel("Tweets color coded by news outlet")
    #plt.show()

def depthWidth(fileList, PATH):

    for file in fileList:
        thisFile = open(PATH + file, 'r')
        for line in thisFile:
            sizes = []
            fractions = []
            jsonLine = json.loads(line)
            width = jsonLine['width']
            depth = jsonLine['depth']
            size = jsonLine['size']
            if width == 0:
                width = size
            sizes.append(size)
            fractions.append(width/depth)
            if size >500:
                color = 'red'
            elif size > 100:
                color = 'green'
            elif size > 20:
                color = 'purple'
            else:
                color = 'blue'
            plt.scatter(sizes, fractions, color=color, marker='.')
    #plt.xlabel("Size")
    #plt.ylabel("Width/Depth")
    plt.show()

def timeBar(files, PATH):
    times = []
    for generalFile in files:
        for line in open(PATH + generalFile, 'r'):
            jsonLine = json.loads(line)
            time = jsonLine['time']
            times.append(time)
    timeTuples = {}
    sortedTimes = sorted(times)
    #print(sortedTimes)
    timeIntervals = 10800
    x = timeIntervals
    timeTuples[x] = 0
    timeValues = []
    timeValues.append(timeIntervals)
    entries = []
    entries.append(0)
    for time in sortedTimes:
        timeDelta = stripTime(time)-datetime.datetime(1900, 1, 1)
        seconds = round(timeDelta.total_seconds())
        if int(seconds) < x:
            timeTuples[x] += 1
            #print("Entries:")
            #print(entries)
            #print("List index: ")
            #print(entries[-1])
            entries[-1] += 1
        else:
            while int(seconds) > x:
                x += timeIntervals
            timeTuples[x] = 1
            timeValues.append(x)
            entries.append(1)
    print(timeValues)
    print(entries)
    hourValues = map(lambda y: y/3600, timeValues)
    print(hourValues)
    nrOfValues = sum(entries)
    percentages = map(lambda y: round(y*100/float(nrOfValues), 2), entries)
    print(percentages)
    plt.semilogy()
    plt.bar(hourValues, entries, width=3)
    plt.show()

def depthWidthSize(fileList, PATH):
    widths = []
    depths = []
    sizes = []
    for file in fileList:
        thisFile = open(PATH + file, 'r')
        for line in thisFile:
            jsonLine = json.loads(line)
            width = jsonLine['width']
            depth = jsonLine['depth']
            size = jsonLine['size']
            if width == 0:
                width = size
            widths.append(width)
            depths.append(depth)
            sizes.append(size*1.4)
    plt.scatter(widths, depths, marker='.', color='mediumturquoise', s=sizes)
    plt.semilogx()
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=16)
    plt.show()

def plotDataOnNodes():
    PATH = './data/tree/nodeData/'

    for folder in os.listdir(PATH):
        maxReaches = []
        trees = []
        if folder == 'TDS':
            color = 'steelblue'
            label = "Three day set"
        elif folder == "top":
            color = 'salmon'
            label = "Top set"
        elif folder == "other":
            color = 'magenta'
            label = "Bottom set"
        else:
            color = 'darkolivegreen'
            label = "Random set"
        for treeFile in os.listdir(PATH + folder + '/'):
            treeReach = 0
            treeNode = 0
            with open(PATH + folder + '/' + treeFile, 'r') as treeFile:
                for line in treeFile:
                    try:
                        maxReaches[treeNode] += treeReach
                    except IndexError:
                        maxReaches.append(treeReach)
                    try:
                        trees[treeNode] += 1
                    except IndexError:
                        trees.append(1)
                    jsonLine = json.loads(line)
                    treeReach = jsonLine['max_reach']
                    treeNode += 1
        maxReachesAverages = [x / y for x, y in zip(maxReaches, trees)]
        print(maxReachesAverages)
        plt.plot(range(0, len(maxReachesAverages)), maxReachesAverages, marker='o', markersize=0, color=color, linewidth=2, label=label)
    plt.legend(loc='upper left')
    ax = plt.gca()
    #ax.set_xlim([0, 7300])
    #ax.set_ylim([0, 50000])
    plt.grid(True)
    plt.show()

def stripTime(timeStamp):
    pattern = '%H:%M:%S'
    if "day" in timeStamp or "days" in timeStamp:
        newTime = timeStamp.replace("day, ", "").replace("days, ", "")
        toAdd = datetime.timedelta(hours=int(newTime.split()[0])*24)
        timeStamp = newTime.replace(newTime.split()[0] + " ", "")
        ts = datetime.datetime.strptime(timeStamp, str(pattern)) + toAdd
        return ts
    return datetime.datetime.strptime(timeStamp, str(pattern))

def maxReach():
    PATH = './data/tree/nodeData/'
    for folder in os.listdir(PATH):
        allMaxReaches = []
        allCounts = []
        if folder == 'TDS':
            color = 'teal'
            label = "Three day set"
        elif folder == "top":
            color = 'darkorange'
            label = "Top set"
        elif folder == "other":
            color = 'orchid'
            label = "Bottom set"
        else:
            color = 'darkolivegreen'
            label = "Random set"
        for treeFile in os.listdir(PATH + folder + '/'):
            maxReaches = []
            counts = []
            treeNode = 0
            with open(PATH + folder + '/' + treeFile, 'r') as treeFile:
                for line in treeFile:
                    maxReaches.append(json.loads(line)['max_reach'])
                    counts.append(1)
                    treeNode += 1
                if 0 < treeNode < 5000:
                    allMaxReaches.append(maxReaches)
                    allCounts.append(counts)
        newList = []
        newCounts = []
        longest = 0
        for i in range(0, len(allMaxReaches)):
            longest = max(longest, len(allMaxReaches[i]))
        for i in range(0, longest):
            newList.append(0)
            newCounts.append(0)

        for i in range(0, len(allMaxReaches)):
            maxReachList = allMaxReaches[i]
            for j in range(0, len(maxReachList)):
                newList[j] += maxReachList[j]
                newCounts[j] += allCounts[i][j]
            for k in range(len(maxReachList), len(newList)):
                newList[k] += maxReachList[-1]

        averages = []
        for i in range(0, len(newList)):
            averages.append((newList[i])/newCounts[i])
        newAve = []
        newAve.append(0)
        newAve.extend(averages)
        plt.plot(range(0, len(averages)+1), newAve, color=color, label=label, marker='.')
    plt.legend(fontsize='xx-large')
    plt.grid(axis='x')
    plt.tick_params(axis='x')
    plt.xticks(range(0, 400, 10))
    plt.show()

#plotTimeSeriesBlack(GENERAL + 'generalTreeDataOther.txt', 'hej') # done for top and random
#plotTimeSeriesFirstRetweet()
#retweetRateBox('classifiedTweets.txt')
#followerDepthWidthScatter(GENERAL+'trees/')
#depthWidthSize(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt'], GENERAL) #should this be used?
#CDFRetweetDepth2(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt', 'generalTreeDataOther.txt'])
#CDFRetweetTime(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt', 'generalTreeDataOther.txt'])
#followerRetweetScatter('./data/tree/trees/')
#followerRetweetBox()
#depthsForAll(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt', 'generalTreeDataOther.txt'])
#plotDataOnNodes()
maxReach()