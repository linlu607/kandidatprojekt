from anytree import RenderTree

class PropTree(object):
    def __init__(self):
        self.roots = []

    def makeSimpleTree(self):
        for root in self.roots:
            print(RenderTree(root))

    def makeIdTree(self):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.id))

    def addRoot(self, newRoot):
        self.roots.append(newRoot)

    def findNodeByIdNr(self, nodeId):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.id == nodeId:
                    return node

    def findNodeByIdStr(self, nodeIdStr):
        for root in self.roots:
            for pre, fill, node in RenderTree(root):
                if node.idStr == nodeIdStr:
                    return node
