# ---------------
# recommend.py
#
# Offers subreddit recommendations based on a given subreddit or user
# ---------------

# Checklist of things to implement:
# pull 100 unique users from comments									DONE
# pull 100 subreddits from comments from each user 						DONE
# create similarity function											DONE
# write "points" to database											DONE
# run similarity on vector, output vector with similarity				DONE		
# Given a user, get subreddits, run above method on each subreddits 	DONE
# Add basic user interface												DONE

import requests
import json
import urllib2
import psycopg2
import urlparse

USR_AG = {'User-Agent' : 'Arbitrary User Agent Name'}
NUM_USERS = 100
NUM_SUBREDDITS = 100
NUM_RESULTS = 3

# ---- Similarity Function ----
def similarity_function(vector1, vector2):
	return cosine_similiarity(vector1,vector2);
# -----------------------------

# ---- Similarity Function Options ----

# Return the cosine similarity between two subreddits
def cosine_similiarity(vector1, vector2):
	return dot_product(vector1,vector2)/(norm(vector1)*norm(vector2))

def euclidean_distance(vector1, vector2):
	acc = 0
	for i in range(len(vector1)):
		acc += (vector1[i]-vector2[i])**2
	return acc**.5

def normalized_squared_eclidean_distance(vector1, vector2):
	norm_vector1 = []
	len_vector1 = norm(vector1)
	norm_vector2 = []
	len_vector2 = norm(vector2)
	if(len_vector1 == 0 or len_vector2 == 0):
		return 0
	for element in vector1:
		norm_vector1.append(element/len_vector1) 
	for element in vector2:
		norm_vector2.append(element/len_vector2) 
	return euclidean_distance(norm_vector1,norm_vector2)

def pearson_correlation(vector1, vector2):
    values = range(len(vector1))
    
    # Summation over all attributes for both vectors
    sum_vector1 = sum([vector1[i] for i in values]) 
    sum_vector2 = sum([vector2[i] for i in values])

    # Sum the squares
    square_sum1 = sum([vector1[i]**2 for i in values])
    square_sum2 = sum([vector2[i]**2 for i in values])

    # Add up the products
    product = sum([vector1[i]*vector2[i] for i in values])

    #Calculate Pearson Correlation score
    numerator = product - (sum_vector1*sum_vector2/len(vector1))
    denominator = ((square_sum1 - sum_vector1**2/len(vector1)) * (square_sum2 - 
    	sum_vector2**2/len(vector1))) ** 0.5
        
    # Can"t have division by 0
    if denominator == 0:
        return 0

    return numerator/denominator

# -------------------------------------

def main():
	while(1):
		print "Would you like recommendations for a (u)ser or (s)ubreddit?"
		response = raw_input("> ")
		if(response is not '' and response[0] == 'u'):
			user = raw_input("Reddit User: ")
			recommend_for_user(user, NUM_RESULTS)
		else:
			subreddit = raw_input("Subreddit: ")
			if(subreddit in get_subreddit_vector().keys()):
				recommend(subreddit, NUM_RESULTS)
			else:
				print "Sorry, that subreddit is not supported."
		#recommend('gameofthrones',NUM_RESULTS)
		#recommend_for_user('GovSchwarzenegger', NUM_RESULTS)

#takes user, gives subreddit recommendation (doesn't exclude ones they already visit)
def recommend_for_user(user, num):
	subreddit_weights = get_subreddit_vector()
	subreddit_counts = {}
	#count subreddits
	for subreddit in get_subreddits_for_user(user, NUM_SUBREDDITS):
		if subreddit in subreddit_weights:
			if subreddit in subreddit_counts.keys():
				subreddit_counts[subreddit] += 1
			else:
				subreddit_counts[subreddit] = 1
	# Sum up similarity values of top 5 recommended subreddits for each subreddit
	for subreddit in subreddit_counts:
		# Get top 5 recommended subreddits for each subreddit
		similarities = similarity_vector(subreddit)
		top_five = []
		for key in sorted(similarities, key=similarities.get, reverse=True):
			if len(top_five) < 5:
				top_five.append(key)
			else:
				break
		# Add count * the similarity score
		for key in top_five:
			subreddit_weights[key] += similarities[key] * subreddit_counts[subreddit]
	# Order dictionary and the top number specified
	subreddits = get_recommended_subreddits_ordered(subreddit_weights)
	print "Top",str(num),"recommended subreddits for",user+":"
	for i in range(0,num):
		print str(i+1)+":",subreddits[i]

# Takes subreddit, gives recommendation
def recommend(subreddit, num):
	similarities = similarity_vector(subreddit)
	subreddits = get_recommended_subreddits_ordered(similarities)
	print "Top",str(num),"recommended subreddits for",subreddit+":"
	for i in range(1,num+1):
		print str(i)+":",subreddits[i]

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
			if data['data']['after'] is None:
				break
			else:
				data = get_next_page('http://www.reddit.com/r/'+subreddit+'/comments/.json', data['data']['after'])
				index = 0

	return users

# Get up to latest n comments from given user
def get_subreddits_for_user(user, num_subreddits):
	r = requests.get('http://www.reddit.com/user/'+user+'/comments/.json', headers = USR_AG)
	data = r.json()
	subreddits = []

	index = 0
	while(len(subreddits) < num_subreddits):
		if not existing_page(user, data):
		   break;
		elif (len(data['data']['children']) > index):
			subreddits.append(data['data']['children'][index]['data']['subreddit'].lower())
			index += 1
		elif data['data']['after'] is None:
			break
		else:
			data = get_next_page('http://www.reddit.com/user/'+user+'/comments/.json', data['data']['after'])
			index = 0

	return subreddits

# Does this page exist?
def existing_page(user, data):
	if 'error' in data:
		print user + " DOES NOT EXIST"
		return False
	return True
	
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
			if subreddit in subreddits.keys():
				subreddits[subreddit] += 1

	return subreddits

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

# Write the points of a subreddit to the database
def write_subreddit_points(subreddit):
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

	# this is broken down this way because postgresql UPDATE is dumb and can't handle placeholder processing
	query1 = "UPDATE ratings SET %s " % subreddit
	dict = get_subreddits(subreddit)
	for key, value in dict.iteritems():

		SQL = query1 + "= %(val)s WHERE reddit=%(key)s;"
		data = ({'val': str(value), 'key': key})
		cur.execute(SQL, data)
		conn.commit()

	return None

# Get all subreddits and subreddit points as a list of tuples
def read_all_points():
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

	cur.execute("SELECT * FROM ratings;")

	return cur.fetchall()
	
# Get all subreddits and subreddit points for this subreddit as a dictionary
def read_subreddit_points(subreddit):
	
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

	query1 = "SELECT reddit, %s" % subreddit
	SQL = query1 + " FROM ratings;"
	data = ({'reddit1': subreddit})
	cur.execute(SQL, data)
	result = {}
	
	for item in cur.fetchall():
		result[item[0]] = item[1]

	return result

# Get all subreddits and subreddit points for this subreddit as a dictionary
def read_subreddit_points(subreddit, total_list):

	subreddit_index = get_index(subreddit, total_list)

	results = {}
	for item in total_list:
		item_to_list = list(item)
		results[item_to_list[0]] = item_to_list[subreddit_index]
	
	return results

# get the index of this subreddit)
def get_index(subreddit, total_list):

	for item in total_list:
		if item[0] == subreddit:
			return item[-1]
			break;
	return subreddit
	
# Get an ordered DESC list of subreddits by points for this subreddit
def get_subreddit_points(subreddit, num_of_results):
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

# run similarity on vector, output vector with similarity
def similarity_vector(subreddit):
	total = read_all_points()
	
	vector1 = read_subreddit_points(subreddit, total)
	results = {}
	for subreddit_name, subreddit_points in vector1.iteritems():
		vector2 = read_subreddit_points(subreddit_name, total)
		
		subreddit_similarity = similarity_function(vector1.values(), vector2.values())
		results[subreddit_name] = subreddit_similarity
		
	return results

# returns ordered list of recommended subreddits starting with the most recommended one
def get_recommended_subreddits_ordered(similarities):
	subreddits = []
	for subreddit in sorted(similarities, key=similarities.get, reverse=True):
		subreddits.append(subreddit+": "+str(similarities[subreddit]))
	return subreddits

main()