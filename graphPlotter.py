import json

import os
from matplotlib import pyplot as plt
from matplotlib import dates as dt
import datetime
import time
import xlwt
import propagationTree

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


def getFollowerCount(jsonLine):
    fileName = jsonLine['fileName']
    tree = propagationTree.printTree('/bbcfox/' + fileName+'.txt')
    return tree.findRootFollowerCount()


def plotTimeSeriesColors():
    dataFile = open('./data/tree/generalTreeData_bbcfox.txt', 'r')
    for line in dataFile:
        maxY = 0
        maxX = "00:00:00"
        maxX = datetime.datetime.strptime(maxX, '%H:%M:%S')
        minX = maxX
        times = []
        levels = []
        jsonLine = json.loads(line)
        followerCount = getFollowerCount(jsonLine)
        followers = 0
        for i in followerCount:
            followers += i
        mediumCount = followers/len(followerCount)
        name = str(len(followerCount)) + ", " + str(mediumCount)
        levelDict = jsonLine['levelTimes']
        for i in range(0, len(levelDict)):
            levels.append(i)
            timeStamp = levelDict[str(i)]
            if timeStamp == 0:
                timeStamp = "0:00:00"
            times.append(stripTime(str(timeStamp)))
        plt.plot(times, levels, label=name)
        maxY = max(maxY, len(levels))
        maxX = max(maxX, times[-1])
    plt.legend(loc='center right')
    xax = plt.gca().get_xaxis()
    xax.set_major_formatter(dt.DateFormatter('%H:%M:%S'))
    plt.ylim(0, maxY-0.5)
    plt.xlim(minX, maxX)
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
        if "bbc" in name:
            plt.plot(times, levels, color='firebrick')
        elif "fxn" in name:
            plt.plot(times, levels, '-.', color='royalblue')
        maxY = max(maxY, len(levels))
        maxX = max(maxX, times[-1])
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
     #          ncol=2, mode="expand", borderaxespad=0.)

    xax = plt.gca().get_xaxis()
    xax.set_major_formatter(dt.DateFormatter('%H:%M:%S'))
    print("Maxx")
    print(maxX)
    plt.ylim(0, maxY)
    plt.xlim(minX, maxX)
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
   # ax.format_ydata = levels
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
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

def makeScatter(PATH):
    for treeFile in os.listdir(PATH):
        if os.path.isfile(PATH + treeFile):
            tree = propagationTree.printTree(treeFile)
            scatterData = tree.getDiffusionConstants()
            if scatterData:
                plt.scatter(*zip(*scatterData), marker=".", color='#000000')
    plt.xlabel("Followers")
    plt.ylabel("Children")
    saveScatter(str(int(time.time())))

def saveScatter(titel):
    plt.savefig("./data/tree/scatter/" + titel)
