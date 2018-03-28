import json
import anytree
from anytree import Node, AnyNode, RenderTree

def create(tweetsFile):
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
        reference = "ID" + idStr
        idAndName[idStr] = reference  # by searching an id_str, you can get their reference and set them as parent

        if 'quoted_status' in post:
            # this is a quote
            parentIdStr = post['quoted_status_id_str']
            print("Here's the id_str: " + parentIdStr)
            try:
                print("Reference to parent is " + idAndName[parentIdStr])
                parentId = idAndName[parentIdStr]
            except KeyError:
                parentId = "x"+parentIdStr
                idAndName[parentIdStr] = parentId
                parentId = AnyNode(id="x"+str(unknownIdNr))
                unknownIdNr += 1
                #return
            print("Parent id is ")
            print(parentId)
            reference = AnyNode(id=idNr, parent=parentId)
            print("Found quote")
        elif 'retweeted_status' in post:
            # this is a retweet
            print()
        else:
            # this is original content
            reference = AnyNode(id=idNr)
            print(reference)
        idNr += 1
#    ref2 = AnyNode(id=idNr, parent=reference)
    ID200 = AnyNode(id=200, parent=reference)
    #print(RenderTree(reference))
    #for pre, fill, node in RenderTree(reference):
     #   print("%s%s" % (pre, node.id))
    #for key, val in idAndName.items():
    #   print(key + " " + val)



