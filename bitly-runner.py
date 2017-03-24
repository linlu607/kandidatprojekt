# Run the Bitly-extractor on the links in the tweets we collected
# We will start when we have one completed twitter file

import time
from time import strftime
import bitlydatahandler
import bitly_api
import time

# Set up API auth
login = 'o_1ej62d4rq7'
api_key = 'R_a1f7decfc0f64426987e083fc9cedfcd'
generic_token = 'e82b679532f66075a939553af072fc3a1b3d0888'
# Open connection
c = bitly_api.Connection(login=login, api_key=api_key, access_token=generic_token)
start_time = time.time()

if __name__ == '__main__':
	# path = 'C:/Utveckling/BitlyDev/bitlytweets-master/data/'
	# path = 'Z:/My Documents/BitlyDev/bitlytweets-master/data/'
	path = './data/'
	
	runs = 0
	lines = []
	haveread = []
	
	#bitlyBundle = []
	#bitlyextractor.expandShortUrl(bitlyBundle)
	
	# We will run the program until we have done a specified number of runs
	while(runs < 1):
		print('We are running! Lap ' + str(runs))
		# Open the file
		runFile = open(path+'runme.txt', 'r').read().split('\n')
		
		# Read paths to files to get bitlys from later
		for line in runFile:
			try:
				lines.append(line)
			except:
				continue
	
		for line in lines:
			if((line not in haveread) and (line != '')):
				# Read me
				time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
				# Create a file for the news sites
				news_file_path = path + time_for_filename + '_news.txt'
				# Create a file for the randomly selected Bitly links
				random_file_path = path + time_for_filename + '_random.txt'
				# Random tweets
				bitlydatahandler.handleTweets(tweetsPath=line, numToRead=100, outfile = random_file_path, newsOnly=0, c=c)
				# News tweets
				bitlydatahandler.handleTweets(tweetsPath=line, numToRead=100, outfile = news_file_path, newsOnly=1, c=c)
				haveread.append(line)
				runs += 1
	print("--- %s seconds ---" % (time.time() - start_time))
	print("DONE")
	
	
