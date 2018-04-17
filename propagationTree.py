import json
import time
import tweepy
from anytree import AnyNode
from PropTree import PropTree
from anytree.exporter import JsonExporter

'''Creates a tree structure'''
def create(tweetsFile):
    # A node should have an nodeNr (starting on 0), idStr(tweet id), parent.
    propTree = PropTree()  # an instance of a tree
    nodeNr = 0  # to be ordered by time
    unknownNodeNr = 0
    posts = []
    print(tweetsFile)
    for line in open(tweetsFile, 'r'):
        posts.append(json.loads(line))  # make a list of json arrays
    print(len(posts))
    for post in posts:
        post['tweet_nr'] = nodeNr  # adds a new key, which is the id for a post when in the tree (does this do anything really? Should we include post as a JSON in the AnyNode object?)
        idStr = post['id_str']
        idUser = post['user']['id_str']

        if 'retweeted_status' in post:
            parentIdStr = post['retweeted_status']['id_str']
            parentIdUser = post['retweeted_status']['user']['id_str']
        elif 'quoted_status' in post:
            parentIdStr = post['quoted_status']['id_str']
            parentIdUser = post['quoted_status']['user']['id_str']

        if 'retweeted_status' in post or 'quoted_status' in post:
            # make retweet or quote node
            parentNode = getFriendInTree(propTree, idUser, parentIdStr)
            if parentNode is None:  # if this node has no parent we want to artificially create one
                parentNodeNr = "ex" + str(unknownNodeNr)  # artificial parents can be distinguished by an ex in their id
                parentNode = AnyNode(nodeNr=parentNodeNr, idStr=parentIdStr, idUser=parentIdUser)
                propTree.addRoot(parentNode)
                unknownNodeNr += 1
            AnyNode(nodeNr=nodeNr, idStr=idStr, idUser=idUser, parent=parentNode)
        else:
            # this is original content
            reference = AnyNode(nodeNr=nodeNr, idStr=idStr, idUser=idUser)
            propTree.addRoot(reference)
        nodeNr += 1
    propTree.updatePosts(posts)
    exporter = JsonExporter(indent=2, sort_keys=True)

    open('./data/tree/trees/' + tweetsFile[30:-4] + '.txt', 'w').close
    savedFile = open('./data/tree/trees/' + tweetsFile[30:-4] + '.txt', 'r+')
    for root in propTree.roots:
        exporter.write(root, savedFile)
        savedFile.write("\n")

    savedFile.close()
    propTree.makeSimpleTree()


def getFriendInTree(propTree, idUser, parentIdStr):
    access_token = '2499482702-0b9ktOZ8Ooz1rFvvOSSmAs51nNu6qfn7svTUkLV'
    access_token_secret = 'frzzjZHLXSKsKW3XXkGl2zmWM7ZWWDEY4s7reROebnoe7'
    consumer_key = 'Xunyk8FMaSSddtlelb8UDvhRj'
    consumer_secret = 'T8VFupQ5g1RszY6zyrcMA1KN3qztdMx6QFLv2pe2AfErztIC7c'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    friends = []
    exceeded = True
    while exceeded:
        try:
            for page in tweepy.Cursor(api.friends_ids, id=idUser).pages():
                friends.extend(page)
            exceeded = False
        except Exception:
            print("Request limit reached, retrying in 90 seconds...")
            time.sleep(91)
            exceeded = True

    usersInTree = propTree.getListIdUser()

    for user in usersInTree:
        for friend in friends:
            if str(user) == str(friend):
                return propTree.findNodeByIdUser(user)

    if propTree.findNodeByIdStr(parentIdStr) is not None:
        return propTree.findNodeByIdStr(parentIdStr)
