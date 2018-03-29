import json
from anytree import AnyNode
from PropTree import PropTree

def create(tweetsFile):
    # A node should have an idNr (starting on 0), idStr(tweet id), parent.
    propTree = PropTree()
    idNr = 0  # to be ordered by time
    unknownIdNr = 0
    posts = []
    idAndName = {}
    print(tweetsFile)
    for line in open(tweetsFile, 'r'):
        posts.append(json.loads(line))
    print(len(posts))
    for post in posts:
        post['tweetNr'] = idNr
        idStr = post['id_str']
        idAndName[idStr] = idNr  # by searching an id_str, you can get their idNr and set them as parent

        if 'quoted_status' in post:
            # this is a quote
            parentIdStr = post['quoted_status_id_str']
            try:
                parentIdNr = idAndName[parentIdStr]
                parentNode = propTree.findNodeByIdNr(parentIdNr)
            except KeyError:
                parentIdNr = "x" + str(unknownIdNr)
                idAndName[parentIdStr] = parentIdNr
                parentNode = AnyNode(id=parentIdNr, idStr=parentIdStr)
                propTree.addRoot(parentNode)
                unknownIdNr += 1
            AnyNode(id=idNr, idStr=idStr, parent=parentNode)
        elif 'retweeted_status' in post:
            # this is a retweet
            print("Here's a retweet")
        else:
            # this is original content
            reference = AnyNode(id=idNr, idStr=idStr)
            propTree.addRoot(reference)
        idNr += 1
    parentToTest = propTree.findNodeByIdStr("974939595002515457")
    #print(parentToTest)
    thisNode = AnyNode(id="test", parent=parentToTest)
    #propTree.addRoot(thisNode)
    propTree.makeSimpleTree()


