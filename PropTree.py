import dateutil
from anytree import RenderTree, AnyNode
import datetime
from dateutil import parser
'''A class for making a tree structure with many roots'''
class PropTree(object):
    def __init__(self):
        self.roots = []
        self.ptPosts = []

    '''Defines the Twitter posts to be included. Should be JSON arrays'''
    def updatePosts(self, ptPosts):
        self.ptPosts = ptPosts

    '''Shows the tree with every attribute of every node'''
    def makeSimpleTree(self):
        for root in self.roots:
            print(RenderTree(root))

    '''Shows the tree with only the idNr of each node'''
    def makeNodeTree(self):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.nodeNr))

    '''Adds a root to the tree'''
    def addRoot(self, newRoot):
        self.roots.append(newRoot)

    '''Find a specific node by its idNr'''
    def findNodeByIdNr(self, nodeId):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.id == nodeId:
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

    '''Get the timestamp of the node whose tweet was posted first'''
    def getFirstTimeStamp(self):
        unknownTSFound = False
        knownTSFound = False
        for root in self.roots:
            if root.id == "x0":
                uTimeStamp = self.getTimeStampForUnknown(root)
                unknownTSFound = True
                break
        for post in self.ptPosts:
            if post['tweet_nr'] == 0:
                kTimeStamp = post['created_at']
                knownTSFound = True
                break
        if unknownTSFound and knownTSFound:
            ts1 = parser.parse(uTimeStamp)
            ts2 = parser.parse(kTimeStamp)
            print(str(ts1) + " " + str(ts2))

            return min(ts1, ts2)
        elif unknownTSFound:
            return datetime.datetime.strptime(uTimeStamp, '%b %d %H:%M:%S %Y')
        elif knownTSFound:
            return datetime.datetime.strptime(kTimeStamp, '%b %d %H:%M:%S %Y')

    '''Get the timestamp of an artificial parent node'''
    def getTimeStampForUnknown(self, node):
        for post in self.ptPosts:
            if 'quoted_status' in post:
                if post['quoted_status_id_str'] == node.idStr:
                    quotedPost = post['quoted_status']
                    timeStamp = quotedPost['created_at']
                    return timeStamp
        return None

    '''Get a list of user ids in a tree'''
    def getListIdUser(self):
        listIdUser = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                listIdUser.append(node.idUser)
        return listIdUser

    '''Print a list of user ids in a tree'''
    def printListIdUser(self):
        listIdUser = []
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("Node" + str(node.idUser))
        return listIdUser
