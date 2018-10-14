'''
gh_mining.py

Author: Arjun B. Gupta
Date Created: 12/10/2018

This script was designed to scrape raw files from github, encode them in html, and then store them in a database.
'''

import psycopg2
import requests
import csv

# Connecting to local host database called
conn = psycopg2.connect(database="log6307", user = "arjun", password = "", host = "127.0.0.1", port = "5432")

# Creating a new cursor
cur = conn.cursor()

# Grabing data from database
cur.execute("SELECT postid, ghurl FROM goodurls LIMIT 100")
rows = cur.fetchall()

# Creating an index for progress analysis
index = 0
total = len(rows)

# Exctracting the raw file to insert in the table
for row in rows:
	print(row[0],row[1])
	request = requests.get(row[1])

	# if file still exist, store contents in the ghurl_contents table in database
	if request.status_code == 200:
		data = request.text
		# Replace new lines with html character so that files fit on one line
		url_content = data.replace("\n", "&#xa;")
		cur.execute("INSERT INTO ghurl_contents (postid, data) VALUES (%s, %s)", (row[0], url_content))

	# Every 100 files, print the progress
	if index%100 == 0:
		print("Progress {:2.1%}".format(100 * index / total), end="\r")

	index += 1
	
conn.commit()
print("Operation done successfully")
conn.close()