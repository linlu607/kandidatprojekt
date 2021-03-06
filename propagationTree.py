import json
import tweepy
from anytree import AnyNode
from PropTree import PropTree
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

TREEPATH = './data/tree/'

'''Creates a tree structure, prints it and saves it to file (from a headline)'''
def create(tweetsFile, generalFileName):
    # A node should have an nodeNr (starting on 0), idStr(tweet id), parent.
    propTree = PropTree()  # an instance of a tree
    nodeNr = 0  # to be ordered by time
    unknownNodeNr = 0
    requestCounter = 1
    posts = []
    for line in open(tweetsFile, 'r'):
        posts.append(json.loads(line))  # make a list of json arrays
    print(len(posts))
    quotesAndRetweets = 0
    repostedUsers = {}
    for post in posts:
        userID = None
        if 'retweeted_status' in post:
            userID = post['retweeted_status']['user']['id_str']
        elif 'quoted_status' in post:
            userID = post['quoted_status']['user']['id_str']
        if userID is not None:
            quotesAndRetweets += 1
            if userID in repostedUsers:
                repostedUsers[userID] += 1
            else:
                repostedUsers[userID] = 1
    for post in posts:
        post['tweet_nr'] = nodeNr  # adds a new key, which is the id for a post when in the tree (does this do anything really? Should we include post as a JSON in the AnyNode object?)
        idStr = post['id_str']
        idUser = post['user']['id_str']
        timeStamp = post['created_at']
        followerCount = post['user']['followers_count']
        if 'retweeted_status' in post:
            parentIdStr = post['retweeted_status']['id_str']
            parentIdUser = post['retweeted_status']['user']['id_str']
            parentTimeStamp = post['retweeted_status']['created_at']
            parentFollowerCount = post['retweeted_status']['user']['followers_count']
        elif 'quoted_status' in post:
            parentIdStr = post['quoted_status']['id_str']
            parentIdUser = post['quoted_status']['user']['id_str']
            parentTimeStamp = post['quoted_status']['created_at']
            parentFollowerCount = post['quoted_status']['user']['followers_count']
        if 'retweeted_status' in post or 'quoted_status' in post:
            # make retweet or quote node
            parentNode = getFriendInTree(propTree, idUser, parentIdStr, parentIdUser, requestCounter, len(posts))
            requestCounter += 1
            if parentNode is None:  # if this node has no parent we want to artificially create one
                parentNodeNr = "x" + str(unknownNodeNr)  # artificial parents can be distinguished by an ex in their id
                parentNode = AnyNode(nodeNr=parentNodeNr, idStr=parentIdStr, idUser=parentIdUser, time=parentTimeStamp, followerCount=parentFollowerCount)
                propTree.addRoot(parentNode)
                if str(parentIdUser) in repostedUsers:
                    if int(repostedUsers[parentIdUser]) > int(parentFollowerCount)/5000:
                        if parentIdUser not in propTree.rootFollowers:
                            propTree.addRootFollowers(parentIdUser, getFollowers(parentIdUser, requestCounter, len(posts)))
                            requestCounter += 1
                unknownNodeNr += 1
            AnyNode(nodeNr=nodeNr, idStr=idStr, idUser=idUser, parent=parentNode, time=timeStamp, followerCount=followerCount)
        else:
            # this is original content
            reference = AnyNode(nodeNr=nodeNr, idStr=idStr, idUser=idUser, time=timeStamp, followerCount=followerCount)
            propTree.addRoot(reference)
            if str(idUser) in repostedUsers:
                if int(repostedUsers[idUser]) > int(followerCount)/5000:
                    if idUser not in propTree.rootFollowers:
                        propTree.addRootFollowers(idUser, getFollowers(idUser, requestCounter, len(posts)))
                        requestCounter += 1
        nodeNr += 1
    propTree.updatePosts(posts)
    exporter = JsonExporter(indent=2, sort_keys=True)
    saveFileName = propTree.getFileName()
    open('./data/tree/trees/other/' + saveFileName + '.txt', 'w').close
    savedFile = open('./data/tree/trees/other/' + saveFileName + '.txt', 'w')
    for root in propTree.roots:
        exporter.write(root, savedFile)
        savedFile.write("&\n")

    savedFile.close()
    writeToFile(propTree, generalFileName)
    return propTree

def getTreeAndWriteToFile(tweetsFile, generalFileName):
    tree = printTree(tweetsFile)
    posts = []
    for line in open('./data/manual_of_interest/chosen/' + tweetsFile + '.txt', 'r'):
        posts.append(json.loads(line))  # make a list of json arrays
    tree.updatePosts(posts)
    writeToFile(tree, generalFileName)
    return tree

'''Prints a tree from saved file'''
def printTree(tweetsFile):
    propTree = PropTree()  # an instance of a tree
    importer = JsonImporter()
    rootNr = 0
    with open(tweetsFile, 'r') as _file:
        content = _file.read()

    contentSplit = content.split("&")
    contentSplit.pop()
    for data in contentSplit:
        root = importer.import_(data)
        propTree.addRoot(root)
        rootNr += 1
    return propTree

def getFollowers(idUser, requestCounter, tot):
    access_token = '2499482702-0b9ktOZ8Ooz1rFvvOSSmAs51nNu6qfn7svTUkLV'
    access_token_secret = 'frzzjZHLXSKsKW3XXkGl2zmWM7ZWWDEY4s7reROebnoe7'
    consumer_key = 'Xunyk8FMaSSddtlelb8UDvhRj'
    consumer_secret = 'T8VFupQ5g1RszY6zyrcMA1KN3qztdMx6QFLv2pe2AfErztIC7c'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    followers = []
    retry = True
    while retry:
        try:
            for page in tweepy.Cursor(api.followers_ids, id=idUser).pages():
                followers.extend(page)
            print("Collecting followers for node " + str(requestCounter) + " out of " + str(tot) + "! ")
            retry = False
        except Exception:  # User has been removed or is otherwise inaccessible
            print("Followers not available!")
            return followers

    return followers


def getFriendInTree(propTree, idUser, parentIdStr, parentIdUser, requestCounter, tot):
    access_token = '2499482702-0b9ktOZ8Ooz1rFvvOSSmAs51nNu6qfn7svTUkLV'
    access_token_secret = 'frzzjZHLXSKsKW3XXkGl2zmWM7ZWWDEY4s7reROebnoe7'
    consumer_key = 'Xunyk8FMaSSddtlelb8UDvhRj'
    consumer_secret = 'T8VFupQ5g1RszY6zyrcMA1KN3qztdMx6QFLv2pe2AfErztIC7c'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    rootFollowers = propTree.rootFollowers.get(parentIdUser)
    if rootFollowers is not None:
        for follower in rootFollowers:
            if str(idUser) == str(follower):
                print("Found root follower")
                return propTree.findNodeByIdUser(parentIdUser)

    friends = []
    retry = True
    while retry:
        try:
            for page in tweepy.Cursor(api.friends_ids, id=idUser).pages():
                friends.extend(page)
            print("Collected " + str(requestCounter) + " out of " + str(tot) + "!")
            retry = False
        except Exception:  # User has been removed or is otherwise inaccessible
            print("User not available!")
            return propTree.findNodeByIdStr(parentIdStr)

    usersInTree = propTree.getListIdUser()

    for user in usersInTree:
        for friend in friends:
            if str(user) == str(friend):
                return propTree.findNodeByIdUser(user)

    return propTree.findNodeByIdStr(parentIdStr)

def writeToFile(propTree, generalFileName):
    data = propTree.getGeneralJsonData()
    with open(TREEPATH + generalFileName, 'a') as general:
        general.write(data + '\n')

def changeInFile(fileName, attribute, value):
    general2 = open(TREEPATH + "generalTreeData2.txt", 'a+')
    with open(TREEPATH + "generalTreeData.txt", 'r') as general1:
        fileName = str(fileName.replace('.txt', ''))
        for line in general1:
            jsonLine = json.loads(line)
            if jsonLine['fileName'] == fileName:
                print("Found match")
                jsonLine[attribute] = value
                newLine = json.dumps(jsonLine)
                general2.write(newLine + '\n')
                break
