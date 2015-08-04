# ---------------
# recommend.py
#
# Offers subreddit recommendations based on a given subreddit
# ---------------

# Checklist of things to implement:
# pull 100 users from comments					DONE
# pull 100 comments from each user
# pull subreddits from comments
# create similarity function
# write similarity to database 
# sort similarity and output recommendation

import requests
import json
import urllib2

USR_AG = {'User-Agent' : 'Arbitrary User Agent Name'}

def main():
	recommend('gameofthrones')

def recommend(subreddit):
	r = requests.get('http://www.reddit.com/r/'+subreddit+'/comments/.json', headers = USR_AG)
	data = r.json()

	users = getUsers(data, 100)
	for user in users:
		print user

def getNextPage(data):
	subreddit = data['data']['children'][0]['data']['subreddit']
	after = data['data']['after']
	r = requests.get('http://www.reddit.com/r/'+subreddit+'/comments/.json?after='+after, headers = USR_AG)
	return r.json()

def getUsers(data, numUsers):
	pageData = data
	users = []

	index = 0
	while(len(users) < numUsers):
		if(len(pageData['data']['children']) > index):
			user = pageData['data']['children'][index]['data']['author']
			if user not in users:
				users.append(user)
			index += 1
		else:
			pageData = getNextPage(pageData)
			index = 0

	return users

main()