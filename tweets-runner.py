# ******** TWEETS-RUNNER *********'
# Main file of the project!
# Collects tweets in [runs] number of runs, as default set to 0 (meaning one run)
# Each run lasts for [timeout] seconds, as default set to 10 seconds
# Each run is saved in a file named with date and time.
# The file name is written to a file.

import bitlyfinder
import time
from time import strftime

if __name__ == '__main__':
	# path = 'C:/Utveckling/BitlyDev/bitlytweets-master/data/'
	# path = 'Z:/My Documents/BitlyDev/bitlytweets-master/data/'
	path = './data/'
	
	runs = 0
	timeout = 20
	
	# We will run the program until we have done X runs
	while(runs < 1):
		print('We are running! Lap ' + str(runs))
		runmeFile = open(path+'runme.txt', 'a+')
		
		# Tweets file named year-month-day_hour.txt
		time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
		path_and_filename = path+'tweets/'+time_for_filename+'.txt'

		# Get Tweets from Twitter! (Last argument is seconds to collect data)
		bitlyfinder.collectTweets(path_and_filename, timeout)
		runmeFile.write(path_and_filename + '\n')
		runmeFile.close()
		runs += 1
		
