#This is the main file of the projekt and it is from here that you are setting all variables from an UI
import tweetsRunner
import bitlyRunner
import UpdateClicks
import htmlToText
import naiveBayesPipeline
from multiprocessing import Process, active_children, Pool, Lock

def b(tweetsPath):
    res = bitlyRunner.run(tweetsPath)
    return res
if (__name__ == '__main__'):
    timeout = input("In seconds, for how long would you like to collect tweets? ", )

    runs = input("For how many runs would you like to collect tweets? ", )

    runBitly = raw_input("Would you like to extract bitly info too? (y/n)")

    runHtmlExtractor = raw_input("Would you like to extract articles from identified links? (y/n)")

    runNaiveBayes = raw_input("Would you like to classify extracted articles? (y/n)")

    saveClicks = raw_input("Would you like to save clicks to excelfile? (y/n)")
    if saveClicks == "y":
        sleeplenght=int(raw_input("How often would you like to update clicks, answer in seconds "))
        turns = int(raw_input("How many times would you like to save?"))

    open('./data/seenShortURLs.txt', 'w').close()
    open('./data/expanded.txt', 'w').close()
    open('./data/runme.txt', 'w').close()
    open('./data/links/UnknownArticlesToBeExtracted.txt', 'w').close()
    open('./data/news/classifications.txt', 'w').close()
    #Erase contents in some .txt

    pool = Pool(2)

    i = 0
    while i < runs:
        tweetsPath = tweetsRunner.collectTweets(timeout)
        i = i + 1
        if runBitly == "y":
            print "Runing bitlys"
            #TODO: start on async on a new thread
            res = pool.apply_async(b, (tweetsPath,))
            #Process(target=b, args=(tweetsPath,)).start()
            #print "Runing bitlys in process %d" % p.pid

    pool.close()
    pool.join()

    if runHtmlExtractor == "y":
        print "Runing html"
        htmlToText.run()
        
    if saveClicks == "y":
        #TODO: Doesn't work right. FIX!
        #Actually, splitt it into two classes, one for updating clicks and one for writing to xml.
        print "Runing updates"
        UpdateClicks.main(turns, sleeplenght)

    if runNaiveBayes == "y":
        print "Runing Bayes"
        naiveBayesPipeline.run()

    print "FINISHED"
    done = raw_input("You can close the program now by pressing any key")
