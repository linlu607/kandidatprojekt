# -*- coding: cp1252 -*-
# Communicates with bitly.com to expand short URL's

import bitly_api

# Set up API auth
##login = 'o_1ej62d4rq7'
##api_key = 'R_a1f7decfc0f64426987e083fc9cedfcd'
##generic_token = 'e82b679532f66075a939553af072fc3a1b3d0888'

# Open connection
##c = bitly_api.Connection(login=login, api_key=api_key, access_token=generic_token)

# Send request to bitly API and write response to file.
# shortUrls is an array of up to 15 short URL's (bitly.com API max limit)
def expandShortUrl(shortUrls, c):
	# File to write to
	# path = 'C:/Utveckling/BitlyDev/bitlytweets-master/data/'
	# path = 'Z:/My Documents/BitlyDev/bitlytweets-master/data/'
	path = './data/'
	
	response = None
	try:
		o = open(path+'expanded.txt', 'a+')
		response = c.expand(shortUrl=shortUrls)
		print("länk extraherad")
		o.write((str(response).encode('utf-8')) + '\n')
		o.close()
	except: 
		pass
	return response;
	
def getRefs(link, c):
	refs = None
	try:
		refs = c.link_referrers_by_domain(link)
		print("refs-länk hittad")
	except: 
		print('Unable to retrieve refs')
	return refs;
	
def getLinkCountries(link, c):
	countries = None
	try:
		countries = c.link_countries(link)
		print("land hittat")
	except: 
		print('Unable to retrieve countries')
	return countries;
	
def getURLClicks(globalHash, c):
	URLclicks = None
	try:
		URLclicks = c.clicks(globalHash)
		print("länkar har vi hittat hur många gånger de klickas")
	except: 
		print('Unable to retrieve clicks')
	return URLclicks;

# Dummy main function, just for testing a bitly URL	
#if __name__ == '__main__':
#	shortUrls = []
#	shortUrls.append('http://bit.ly/28Zo8vQ')
#	expandShortUrl(shortUrls)
#	getURLClicks('28ZYUgL')
#	getLinkCountries('http://bit.ly/28Zo8vQ')
#	getRefs('http://bit.ly/28Zo8vQ')
