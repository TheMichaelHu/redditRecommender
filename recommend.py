# ---------------
# recommend.py
#
# Offers subreddit recommendations based on a given subreddit
# ---------------

# Checklist of things to implement:
# pull 100 unique users from comments						DONE
# pull 100 subreddits from comments from each user 			DONE
# create similarity function								DONE
# write similarity to database 								DONE
# sort similarity and output recommendation					DONE

import requests
import json
import urllib2
import psycopg2
import urlparse

USR_AG = {'User-Agent' : 'Arbitrary User Agent Name'}
NUM_USERS = 100
NUM_SUBREDDITS = 100
SUBREDDITS = 

def main():
	recommend('gameofthrones')

# Takes subreddit, gives recommendation
def recommend(subreddit):
	# just testin' some stuff...
	print cosine_similiarity(subreddit,'fffffffuuuuuuuuuuuu')

# Gets JSON for page after the given one
def get_next_page(url, after):
	if after is None:
		return None
	r = requests.get(url+'?after='+after, headers = USR_AG)
	return r.json()

# Get up to n unique users from given JSON.
def get_users(subreddit, num_users):
	r = requests.get('http://www.reddit.com/r/'+subreddit+'/comments/.json', headers = USR_AG)
	data = r.json()
	users = []

	index = 0
	while(len(users) < num_users):
		if(len(data['data']['children']) > index):
			user = data['data']['children'][index]['data']['author']
			if user not in users:
				users.append(user)
			index += 1
		else:
			data = get_next_page('http://www.reddit.com/r/'+subreddit+'/comments/.json', data['data']['after'])
			index = 0
			if data is None:
				break

	return users

# Get up to latest n comments from given user
def get_subreddits_for_user(user, num_subreddits):
	r = requests.get('http://www.reddit.com/user/'+user+'/comments/.json', headers = USR_AG)
	data = r.json()
	subreddits = []

	index = 0
	while(len(subreddits) < num_subreddits):
		if(len(data['data']['children']) > index):
			subreddits.append(data['data']['children'][index]['data']['subreddit'])
			index += 1
		else:
			data = get_next_page('http://www.reddit.com/user/'+user+'/comments/.json', data['data']['after'])
			index = 0
			if data is None:
				break

	return subreddits

# queries database to produce vector (order arbitrary but preserved in same python ver.)
def get_subreddit_vector():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse("postgres://tzxzlthahxikmb:4BNoR1mJxoFquJtf0X322KTLO8@ec2-54-83-51-0.compute-1.amazonaws.com:5432/dbknaoq86ntmdo")

	conn = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
	)

	cur = conn.cursor()

	cur.execute("SELECT COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name = 'ratings';")

	results = cur.fetchall()
	
	subreddits = {}
	for subreddit in results:
		subreddits[subreddit[0]] = 0
	return subreddits

# Get subreddits recent commenters have also been to
def get_subreddits(subreddit):
	subreddits = get_subreddit_vector()
	users = get_users(subreddit, NUM_USERS)

	for user in users:
		user_subreddits = get_subreddits_for_user(user, NUM_SUBREDDITS)
		for subreddit in user_subreddits:
			if subreddit in subreddits:
				subreddits[subreddit] += 1

	return subreddits.values()

def dot_product(vector1, vector2):
	dot_product = 0
	for i in range(len(vector1)):
		dot_product += vector1[i] * vector2[i]
	return dot_product

def norm(vector):
	sum_of_squares = 0
	for element in vector:
		sum_of_squares += element**2
	return sum_of_squares**.5

# Return the cosine similarity between two subreddits
def cosine_similiarity(subreddit1, subreddit2):
	vector1 = get_subreddits(subreddit1)
	vector2 = get_subreddits(subreddit2)
	return dot_product(vector1,vector2)/(norm(vector1)*norm(vector2))

# Write the similarity of two subreddits to the database
def write_subreddit_similarity(subreddit1, subreddit2):
	#assuming the similarity will be the same for (subreddit1,subreddit2) and (subreddit2,subreddit1), we insert twice 
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse("postgres://tzxzlthahxikmb:4BNoR1mJxoFquJtf0X322KTLO8@ec2-54-83-51-0.compute-1.amazonaws.com:5432/dbknaoq86ntmdo")

	conn = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
	)

	cur = conn.cursor()

	value = cosine_similiarity(subreddit1, subreddit2)
	SQL = "INSERT INTO ratings(%(reddit1)s, %(reddit2)s) VALUES (%(val)s);"
	data1 = ({'reddit1': subreddit1, 'reddit2':subreddit2, 'val': value})
	data2 = ({'reddit1': subreddit2, 'reddit2':subreddit1, 'val': value})

	cur.execute(SQL, data1)
	cur.execute(SQL, data2)
	cur.commit()

	return None

# get subreddit similarity for these two subreddits
def read_subreddit_similarity(subreddit1, subreddit2):
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse("postgres://tzxzlthahxikmb:4BNoR1mJxoFquJtf0X322KTLO8@ec2-54-83-51-0.compute-1.amazonaws.com:5432/dbknaoq86ntmdo")

	conn = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
	)

	cur = conn.cursor()

	SQL = "SELECT %(reddit1)s FROM ratings WHERE subreddit = %(reddit2)s;"
	data = ({'reddit1': subreddit1, 'reddit2':subreddit2})
	print(cur.mogrify(SQL, data))
	cur.execute(SQL, data)
	print cur.fetchall()
	
	return None

def get_subreddit_recommendation(subreddit, num_of_results):
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse("postgres://tzxzlthahxikmb:4BNoR1mJxoFquJtf0X322KTLO8@ec2-54-83-51-0.compute-1.amazonaws.com:5432/dbknaoq86ntmdo")

	conn = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
	)
	
	cur = conn.cursor()

	# this is broken down this way because postgresql ORDER BY is dumb and can't handle placeholder processing
	SQL = "SELECT reddit FROM ratings ORDER BY %s DESC LIMIT %%(num)s;" % subreddit
	data = ({"num":num_of_results})
		  
	cur.execute(SQL, data)
	print cur.fetchall()

main()