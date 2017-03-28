#This is the main file of the projekt and it is from here that you are setting all variables from an UI
import tweetsRunner
import bitlyRunner
import UpdateClicks

timeout = input("for how long would you like to collect tweets in seconds? ", )

runBitly = raw_input("would you like to extract bitly info to? (y/n)")

saveClicks = raw_input("would you like to save clicks to excelfile? (y/n)")
if saveClicks == "y":
    sleeplenght=int(raw_input("How often would you like to update clicks, answer in seconds "))
    turns = int(raw_input("How many times would you like to save?"))

tweetsRunner.collectTweets(timeout)

if runBitly == "y":
    bitlyRunner.run()


if saveClicks == "y":
    UpdateClicks.main(turns, sleeplenght)

print timeout