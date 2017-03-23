# Handles the Bitly data

import json
from urlparse import urlsplit
import bitlyextractor
import random
from operator import itemgetter
import datetime

# Object to hold our json data
tweetsData = []
expandedData = []
PATTERNLIST = [
	'www.bbc.co.uk',
	'www.breitbart.com'
]

# Reads a number of random Tweets from a file
def handleTweets(tweetsPath, numToRead, outfile, newsOnly): 
	file = open(outfile, 'a+')
	longNewsURLs = open('./data/links/UnknownArticlesToBeExtracted.txt', 'a+')
	
	# Open the file
	tweetsFile = open(tweetsPath, 'r')

	# Read from the tweets file to tweetsData
	for line in tweetsFile:
		try:
			tweet = json.loads(line)
			tweetsData.append(tweet)
		except:
			continue

	bitlyDicts = []
	bitlyNewsDicts = []
	# Put URL info from the Tweets data in the tweets array
	for tw in tweetsData:
		# Save ID and bitly link in dict array
		dict = {'id':tw['id'], 'short_url':tw['entities']['urls'][0]['expanded_url'], 'long_url':'', 'bitly_global_hash':'', 'bitly_user_hash':'', 'refs':'', 'countries':'', 'global_clicks':'', 'user_clicks':''}
		bitlyDicts.append(dict)
		if('bit.ly/' not in dict['short_url']):
			bitlyNewsDicts.append(dict)

	# If the newsOnly flag is 1 we will pick specific news links (e.g. cnn.it), else we will pick bit.ly URLs
	if(newsOnly == 1):
		# Only news URLs
		samples = pickSamples(bitlyDicts = bitlyNewsDicts, numToRead = numToRead)
	else:
		# Both news URLs and Bitly URLs
		samples = pickSamples(bitlyDicts = bitlyDicts, numToRead = numToRead)

	uniqueBitlys = pickUnique(bitlySamples = samples)
	URLs = resolveBitlys(uniqueBitlys)
	
	shortURLs = []
	longURLs = []
	globalHashes = []
	userHashes = []
	
	# We split the tupe URLs into three arrays
	for url in URLs:
		shortURLs.append(url[0])
		longURLs.append(url[1])
		globalHashes.append(url[2])
		userHashes.append(url[3])
		r = urlsplit(url[1])
		for PATTERN in PATTERNLIST:
			if (PATTERN == r.netloc):
				if (patternIsUnique(url[1])):
					longNewsURLs.write(str(url[1])+ '\n')
	longNewsURLs.close()
	# For each of the Bitly links from our collected tweets
	tmp=0
	for sample in samples:
                tmp=tmp+1
		# If the bitlyURL is found (it should always be)
		if sample['short_url'] in shortURLs:
			i = shortURLs.index(sample['short_url'])
			sample['long_url'] = longURLs[i]
			sample['bitly_global_hash'] = globalHashes[i]
			sample['bitly_user_hash'] = userHashes[i]
			clickBlock = bitlyextractor.getURLClicks(sample['bitly_global_hash'])
			sample['countries'] = bitlyextractor.getLinkCountries(sample['short_url'])
			sample['refs'] = bitlyextractor.getRefs(sample['short_url'])
			print("number of bitlylinks extracted is: " , tmp)
			if clickBlock != None:
				for e in clickBlock:
					sample['user_clicks'] = e.get('user_clicks')
					sample['global_clicks'] = e.get('global_clicks')
			
			file.write(str(sample) + '\n')
			#print('Sample:' + str(sample))
		else:
			print(str(sample) + ' could not be resolved.')
	file.close()
	
def pickSamples(bitlyDicts, numToRead):
	# Samples bitly links (with name and ID)
	bitlySamples = []
		
	# Select numToRead tweets randomly
	if(numToRead < len(bitlyDicts)):
		bitlySamples = random.sample(bitlyDicts, numToRead)
	elif len(bitlyDicts) == 0:
		print('No bitlys to read!')
		return None;
	else:
		#print('We only have ' + str(len(bitlyDicts)) + ' to read!')
		bitlySamples = random.sample(bitlyDicts, len(bitlyDicts))
	return bitlySamples
	
def pickUnique(bitlySamples):
	bitlysArray = []
	for e in bitlySamples:
	# Only unique bitly links should be added
		if e['short_url'] not in bitlysArray:
			bitlysArray.append(e['short_url'])
	return bitlysArray
	
def resolveBitlys(bitlysArray):
	# The bitly bundle contains 15 Bitly URLs! (Cannot send more to Bitly)
	bitlyBundle = []
	start = 0
	end = 7
	max = len(bitlysArray)
	response = [] # The resolved info from Bitly
	URLsAndHash = []
	
	# Build bundles of bitlys to resolve, max 15 at a time
	tmp=0
	while end <= max:
                tmp=tmp+1
		#print('We have more than or equal to 15 bitlys!')
		bitlyBundle = itemgetter(slice(start, end))(bitlysArray)
		try:
                        print("we are curently slicing part number, (every part has 15 links) : ", tmp)
			response = bitlyextractor.expandShortUrl(bitlyBundle) # TODO Error handling on the response
			for e in response:
				shortURL = checkShortURL(e)
				longURL = checkLongURL(e)
				globalHash = checkGlobalHash(e)
				userHash = checkUserHash(e)
				URLsAndHash.append((shortURL, longURL, globalHash, userHash))
		except:
			print('Problems with the response from Bitly.')
			return URLsAndHash
		start += 7
		end +=  7

	if(max < end) and (start <= max):
		#print('We have less than 15 bitlys!')
		# Get items start to max (there are less than 15 items to handle)
		bitlyBundle = itemgetter(slice(start, max))(bitlysArray)

		# Ask the bitly extractor for the full URLs
		try:
			response = bitlyextractor.expandShortUrl(bitlyBundle)
			for e in response:
				shortURL = checkShortURL(e)
				longURL = checkLongURL(e)
				globalHash = checkGlobalHash(e)
				userHash = checkUserHash(e)
				URLsAndHash.append((shortURL, longURL, globalHash, userHash))
		except:
			print('Problems with the response from Bitly.')
			return URLsAndHash
			
	return URLsAndHash

def checkUserHash(e):
	hash = ''
	try:
		hash = (e.get('user_hash'))
		return hash
	except AttributeError:
		return hash
		
def checkGlobalHash(e):
	hash = ''
	try:
		hash = (e.get('global_hash'))
		return hash
	except AttributeError:
		return hash
	
def checkLongURL(e):
	longURL = ''
	try:
		longURL = (e.get('long_url')).encode('utf-8')
		return longURL
	except AttributeError:
		return longURL
		
def checkShortURL(e):
	shortURL = ''
	try:
		shortURL = e.get('short_url')
		return shortURL
	except AttributeError:
		return shortURL

def patternIsUnique(s):
    with open('./data/links/UnknownArticlesToBeExtracted.txt') as f:
	for line in f:
	    if(s + '\n' == line):
		f.close()
		return False
    f.close()
    return True

# This function is not currently used, but if we want some official news channels from Twitter, this is an incomplete list		
def getNewsNames():
	newsSources = []
	newsSources.append('CNN') # CNN
	newsSources.append('CNNMoney') #CNNMoney
	newsSources.append('cnnbrk')
	newsSources.append('BBC')
	newsSources.append('BBCBreaking')
	newsSources.append('Reuters')
	newsSources.append('nytimes')
	newsSources.append('TIME')
	newsSources.append('washingtonpost')
	newsSources.append('WSJ')
	newsSources.append('FoxNews')
	newsSources.append('ABC')
	newsSources.append('NPR')
	newsSources.append('guardian')
	newsSources.append('CBSNews')
	newsSources.append('AFP')
	newsSources.append('cnni')
	newsSources.append('NBCNews')
	newsSources.append('latimes')
	newsSources.append('NewYorker')
	newsSources.append('HuffingtonPost')
	return newsSources;
