#This is the main file of the projekt and it is from here that you are setting all variables from an UI
import tweetsRunner
import bitlyRunner
import UpdateClicks
import htmlToText
import bitlydatahandler
import naiveBayesPipeline
import Queue as NormalQueue
import time
from multiprocessing import Process, Pool, Manager

def b(tweetsPath, lock):
    lock.acquire()
    res = bitlyRunner.run(tweetsPath)
    lock.release()
    print "b has been released"
    return res

def u(q, sleep, turns, lock):
    updatingQueue = NormalQueue.PriorityQueue()
    timeOfUpdateQueue = NormalQueue.PriorityQueue()
    timeOfNextUpdate = 0
    run = True
    print "Starting update process"
    while run:
        # timeOfNextUpdate never becomes not null.
        # print "The time of the next update is: %.2f" % timeOfNextUpdate
        if(timeOfNextUpdate != 0):
            print "The next update is in: %.2f" % (timeOfNextUpdate - time.time())
            if time.time() >= timeOfNextUpdate:
                path = updatingQueue.get()[1]
                #print "The next news-file is: " + str(path)
                startGetting = time.time()
                lock.acquire()
                startBitly = time.time()
                # Make faster/getmore threads
                res = bitlydatahandler.updateClicks(path)
                print "bitlys updated in %.2f seconds" % (time.time() - startBitly)
                lock.release()
                time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
                #print "u has been released, %.2f seconds after requesting lock" % (time.time() - startGetting)
                updatePath = path[:(len(path)-4)] + "_(" + time_for_filename + ").txt"
                #print updatePath
                # put the IO on a thread
                # Actually: The write of the updated data on bitlys collected over 10 s. is less than 0.01 s.
                # not much speed to gain here.
                f = open(updatePath, "w")
                f.write(str(res))
                f.close()
                print "Done with all IO after %.2f seconds, for now." % (time.time() - startGetting)
                #print "Is the time queue empty: " , timeOfUpdateQueue.empty()
                #print "Is the updating queue empty: " , updatingQueue.empty()
                if timeOfUpdateQueue.empty() is False:
                    timeOfNextUpdate = timeOfUpdateQueue.get()
                else:
                    run = False
                    print "Done updating"
                    return "DONE"
            else:
                #print "Short sleep"
                time.sleep(1)
        else:
            #print "Long sleep"
            time.sleep(2)
        #print "Is the queue empty: " , q.empty()
        if q.empty() is False:
            newsPath = q.get()
            print "Path to the original news-file:", newsPath
            print "Turns to save:", turns
            t = time.time()
            i = 1
            while i <= turns:
                updatingQueue.put(((t +(sleep * i)),newsPath))
                timeOfUpdateQueue.put(t +(sleep * i))
                if timeOfNextUpdate == 0:
                    timeOfNextUpdate = timeOfUpdateQueue.get()
                    print "First update time added. It is in %.2f seconds." % (timeOfNextUpdate - time.time())
                i = i + 1
    return "DONE"
    
if (__name__ == '__main__'):

    manager = Manager()
    q = manager.Queue()
    lock = manager.Lock()
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
    if sleeplength > 0:
        p = Process(target=u, args=(q,sleeplength,turns,lock,))
        p.start()
        print p.pid
    
    pool = Pool(3)
##    if sleeplength > 0:
##        pool.apply_async(u, (q,sleeplength,turns,lock,))
    i = 0
    while i < runs:
        tweetsPath = tweetsRunner.collectTweets(timeout)
        i = i + 1
        if runBitly == "y":
            print "Runing bitlys"
            pool.apply_async(b, (tweetsPath,lock,), callback=q.put)
    pool.close()
    pool.join()
    time.sleep(sleeplength)
    if sleeplength > 0:
        p.join()
        print "P should have joined now"
        print p.is_alive()
        if p.is_alive():
            p.terminate()

    if runHtmlExtractor == "y":
        print "Runing html"
        htmlToText.run()
        
    if saveClicks == "y":
        #TODO: Doesn't work right. FIX!
        #Actually, splitt it into two classes, one for updating clicks and one for writing to xml.
        print "Runing updates"
        #UpdateClicks.main(turns, sleeplength)

    if runNaiveBayes == "y":
        print "Runing Bayes"
        naiveBayesPipeline.run()

    print "FINISHED"
    done = raw_input("You can close the program now by pressing any key")
