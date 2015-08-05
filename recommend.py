# ---------------
# recommend.py
#
# Offers subreddit recommendations based on a given subreddit
# ---------------

# Checklist of things to implement:
# pull 100 unique users from comments						DONE
# pull 100 subreddits from comments from each user 			DONE
# create similarity function
# write similarity to database 
# sort similarity and output recommendation

import requests
import json
import urllib2

USR_AG = {'User-Agent' : 'Arbitrary User Agent Name'}
NUM_USERS = 100
NUM_SUBREDDITS = 100

def main():
	recommend('gameofthrones')

# Takes subreddit, gives recommendation
def recommend(subreddit):
	print getSubreddits(subreddit)

# Gets JSON for page after the given one
def getNextPage(url, after):
	if after is None:
		return None
	r = requests.get(url+'?after='+after, headers = USR_AG)
	return r.json()

# Get up to n unique users from given JSON.
def getUsers(subreddit, numUsers):
	r = requests.get('http://www.reddit.com/r/'+subreddit+'/comments/.json', headers = USR_AG)
	data = r.json()
	users = []

	index = 0
	while(len(users) < numUsers):
		if(len(data['data']['children']) > index):
			user = data['data']['children'][index]['data']['author']
			if user not in users:
				users.append(user)
			index += 1
		else:
			data = getNextPage('http://www.reddit.com/r/'+subreddit+'/comments/.json', data['data']['after'])
			index = 0
			if data is None:
				break

	return users

# Get up to latest n comments from given user
def getSubredditsForUser(user, numSubreddits):
	r = requests.get('http://www.reddit.com/user/'+user+'/comments/.json', headers = USR_AG)
	data = r.json()
	subreddits = []

	index = 0
	while(len(subreddits) < numSubreddits):
		if(len(data['data']['children']) > index):
			subreddits.append(data['data']['children'][index]['data']['subreddit'])
			index += 1
		else:
			data = getNextPage('http://www.reddit.com/user/'+user+'/comments/.json', data['data']['after'])
			index = 0
			if data is None:
				break

	return subreddits

# Get subreddits recent commenters have also been to
def getSubreddits(subreddit):
	subreddits = {}
	users = getUsers(subreddit, NUM_USERS)

	for user in users:
		user_subreddits = getSubredditsForUser(user, NUM_SUBREDDITS)
		for subreddit in user_subreddits:
			if subreddit in subreddits:
				subreddits[subreddit] += 1
			else:
				subreddits[subreddit] = 1 

	return subreddits

main()