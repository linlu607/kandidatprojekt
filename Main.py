#This is the main file of the projekt and it is from here that you are setting all variables from an UI
import tweetsRunner
import bitlyRunner
import UpdateClicks
import htmlToText
import naiveBayesPipeline

timeout = input("In seconds, for how long would you like to collect tweets? ", )

runBitly = raw_input("Would you like to extract bitly info too? (y/n)")

runHtmlExtractor = raw_input("Would you like to extract articles from identified links? (y/n)")

runNaiveBayes = raw_input("Would you like to classify extracted articles? (y/n)")

saveClicks = raw_input("Would you like to save clicks to excelfile? (y/n)")
if saveClicks == "y":
    sleeplenght=int(raw_input("How often would you like to update clicks, answer in seconds "))
    turns = int(raw_input("How many times would you like to save?"))

tweetsRunner.collectTweets(timeout)

if runBitly == "y":
    print "Runing bitlys"
    bitlyRunner.run()

if runHtmlExtractor == "y":
    print "Runing html"
    htmlToText.run()

if runNaiveBayes == "y":
    print "Runing Bayes"
    naiveBayesPipeline.run()

if saveClicks == "y":
    print "Runing updates"
    UpdateClicks.main(turns, sleeplenght)

print timeout
