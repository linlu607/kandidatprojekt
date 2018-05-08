import json
import tweepy
from anytree import AnyNode
from PropTree import PropTree
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

TREEPATH = './data/tree/'

'''Creates a tree structure, prints it and saves it to file (from a headline)'''
def create(tweetsFile):
    # A node should have an nodeNr (starting on 0), idStr(tweet id), parent.
    propTree = PropTree()  # an instance of a tree
    nodeNr = 0  # to be ordered by time
    unknownNodeNr = 0
    requestCounter = 1
    posts = []
    for line in open(tweetsFile, 'r'):
        posts.append(json.loads(line))  # make a list of json arrays
    print(len(posts))
    collectFollowers = True
    quotesAndRetweets = 0
    repostedUsers = []
    for post in posts:
        if 'retweeted_status' in post:
            quotesAndRetweets += 1
            repostedUsers.append(post['retweeted_status']['user']['id_str'])
        elif 'quoted_status' in post:
            quotesAndRetweets += 1
            repostedUsers.append(post['quoted_status']['user']['id_str'])
    repostedUsers = json.dumps(repostedUsers)
    print(repostedUsers)
    print(quotesAndRetweets)
    for post in posts:
        post['tweet_nr'] = nodeNr  # adds a new key, which is the id for a post when in the tree (does this do anything really? Should we include post as a JSON in the AnyNode object?)
        idStr = post['id_str']
        idUser = post['user']['id_str']
        print(idUser)
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
            parentNode = getFriendInTree(propTree, idUser, parentIdStr, parentIdUser, requestCounter, len(posts), collectFollowers)
            requestCounter += 1
            if parentNode is None:  # if this node has no parent we want to artificially create one
                parentNodeNr = "x" + str(unknownNodeNr)  # artificial parents can be distinguished by an ex in their id
                parentNode = AnyNode(nodeNr=parentNodeNr, idStr=parentIdStr, idUser=parentIdUser, time=parentTimeStamp, followerCount=parentFollowerCount)
                propTree.addRoot(parentNode)
                print("Parent: " + str(parentIdUser))
                if str(parentIdUser) in repostedUsers:
                   # print("Left: " + str(int(followerCount) * len(repostedUsers) / 5000))
                    #if (int(parentFollowerCount)*len(repostedUsers)/5000) < quotesAndRetweets:
                    propTree.addRootFollowers(parentIdUser, getFollowers(parentIdUser, requestCounter, len(posts)))
                unknownNodeNr += 1
            AnyNode(nodeNr=nodeNr, idStr=idStr, idUser=idUser, parent=parentNode, time=timeStamp, followerCount=followerCount)
        else:
            # this is original content
            reference = AnyNode(nodeNr=nodeNr, idStr=idStr, idUser=idUser, time=timeStamp, followerCount=followerCount)
            propTree.addRoot(reference)
            print("User: " + str(idUser))
            if str(idUser) in repostedUsers:
                print("Left: " + str(int(followerCount) * len(repostedUsers)/5000))
               # if (int(followerCount) * len(repostedUsers)/5000) < quotesAndRetweets:
                propTree.addRootFollowers(idUser, getFollowers(idUser, requestCounter, len(posts)))
        nodeNr += 1
    propTree.updatePosts(posts)
    exporter = JsonExporter(indent=2, sort_keys=True)
    saveFileName = propTree.getFileName()
    open('./data/tree/trees/' + saveFileName + '.txt', 'w').close
    savedFile = open('./data/tree/trees/' + saveFileName + '.txt', 'r+')
    for root in propTree.roots:
        exporter.write(root, savedFile)
        savedFile.write("&\n")

    savedFile.close()
    writeToFile(propTree)
    return propTree

def getTreeAndWriteToFile(tweetsFile):
    tree = printTree(tweetsFile)
    posts = []
    for line in open('./data/manual_of_interest/chosen/' + tweetsFile + '.txt', 'r'):
        posts.append(json.loads(line))  # make a list of json arrays
    tree.updatePosts(posts)
    writeToFile(tree)
    return tree

'''Prints a tree from saved file'''
def printTree(tweetsFile):
    propTree = PropTree()  # an instance of a tree
    importer = JsonImporter()
    rootNr = 0

    with open('./data/tree/trees/' + tweetsFile, 'r') as _file:
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


def getFriendInTree(propTree, idUser, parentIdStr, parentIdUser, requestCounter, tot, collectFollowers):
    access_token = '2499482702-0b9ktOZ8Ooz1rFvvOSSmAs51nNu6qfn7svTUkLV'
    access_token_secret = 'frzzjZHLXSKsKW3XXkGl2zmWM7ZWWDEY4s7reROebnoe7'
    consumer_key = 'Xunyk8FMaSSddtlelb8UDvhRj'
    consumer_secret = 'T8VFupQ5g1RszY6zyrcMA1KN3qztdMx6QFLv2pe2AfErztIC7c'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    #if collectFollowers:
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

def writeToFile(propTree):
    data = propTree.getGeneralJsonData()
    with open(TREEPATH + "generalTreeData.txt", 'a') as general:
        general.write(data + '\n')

def changeInFile(fileName, attribute, value):
    with open(TREEPATH + "generalTreeData.txt", 'r+') as general:
        fileName = str(fileName.replace('.txt', ''))
        for line in general:
            jsonLine = json.loads(line)
            if jsonLine['fileName'] == fileName:
                print("Found match")
                jsonLine[attribute] = value
                newLine = json.dumps(jsonLine)
                general.write(newLine + '\n')
                break
