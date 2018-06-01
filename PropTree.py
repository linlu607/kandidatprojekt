import json
from anytree import RenderTree, LevelOrderGroupIter, LevelOrderIter
import datetime

'''A class for making a tree structure with many roots'''
class PropTree(object):
    def __init__(self):
        self.roots = []
        self.ptPosts = []
        self.data = {}
        self.fileName = ""
        self.rootFollowers = {}

    '''Defines the Twitter posts to be included. Should be JSON arrays'''
    def updatePosts(self, ptPosts):
        self.ptPosts = ptPosts

    def getLink(self):
        return self.ptPosts[0]['entities']['urls'][0]['expanded_url']

    def getFileName(self):
        longName = self.ptPosts[0]['fileName']
        shortName = json.dumps(longName)[1:len(longName)-2]
        self.fileName = shortName
        return shortName

    '''Shows the tree with every attribute of every node'''
    def makeSimpleTree(self):
        for root in self.roots:
            print(RenderTree(root))

    '''Shows the tree with only the idNr of each node'''
    def makeNodeTree(self):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.nodeNr))

    def makeFollowerTree(self):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.followerCount))

    def makeTimeTree(self):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.time))


    def getOriginalCount(self):
        return len(self.roots)


    def getFollowersAndChildren(self):
        followers = []
        children = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                followers.append(node.followerCount)
                children.append(len(node.children))
        return [followers, children]

    def getNrOfChildren(self, node):
        return len(node.children)

    def getNodeFollowerCount(self, node):
        return node.followerCount

    '''Adds a root to the tree'''
    def addRoot(self, newRoot):
        self.roots.append(newRoot)

    def addRootFollowers(self, idUser, followers):
        self.rootFollowers[idUser] = followers

    '''Find a specific node by its idNr'''
    def findNodeByIdNr(self, nodeId):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.nodeNr == nodeId:
                    return node

    '''Find a specific node by its idStr as seen in its JSON array'''
    def findNodeByIdStr(self, IdStr):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.idStr == IdStr:
                    return node

    '''Find a specific node by its idUser'''
    def findNodeByIdUser(self, idUser):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.idUser == idUser:
                    return node

    def findNodesOnLevel(self, level):
        nodeCount = 0
        for root in self.roots:
            nodes = [[node.nodeNr for node in children] for children in LevelOrderGroupIter(root)]
            if len(nodes) > level:
                nodeCount += len(nodes[level])
        return nodeCount

    def getTimeSortedRetweets(self):
        nodes = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.parent is not None:
                    nodes.append(self.stripTime(node.time))
        sortedNodes = sorted(nodes)
        return sortedNodes

    def getFirstTimeStampBySorting(self):
        nodes = []
        for root in self.roots:
            nodes.append(self.stripTime(root.time))
        sortedNodes = sorted(nodes)
        return sortedNodes[0]

    def getFirstTimeStampBySortingLevel(self, times):
        nodes = []
        for time in times:
            nodes.append(self.stripTime(time))
        sortedNodes = sorted(nodes)
        return sortedNodes[0]

    def getNodesAtTimes(self, maxDays):
        sortedNodes = self.getTimeSortedRetweets()
        #print(len(sortedNodes))
        hourStamps = []
        firstStamp = self.getFirstTimeStampBySorting()
        nodesAtTimes = []
        hourStamps.append(0)
        for i in range(0, len(sortedNodes)):
            hourStamps.append(round(((sortedNodes[i] - firstStamp).total_seconds())/3600))
        maxHours = int(max(hourStamps))
        for i in range(0, maxHours+2):
            nodesAtTimes.append(0)
        for value in hourStamps:
            nodesAtTimes[int(value)+1] += 1

        return nodesAtTimes

    def getNodesAtDepths(self):
        minStamps = []
        nodesAtDepths = []
        for root in self.roots:
            nodeGroups = [[node.time for node in children] for children in LevelOrderGroupIter(root)]
            for i in range(0, len(nodeGroups)):
                timeStamp = self.getFirstTimeStampBySortingLevel(nodeGroups[i])
                if len(minStamps) > i:
                    minStamps[i] = min(timeStamp, minStamps[i])
                else:
                    minStamps.append(timeStamp)
        for i in range(0, len(minStamps)):
            nodesAtDepths.append(0)
        sortedNodes = self.getTimeSortedRetweets()

        for i in range(0, len(sortedNodes)):
            j = len(minStamps) - 1
            #print(minStamps[j])
            while sortedNodes[i] <= minStamps[j] and j >= 0:
                nodesAtDepths[j] += 1
                j -= 1
        #print(nodesAtDepths)
        return nodesAtDepths

    def getNodesOnTimeLevels(self):
        nodeCounts = []
        for root in self.roots:
            nodes = [[node.time for node in children] for children in LevelOrderGroupIter(root)]
            #print(nodes)
            for i in range(0, len(nodes)):
                #print(i)
                #1print(len(nodes))
                if len(nodes) > i + 1:
                    timeStamp = self.findMinTimeStamp(nodes[i+1])
                    #print(timeStamp)
                    for time in nodes[i]:
                        if self.stripTime(time) <= timeStamp:
                            if len(nodeCounts) <= i:
                                nodeCounts.append(1)
                            else:
                                nodeCounts[i] += 1

            #print(nodeCounts)
        #for i in range(0, len(nodeCounts) - 1):
            #nodeCounts[i+1] += nodeCounts[i]

        return nodeCounts

    '''Get the timestamp of the node whose tweet was posted first'''
    def getFirstTimeStamp(self):
        unknownTSFound = False
        for root in self.roots:
            if root.nodeNr == "x0":
                uTimeStamp = self.getTimeStampForUnknown(root)
                if uTimeStamp is not None:
                    unknownTSFound = True
                    break
        for post in self.ptPosts:
            if post['tweet_nr'] == 0:
                kTimeStamp = post['created_at']
                break
        if unknownTSFound:
            ts1 = unicode(uTimeStamp)
            ts2 = unicode(kTimeStamp)
            if min(ts1, ts2) == ts1:
                return uTimeStamp
        return kTimeStamp

    def getTimeStampOnLevel(self, maxLevel):
        stamps = []
        #print("Max")
        #print(maxLevel)
        for root in self.roots:
            timeGroups = [[node.time for node in children] for children in LevelOrderGroupIter(root, maxlevel=maxLevel)]
            #print("Len")
            #print(len(timeGroups))
            if len(timeGroups) + 1 >= maxLevel:
                #print(timeGroups[-1])
                minOnLevel = min(timeGroups[-1])
                #print(minOnLevel)
                stamps.append(minOnLevel)
       # print(min(stamps))
        return min(stamps)

    def getTimePeriodRedo(self):
        rootTimes = []
        leafTimes = []
        for root in self.roots:
            rootTimes.append(root.time)
            for pre, fill, node in RenderTree(root):
                if node.is_leaf:
                    leafTimes.append(node.time)
        firstTimeStamp = self.findMinTimeStamp(rootTimes)
        lastTimeStamp = self.findMaxTimeStamp(leafTimes)
        return self.compareStrippedStamps(firstTimeStamp, lastTimeStamp)

    '''Get the timestamp of the node whose tweet was posted last'''
    def getLastTimeStamp(self):
        lastInPosts = self.ptPosts[-1]
        timeStamp = lastInPosts['created_at']
        return timeStamp

    '''Get the timestamp of an artificial parent node'''
    def getTimeStampForUnknown(self, node):
        for post in self.ptPosts:
            if 'quoted_status' in post:
                if post['quoted_status']['id_str'] == node.idStr:
                    quotedPost = post['quoted_status']
                    timeStamp = quotedPost['created_at']
                    return timeStamp
            if 'retweeted_status' in post:
                if post['retweeted_status']['id_str'] == node.idStr:
                    retweetedPost = post['retweeted_status']
                    timeStamp = retweetedPost['created_at']
                    return timeStamp
        return None

    '''Returns the time period between the first and last tweet'''
    def getTimePeriod(self):
        firstTimeStamp = self.getFirstTimeStamp()
        lastTimeStamp = self.getLastTimeStamp()
        return str(self.stripTime(lastTimeStamp) - self.stripTime(firstTimeStamp))

    def compareTimeStamps(self, firstTimeStamp, secondTimeStamp):
        return str(self.stripTime(secondTimeStamp) - self.stripTime(firstTimeStamp))

    def compareStrippedStampsOriginal(self, firstTimeStamp, secondTimeStamp):
        return str(secondTimeStamp - firstTimeStamp)

    def compareStrippedStamps(self, firstTimeStamp, secondTimeStamp):
        timeDiff = secondTimeStamp - firstTimeStamp
        if (timeDiff.seconds / 3600) < 10:
            return str(timeDiff)[:-7] + "0" + str(timeDiff)[len(str(timeDiff)) - 7:]
        return str(timeDiff)

    def stripTime(self, timeStamp):
        offset = timeStamp.split(" ")[4]
        pattern = '%a %b %d %H:%M:%S ' + str(offset) + ' %Y'
        return datetime.datetime.strptime(timeStamp, str(pattern))

    '''Get a list of user ids in a tree'''
    def getListIdUser(self):
        listIdUser = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                listIdUser.append(node.idUser)
        return listIdUser

    def findRootFollowerCount(self):
        followerCounts = []
        for root in self.roots:
            followerCounts.append(root.followerCount)
        return followerCounts

    '''Print a list of user ids in a tree'''
    def printListIdUser(self):
        listIdUser = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("Node " + str(node.idUser))
        return listIdUser

    '''Returns a JSON object with data about the tree'''
    def getGeneralJsonData(self):
        pythonData = self.data
        pythonData['fileName'] = self.getFileName()
        pythonData['link'] = self.getLink()
        pythonData['time'] = self.getTimePeriodRedo()
        pythonData['depth'] = self.getTreeDepth()
        pythonData['size'] = self.getTreeSize()
        pythonData['width'] = self.getMaxWidth()
        pythonData['levelTimes'] = self.getTimeForLevels()
        jsonData = json.dumps(pythonData)
        self.data = pythonData
        return jsonData

    def loadData(self, data):
        self.data = data

    '''Returns the longest chain of posts'''
    def getTreeDepth(self):
        longestChain = 1
        for root in self.roots:
            if root.height + 1 > longestChain:
                longestChain = root.height + 1
        return longestChain

    def getSubTreeDepth(self, node):
        return node.height + 1

    '''Returns the number of nodes in the tree'''
    def getTreeSize(self):
        size = 0
        for root in self.roots:
            size += 1 + self.getNrOfDescendants(root)
        return size

    '''Returns the number of descendants a node has'''
    def getNrOfDescendants(self, node):
        currentSize = 0
        for child in node.children:
            currentSize += 1 + self.getNrOfDescendants(child)
        return currentSize

    '''Returns the diffusion constant of all nodes node'''
    def getDiffusionConstants(self):
        diffDict = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                theChildren = self.getNrOfChildren(node)
                theFollowers = self.getNodeFollowerCount(node)
                if theFollowers is not 0 and theChildren is not 0 and theChildren < 100 and theFollowers < 1000:
                    dataTuple = (theFollowers, theChildren)
                    diffDict.append(dataTuple)
        return diffDict

    def findMinTimeStamp(self, stamps):
        strpStamps = []
        for stamp in stamps:
            strpStamps.append(self.stripTime(stamp))
        return min(strpStamps)

    def findMaxTimeStamp(self, stamps):
        strpStamps = []
        for stamp in stamps:
            strpStamps.append(self.stripTime(stamp))
        return max(strpStamps)

    def getTimeForLevels(self):
        group = 0
        levelTimes = {}
        firstRoot = True
        highestIndex = 0
        for root in self.roots:
            levelIndex = 0
            timeGroups = [[node.time for node in children] for children in LevelOrderGroupIter(root)]
            for level in timeGroups:
                minOnLevel = self.findMinTimeStamp(level)
                if firstRoot or highestIndex < levelIndex:
                    levelTimes[levelIndex] = minOnLevel
                    if highestIndex < levelIndex:
                        highestIndex += 1
                else:
                    levelTimes[levelIndex] = min(minOnLevel, levelTimes[levelIndex])
                levelIndex += 1
            group += 1
            firstRoot = False
        times = {}
        times[0] = 0
        index = 1
        while index < len(levelTimes):
            times[index] = self.compareStrippedStamps(levelTimes[0], levelTimes[index])
            index += 1
        return times

    '''Returns the maximum number of children of any node'''
    def getMaxWidth(self):
        maxWidthFound = 0
        nrOfChildren = 0
        for root in self.roots:
            if not root.is_leaf:
                nrOfChildren = self.getHighestChildCount(root)
            if nrOfChildren > maxWidthFound:
                maxWidthFound = nrOfChildren
        return maxWidthFound

    '''Returns the maximum number of siblings in a descendant chain of a node'''
    def getHighestChildCount(self, node):
        currentSize = 0
        grandchildSize = 0
        for child in node.children:
            currentSize += 1
            grandchildSize = self.getHighestChildCount(child)
        return max(currentSize, grandchildSize)
