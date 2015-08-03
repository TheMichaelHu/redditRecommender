# prints the count of the test db

import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://briyksootyszgu:tQemn69JbxhBucAIgWNkLWSkH6@ec2-54-83-51-0.compute-1.amazonaws.com:5432/d8tuou1ths13uu")

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

# cur.execute("CREATE TABLE test(Id INTEGER PRIMARY KEY, testCol VARCHAR(20))")
cur.execute("SELECT COUNT(*) FROM test;")

conn.commit()

count = cur.fetchone()
print count[0]