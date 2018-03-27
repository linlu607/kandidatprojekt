import json
import anytree
from anytree import Node

def create(tweetsFile):
    posts = []
    for line in tweetsFile:
        posts.append(json.loads(line))

    for post in posts:
        if 'quoted_status' in post:
            # this is a quote
            print()
        elif 'retweeted status' in post:
            # this is a retweet
            print()
        else:
            # this is original content
            print()



