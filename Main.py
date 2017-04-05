#This is the main file of the projekt and it is from here that you are setting all variables from an UI
import tweetsRunner
import bitlyRunner
import UpdateClicks
import htmlToText
import bitlydatahandler
import naiveBayesPipeline
import Queue as NormalQueue
import time
from multiprocessing import Process, active_children, Pool, Queue

def b(tweetsPath):
    res = bitlyRunner.run(tweetsPath)
    return res

def u(q, sleep, turns):
    updatingQueue = Queue.priorityQueue()
    timeOfUpdateQueue = Queue.priorityQueue()
    timeOfNextUpdate = 0
    while True:
        if(timeOfNextUpdate != 0):
            if time.time() >= timeOfNextUpdate:
                path = updatingQueue.get()
                res = bitlydatahandler.updateClicks(path)
                with open(updatePath, "w") as f:
                    for sample in res:
                        f.write(sample + "\n")
                if timeOfUpdateQueue.empty() is False:
                    timeOfNextUpdate = timeOfUpdateQueue.get()
                else:
                    break
            else:
                time.sleep(10)
        if q.empty() is False:
            newsPath = q.get()
            t = time.time()
            i = 1
            while i <= turns:
                updatingQueue.put(((t +(sleep * i)),newsPath))
                timeOfUpdateQueue.put(t +(sleep * i))
                i = i + 1
                if timeOfNextUpdate == 0:
                    timeOfNextUpdate = t +(sleep * i)
    
if (__name__ == '__main__'):

    q = Queue()
    sleeplength = 0
    timeout = input("In seconds, for how long would you like to collect tweets? ", )

    runs = input("For how many runs would you like to collect tweets? ", )

    runBitly = raw_input("Would you like to extract bitly info too? (y/n)")

    runHtmlExtractor = raw_input("Would you like to extract articles from identified links? (y/n)")

    runNaiveBayes = raw_input("Would you like to classify extracted articles? (y/n)")

    saveClicks = raw_input("Would you like to save clicks to excelfile? (y/n)")
    if saveClicks == "y":
        sleeplength=int(raw_input("How often would you like to update clicks, answer in seconds "))
        turns = int(raw_input("How many times would you like to save?"))

    open('./data/seenShortURLs.txt', 'w').close()
    open('./data/expanded.txt', 'w').close()
    open('./data/runme.txt', 'w').close()
    open('./data/links/UnknownArticlesToBeExtracted.txt', 'w').close()
    open('./data/news/classifications.txt', 'w').close()
    #Erase contents in some .txt
    pool = Pool(2)
    if sleeplength > 0:
        p = Process(target=u, args=(q,sleeplength,turns,)).start()
    i = 0
    while i < runs:
        tweetsPath = tweetsRunner.collectTweets(timeout)
        i = i + 1
        if runBitly == "y":
            print "Runing bitlys"
            pool.apply_async(b, (tweetsPath,), callback=q.put)
            #q.put(res)
    pool.close()
    pool.join()
    if sleeplength > 0:
        p.join

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
