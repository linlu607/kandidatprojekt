import os

SORTEDPATH = './data/tweets/sortedFiles/'
def makeMiniTweet(bigTweet):
    miniTweet = {}

    miniTweet["created_at"] = bigTweet["created_at"]
    miniTweet["id_str"] = bigTweet["id_str"]
    miniTweet["user"] = {}
    miniTweet["user"]["id_str"] = bigTweet["user"]["id_str"]
    miniTweet["user"]["followers_count"] = bigTweet["user"]["followers_count"]
    miniTweet["user"]["friends_count"] = bigTweet["user"]["friends_count"]
    miniTweet["user"]["statuses_count"] = bigTweet["user"]["statuses_count"]
    miniTweet["quote_count"] = bigTweet["quote_count"]
    miniTweet["retweet_count"] = bigTweet["retweet_count"]
    miniTweet['entities'] = {}
    miniTweet["entities"]["urls"] = [{}]
    bitly = bigTweet["entities"]["urls"][0]['expanded_url']
    miniTweet["entities"]["urls"][0]['expanded_url'] = bitly
    miniTweet['fileName'] = ''.join(e for e in bitly if e.isalnum()).replace("http", "").replace("\\", "")[:20]

    if "retweeted_status" in bigTweet:
        miniTweet["retweeted_status"] = {}
        miniTweet["retweeted_status"]["created_at"] = bigTweet["retweeted_status"]["created_at"]
        miniTweet["retweeted_status"]["id_str"] = bigTweet["retweeted_status"]["id_str"]
        miniTweet["retweeted_status"]["user"] = {}
        miniTweet["retweeted_status"]["user"]["id_str"] = bigTweet["retweeted_status"]["user"]["id_str"]
        miniTweet["retweeted_status"]["user"]["followers_count"] = bigTweet["retweeted_status"]["user"][
            "followers_count"]
        miniTweet["retweeted_status"]["user"]["friends_count"] = bigTweet["retweeted_status"]["user"]["friends_count"]
        miniTweet["retweeted_status"]["user"]["statuses_count"] = bigTweet["retweeted_status"]["user"]["statuses_count"]
        miniTweet["retweeted_status"]["quote_count"] = bigTweet["retweeted_status"]["quote_count"]
        miniTweet["retweeted_status"]["retweet_count"] = bigTweet["retweeted_status"]["retweet_count"]
        try:
            miniTweet["retweeted_status"]['entities'] = {}
            miniTweet["retweeted_status"]["entities"]["urls"] = [{}]
            miniTweet["retweeted_status"]["entities"]["urls"][0]['expanded_url'] = \
            bigTweet["retweeted_status"]["entities"]["urls"][0]['expanded_url']
        except IndexError:
            return None

    if "quoted_status" in bigTweet:
        miniTweet["quoted_status"] = {}
        miniTweet["quoted_status"]["created_at"] = bigTweet["quoted_status"]["created_at"]
        miniTweet["quoted_status"]["id_str"] = bigTweet["quoted_status"]["id_str"]
        miniTweet["quoted_status"]["user"] = {}
        miniTweet["quoted_status"]["user"]["id_str"] = bigTweet["quoted_status"]["user"]["id_str"]
        miniTweet["quoted_status"]["user"]["followers_count"] = bigTweet["quoted_status"]["user"]["followers_count"]
        miniTweet["quoted_status"]["user"]["friends_count"] = bigTweet["quoted_status"]["user"]["friends_count"]
        miniTweet["quoted_status"]["user"]["statuses_count"] = bigTweet["quoted_status"]["user"]["statuses_count"]
        miniTweet["quoted_status"]["quote_count"] = bigTweet["quoted_status"]["quote_count"]
        miniTweet["quoted_status"]["retweet_count"] = bigTweet["quoted_status"]["retweet_count"]
        try:
            miniTweet["quoted_status"]['entities'] = {}
            miniTweet["quoted_status"]["entities"]["urls"] = [{}]
            miniTweet["quoted_status"]["entities"]["urls"][0]['expanded_url'] = \
            bigTweet["quoted_status"]["entities"]["urls"][0]['expanded_url']
        except IndexError:
            return None
    return miniTweet

def gatherCopy():
    saveFolder = SORTEDPATH+"Sorted_of_interest/"
    foldersChecked = 0
    filesChecked = 0
    for folder in os.listdir(SORTEDPATH):
        if folder != "Sorted_of_interest":
            for innerFolder in os.listdir(SORTEDPATH+folder+"/"):
                for textFile in os.listdir(SORTEDPATH+folder+"/"+innerFolder+"/"):
                    filesChecked += 1
                    filePathAndName = SORTEDPATH+folder+"/"+innerFolder+"/"+textFile
                    fileSize = int(os.path.getsize(filePathAndName))
                    fileFound = True
                    if fileSize in range(0, 9999):
                        fileFound = False
                    if fileSize in range(10000, 20000):
                        saveLocation = open(saveFolder + "ten_twenty/" + textFile, 'a+')
                    elif fileSize in range(50000, 70000):
                        saveLocation = open(saveFolder + "fifty_sixty/" + textFile, 'a+')
                    elif fileSize in range(100000, 300000):
                        saveLocation = open(saveFolder + "hundred_hundredtwenty/" + textFile, 'a+')
                    elif fileSize in range(500000, 100000000):
                        saveLocation = open(saveFolder + "huge/" + textFile, 'a+')
                    else:
                        fileFound = False
                    if fileFound:
                        origFile = open(filePathAndName, 'r')
                        for line in origFile:
                            saveLocation.write(line)
                        saveLocation.close()
    print(filesChecked)