The current version of our program works as follows

******* tweets-runner ********
The main file of the program. Could be replaced with some sort of shell script instead.
Collects tweets during [runs] runs which are [timeout] seconds long. Each run is saved in a file named with date and time. The file name is written to a file.

******* bitly-runner *********
Reads file names from a file (which tweets-runner stores them in). The file names are the twitter files to process. For each such file, this program runs a set of X (in this case 100) randomly selected tweets and as many news tweets. The program asks bitly for long URL, clicks per country and clicks per referrer. We also save identifiers (bitly user, bitly link, and tweet ID) global clicks and clicks made by user.

******* helper files *********
bitlyextractor, bitlyfinder and bitlydatahandler are helper filers. I use a directory "data" for the data and a sub-directory "tweets" in "data" for the tweets.