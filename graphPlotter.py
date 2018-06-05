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
        #normedCounts = [round(elem, 2) for elem in normedCounts]
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
        print(setCounts)
        print(len(setCounts))
    print(fullNodes)
    fullSize = float(fullNodes[-1])
    normedFull = map(lambda x: 100*round(x/fullSize, 2), fullNodes)
    #normedFull = [round(elem, 2) for elem in normedFull]
    plt.plot(range(0, len(fullNodes)), normedFull, label="All", color='black', linestyle='--', linewidth=2)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=17)
    plt.xticks(range(0, 13*24, 6))
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
    plt.xticks(range(0, 11))
    plt.legend(fontsize='xx-large', loc='lower right')
    plt.grid()
    plt.show()

def getFollowerCount(jsonLine):
    fileName = jsonLine['fileName']
    tree = propagationTree.printTree(TREEPATH + '/TDS/' + fileName + '.txt')
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
    plt.xticks(range(0, 1024, 48))
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
    fig, ax = plt.subplots(1)
    for treeFile in os.listdir(PATH):
        if os.path.isfile(PATH + treeFile):
            tree = propagationTree.printTree(PATH + treeFile)
            size = tree.getTreeSize()
            scatterData = tree.getDiffusionConstants()
            if scatterData:
                if 97 < size < 99 or 313 < size < 315 or 911 < size < 913 or 1794 < size < 1796 or 2629 < size < 2631 \
                        or 4607 < size < 4609:
                    pointLabel = str(size + (100 - (size % 100))) + " nodes"
                else:
                    pointLabel = None
                ax.scatter(*zip(*scatterData), marker=".", s=size, color='#' + '{0:06X}'.format((size+10000)*300),
                            alpha=0.2, label=pointLabel)
        else:
            for subTreeFile in os.listdir(PATH + treeFile + "/"):
                if os.path.isfile(PATH + treeFile + "/" + subTreeFile):
                    subTree = propagationTree.printTree(PATH + treeFile + "/" + subTreeFile)
                    subSize = subTree.getTreeSize()
                    subScatterData = subTree.getDiffusionConstants()
                    if subScatterData:
                        if 97 < subSize < 99 or 313 < subSize < 315 or 911 < subSize < 913 or 1794 < subSize < 1796 \
                                or 2119 < subSize < 2941 or 4607 < subSize < 4609:
                            subPointLabel = str(subSize + (100 - (subSize % 100)))
                        else:
                            subPointLabel = None
                        ax.scatter(*zip(*subScatterData), marker=".", s=subSize,
                                    color='#' + '{0:06X}'.format((subSize+10000)*300), alpha=0.2,
                                    label=subPointLabel)
    ax.semilogx()
    ax.semilogy()
    ax.tick_params(axis="both", labelsize=15)
    handles, labels = ax.get_legend_handles_labels()

    handles = [handles[2], handles[1], handles[0], handles[3], handles[5], handles[4]]
    labels = [labels[2], labels[1], labels[0], labels[3], labels[5], labels[4]]

    legend = ax.legend(handles, labels, loc='upper center', borderpad=1, labelspacing=1, ncol=6,
                       fontsize=15, title="Number of Nodes in Tree of Origin")
    plt.setp(legend.get_title(), fontsize=20)
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
        #setBoxColors(bp)
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
    for i in range(0, sets):
        labels.append(range(i, 21 + i, sets + 1))
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
            color = 'magenta'
            label = "Bottom set"
        else:
            color = 'darkolivegreen'
            label = "Random set"
        for treeFile in os.listdir(TREEPATH + folder + '/'):
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
        plt.boxplot(reposts, positions=positions, boxprops=dict(color=color, linewidth=2), medianprops=dict(linewidth=2)
                    , showfliers=False, labels=labels[labelVal])
        plt.bar([0], [0], color='white', edgecolor=color, label=label, linewidth=2, width=10)
        labelVal += 1
    plt.semilogy()

    plt.legend(fontsize='xx-large')
    plt.tick_params(axis='y', labelsize=17)
    plt.tick_params(axis='x', labelsize=15)
    plt.xticks(labels[3], [10, 100, 1000, 10000, 100000, 1000000])
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
    intervals = 100000

    '''for key, val in sorted(addedFollowers.items()):
        if key < intervals * iteration * iteration * iteration/100:
            keys.append(key)
            counts.append(val[0]/val[1])
        else:
            iteration += 1
            if len(keys) > 0:
                followerCounts.append(sum(keys)/len(keys))
                meanFracs.append(sum(counts)/len(counts))
            else:
                followerCounts.append(intervals * iteration * iteration * iteration/100)
                meanFracs.append(0)
            keys = []
            counts = []
            keys.append(key)
            counts.append(val[0]/val[1])'''
    item = 0
    totalLength = len(addedFollowers)
    print(totalLength)
    groupLength = int(totalLength/30) + 1
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
    '''
    for key, val in sorted(addedFollowers.items()):
        followerCounts.append(key)
        meanFracs.append(val[0]/val[1])
    '''
    newMeans = []
    start = 1
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
    plt.scatter(followers, values, marker='.', color='steelblue', s=13) #13, steelgrey?
    plt.semilogx()
    plt.plot(fnew, f2(fnew), color='black', marker='o')
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

def retweetRate(generalFile, PATH):
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
        retweetRate = float(retweets)/float(originals)
        data[labelName] = retweetRate
    sortedData = sorted(data.items(), key=lambda x: x[1])
    labels = {'bre': 'Breitbart', 'bbc': 'BBC', 'fox': 'Fox News', 'huf': 'Huffington Post', 'cnn': 'CNN', 'tim': 'The Times', 'gua': 'The Guardian'}
    colors = {'bre': 'tomato', 'bbc': 'palegreen', 'fox': 'lightsteelblue', 'huf': 'plum', 'cnn': 'lightpink', 'tim': 'khaki', 'gua': 'teal'}
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
        if file == "generalTreeData.txt":
            color = "red"
            label = "Three Day Set"
        elif file == "generalTreeDataTop.txt":
            color = "green"
            label = "Top"
        elif file == "generalTreeDataRandom.txt":
            color = "blue"
            label = "Random"
        elif file == "generalTreeDataOther.txt":
            color = "grey"
            label = "Bottom"
        else:
            color = "black"
            label = "ERROR"
        plt.scatter(10, 2, marker='.', color=color, s=0.00001, alpha=0.5, label=label)
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
        plt.scatter(widths, depths, marker='.', color=color, s=sizes, alpha=0.5)
        widths = []
        depths = []
        sizes = []
    plt.semilogx()
    plt.legend(fontsize='xx-large', markerscale=10000)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=16)
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
        plt.plot(range(0, len(maxReachesAverages)), maxReachesAverages, marker='o', markersize=0, color=color, linewidth=2, label=label)
    plt.legend(loc='upper left')
    ax = plt.gca()
    #ax.set_xlim([0, 7300])
    #ax.set_ylim([0, 50000])
    plt.grid(True)
    plt.show()

#plotTimeSeriesBlack(GENERAL + 'generalTreeData.txt', 'hej') # done for top and random
#plotTimeSeriesFirstRetweet()
#retweetRate('classifiedTweets.txt', GENERAL + 'trees/topAndRandom/')
#followerDepthWidthScatter(GENERAL+'trees/')
#depthWidthSize(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt'], GENERAL) #should this be used?
#followerDepthWidthScatter(GENERAL+'trees/')
#depthWidthSize(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt', 'generalTreeDataOther.txt'], GENERAL) #should this be used?
#makeScatter(TREEPATH)
plotDataOnNodes()
#CDFRetweetDepth2(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt'])
#CDFRetweetTime(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt'])
#followerRetweetScatter('./data/tree/trees/')
#followerRetweetBox()
#depthsForAll(['generalTreeData.txt', 'generalTreeDataTop.txt', 'generalTreeDataRandom.txt'])