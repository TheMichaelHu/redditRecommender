# modify the db

import os
import psycopg2
import urlparse
import sys


urlparse.uses_netloc.append("postgres")

# cur.execute("CREATE TABLE test(Id INTEGER PRIMARY KEY, testCol VARCHAR(20))")
# cur.execute("INSERT INTO test(Id, testCol) VALUES (%(int)s, %(var)s);", {'int': 1, 'var':"testValue"})
# cur.execute("INSERT INTO test(Id, testCol) VALUES (%(int)s, %(var)s);", {'int': 2, 'var':"testValue2"})
# cur.execute("SELECT * FROM test WHERE testCol = %s;", ("testValue", ))
# cur.execute("SELECT COUNT(*) FROM test;")
# cur.execute("select * from INFORMATION_SCHEMA.COLUMNS where table_name = %(var)s;", {'var':"ratings"})
# cur.execute("INSERT INTO ratings(Id, reddit, askreddit, gadgets) VALUES (%(vara)s, %(varb)s, %(varc)s, %(vard)s);", {'vara': 2, 'varb':"relationships", 'varc':5, 'vard':5})

def get(cur):
	subreddit = raw_input("Which subreddit?\n")

	SQL = "SELECT * FROM ratings WHERE reddit = %s;"
	data = (subreddit, )
	print cur.mogrify(SQL, data)
	cur.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name = %(var)s;", {'var':"ratings"})

def main():
	
	url = urlparse.urlparse("postgres://tzxzlthahxikmb:4BNoR1mJxoFquJtf0X322KTLO8@ec2-54-83-51-0.compute-1.amazonaws.com:5432/dbknaoq86ntmdo")

	conn = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
	)

	while True:
		
		input = raw_input("Get/Post?\n")
		cur = conn.cursor()
		
		if (input in ["exit", "quit"]):
				print("\nExiting...")
				sys.exit()
				
		elif (input == "get"):
			
			get(cur)
		
		elif (input == "populate"):
		
			redditList = ({"reddit": "reddit"},
				{"reddit": "askreddit"},
				{"reddit": "funny"},
				{"reddit": "pics"},
				{"reddit": "todayilearned"},
				{"reddit": "announcements"},
				{"reddit": "worldnews"},
				{"reddit": "science"},
				{"reddit": "iama"},
				{"reddit": "videos"},
				{"reddit": "gaming"},
				{"reddit": "movies"},
				{"reddit": "music"},
				{"reddit": "aww"},
				{"reddit": "news"},
				{"reddit": "gifs"},
				{"reddit": "askscience"},
				{"reddit": "explainlikeimfive"},
				{"reddit": "earthporn"},
				{"reddit": "books"},
				{"reddit": "technology"},
				{"reddit": "television"},
				{"reddit": "bestof"},
				{"reddit": "wtf"},
				{"reddit": "lifeprotips"},
				{"reddit": "adviceanimals"},
				{"reddit": "sports"},
				{"reddit": "mildlyinteresting"},
				{"reddit": "diy"},
				{"reddit": "fitness"},
				{"reddit": "showerthoughts"},
				{"reddit": "space"},
				{"reddit": "tifu"},
				{"reddit": "jokes"},
				{"reddit": "food"},
				{"reddit": "internetisbeautiful"},
				{"reddit": "photoshopbattles"},
				{"reddit": "history"},
				{"reddit": "gadgets"},
				{"reddit": "getmotivated"},
				{"reddit": "nottheonion"},
				{"reddit": "dataisbeautiful"},
				{"reddit": "futurology"},
				{"reddit": "documentaries"},
				{"reddit": "listentothis"},
				{"reddit": "personalfinance"},
				{"reddit": "philosophy"},
				{"reddit": "nosleep"},
				{"reddit": "oldschoolcool"},
				{"reddit": "art"},
				{"reddit": "upliftingnews"},
				{"reddit": "creepy"},
				{"reddit": "writingprompts"},
				{"reddit": "twoxchromosomes"},
				{"reddit": "politics"},
				{"reddit": "atheism"},
				{"reddit": "woahdude"},
				{"reddit": "trees"},
				{"reddit": "leagueoflegends"},
				{"reddit": "games"},
				{"reddit": "programming"},
				{"reddit": "sex"},
				{"reddit": "fffffffuuuuuuuuuuuu"},
				{"reddit": "android"},
				{"reddit": "gameofthrones"},
				{"reddit": "reactiongifs"},
				{"reddit": "cringepics"},
				{"reddit": "malefashionadvice"},
				{"reddit": "interestingasfuck"},
				{"reddit": "frugal"},
				{"reddit": "youshouldknow"},
				{"reddit": "historyporn"},
				{"reddit": "pokemon"},
				{"reddit": "minecraft"},
				{"reddit": "pcmasterrace"},
				{"reddit": "blackpeopletwitter"},
				{"reddit": "askhistorians"},
				{"reddit": "lifehacks"},
				{"reddit": "comics"},
				{"reddit": "europe"},
				{"reddit": "unexpected"},
				{"reddit": "tattoos"},
				{"reddit": "justiceporn"},
				{"reddit": "nfl"},
				{"reddit": "foodporn"},
				{"reddit": "facepalm"},
				{"reddit": "soccer"},
				{"reddit": "wheredidthesodago"},
				{"reddit": "wallpapers"},
				{"reddit": "cringe"},
				{"reddit": "oddlysatisfying"},
				{"reddit": "truereddit"},
				{"reddit": "gentlemanboners"},
				{"reddit": "relationships"},
				{"reddit": "freebies"},
				{"reddit": "conspiracy"},
				{"reddit": "gamedeals"},
				{"reddit": "humor"},
				{"reddit": "offbeat"},
				{"reddit": "cooking"},
				{"reddit": "buildapc"})
				
			cur.executemany("INSERT INTO ratings(reddit) VALUES (%(reddit)s);", redditList)

		
		elif (input == "drop"):
			
			cur.execute("DROP TABLE ratings")
			cur.execute("""CREATE TABLE ratings(
reddit VARCHAR(64) PRIMARY KEY,
askreddit INTEGER,
funny INTEGER,
pics INTEGER,
todayilearned INTEGER,
announcements INTEGER,
worldnews INTEGER,
science INTEGER,
iama INTEGER,
videos INTEGER,
gaming INTEGER,
movies INTEGER,
music INTEGER,
aww INTEGER,
news INTEGER,
gifs INTEGER,
askscience INTEGER,
explainlikeimfive INTEGER,
earthporn INTEGER,
books INTEGER,
technology INTEGER,
television INTEGER,
bestof INTEGER,
wtf INTEGER,
lifeprotips INTEGER,
adviceanimals INTEGER,
sports INTEGER,
mildlyinteresting INTEGER,
diy INTEGER,
fitness INTEGER,
showerthoughts INTEGER,
space INTEGER,
tifu INTEGER,
jokes INTEGER,
food INTEGER,
internetisbeautiful INTEGER,
photoshopbattles INTEGER,
history INTEGER,
gadgets INTEGER,
getmotivated INTEGER,
nottheonion INTEGER,
dataisbeautiful INTEGER,
futurology INTEGER,
documentaries INTEGER,
listentothis INTEGER,
personalfinance INTEGER,
philosophy INTEGER,
nosleep INTEGER,
oldschoolcool INTEGER,
art INTEGER,
upliftingnews INTEGER,
creepy INTEGER,
writingprompts INTEGER,
twoxchromosomes INTEGER,
politics INTEGER,
atheism INTEGER,
woahdude INTEGER,
trees INTEGER,
leagueoflegends INTEGER,
games INTEGER,
programming INTEGER,
sex INTEGER,
fffffffuuuuuuuuuuuu INTEGER,
android INTEGER,
gameofthrones INTEGER,
reactiongifs INTEGER,
cringepics INTEGER,
malefashionadvice INTEGER,
interestingasfuck INTEGER,
frugal INTEGER,
youshouldknow INTEGER,
historyporn INTEGER,
pokemon INTEGER,
minecraft INTEGER,
pcmasterrace INTEGER,
blackpeopletwitter INTEGER,
askhistorians INTEGER,
lifehacks INTEGER,
comics INTEGER,
europe INTEGER,
unexpected INTEGER,
tattoos INTEGER,
justiceporn INTEGER,
nfl INTEGER,
foodporn INTEGER,
facepalm INTEGER,
soccer INTEGER,
wheredidthesodago INTEGER,
wallpapers INTEGER,
cringe INTEGER,
oddlysatisfying INTEGER,
truereddit INTEGER,
gentlemanboners INTEGER,
relationships INTEGER,
freebies INTEGER,
conspiracy INTEGER,
gamedeals INTEGER,
humor INTEGER,
offbeat INTEGER,
cooking INTEGER,
buildapc INTEGER,
changed DATE);""")
		
		conn.commit()
		print cur.fetchall()

# cur.execute("SELECT ratings.id, ratings.reddit, ratings.gadgets FROM ratings;")
	
main()