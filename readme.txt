The current version of our program works as follows

******* Main ********
It is from this file the program runs from, from here you can chose how long you want to collect tweet
and what sort of results you want to save

******* tweets-runner ********
This file collects the tweets, with the help of some help files.

******* bitly-runner *********
Reads file names from a file (which tweets-runner stores them in). 
The file names are the twitter files to process. For each such file,
 this program runs a set of X (in this case 100) randomly selected tweets
 and as many news tweets. The program asks bitly for long URL, clicks per
 country and clicks per referrer. We also save identifiers (bitly user, bitly
 link, and tweet ID) global clicks and clicks made by user.

******* helper files *********
bitlyextractor, bitlyfinder and bitlydatahandler are helper filers. 
I use a directory "data" for the data and a sub-directory "tweets" in "data" for the tweets.

Files that also exist in the project is:

htmlToText, extract the news article from an url

naiveBayesTrainer, trains a text classifier to classify text as fake or real

naiveBayesPipeline, classifies the text as fake or real.

*****How to run the program *****

to run the program you will need alot of extra packet from python, to do this you can use pip install,
the packet that you need to install is:

xlwt (is used to save to excel)
tweepy (twitter API)
bitly_api (bitlys api)
For the naive bayes classifier you need several packages
pandas (use pipinstall)
****************************************
This two is a little bit tricky to install on windows due to you need a
special winddows version, you can find the packeges on this page: http://www.lfd.uci.edu/~gohlke/pythonlibs/
Scipy
scikit-learn
*********************************************