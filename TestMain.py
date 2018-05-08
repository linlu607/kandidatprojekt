import propagationTreeTest

COLLECTIONPATH = './data/links/collectionByLink/'
TREEPATH = './data/tree/'
def main():
    #tweetsFile = COLLECTIONPATH+"Virtual_staging_Penny_Wise_Pound.txt"
    tweetsFile = COLLECTIONPATH+"Resident_Services_Coordinator_in_Portland.txt"
    propTree = propagationTreeTest.create(tweetsFile)
    propTree.makeNodeTree()

main()

