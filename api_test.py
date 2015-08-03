# Grabs latest 24 comments (all the comments on the first page) from a subreddit

import requests
import json
import urllib2

usr_ag = {'User-Agent' : 'Your Mom'}

subreddit = 'gameofthrones'

r = requests.get('http://www.reddit.com/r/'+subreddit+'/comments/.json', headers = usr_ag)
data = r.json()

for child in data['data']['children']:
    print child['data']['author']+':\n'+child['data']['body']
    print