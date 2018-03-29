import json
from anytree import AnyNode
from PropTree import PropTree

'''Creates a tree structure'''
def create(tweetsFile):
    # A node should have an idNr (starting on 0), idStr(tweet id), parent.
    propTree = PropTree()  # an instance of a tree
    idNr = 0  # to be ordered by time
    unknownIdNr = 0
    posts = []
    idAndName = {}  # dictionary containing
    print(tweetsFile)
    for line in open(tweetsFile, 'r'):
        posts.append(json.loads(line))  # make a list of json arrays
    print(len(posts))
    for post in posts:
        post['tweet_nr'] = idNr  # adds a new key, which is the id for a post when in the tree
        idStr = post['id_str']
        idAndName[idStr] = idNr  # by searching an id_str, you can get their idNr and set them as parent

        if 'quoted_status' in post:
            # this is a quote
            parentIdStr = post['quoted_status_id_str']
            try:
                parentIdNr = idAndName[parentIdStr]
                parentNode = propTree.findNodeByIdNr(parentIdNr)
            except KeyError:
                # if this node has no parent we want to artificially create one
                parentIdNr = "x" + str(unknownIdNr)  # artificial parents can be distinguished by an x in their id
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
    parentToTest = propTree.findNodeByIdStr("974939595002515457")  # just testing that we can have three levels
    AnyNode(id="test", parent=parentToTest)
    propTree.updatePosts(posts)
    propTree.makeSimpleTree()


