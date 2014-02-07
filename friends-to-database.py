#!/usr/bin/env python
#
# Friends to Database
# Created by Michael Rudden, 2014
#
# Uses Facebook Python SDK (https://github.com/pythonforfacebook/facebook-sdk)

import facebook
import sqlite3

# Set up SQLite database!!
dbconnection = sqlite3.connect('friends.db')

dbc = dbconnection.cursor()

# Create table
dbc.execute("CREATE TABLE friends (id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT)")

# Token from Facebook's Graph Explorer - put yours below
# Permissions used: user_about_me, user_friends
oauth_access_token = "token goes here"

# Access the Graph
graph = facebook.GraphAPI(oauth_access_token)
print "\nGraph gotten!\n"

# Pull my profile
profile = graph.get_object("me")
print "Hello, " + profile['name'] + "\n"

# Get my friends' Facebook ID, first name and last name
friends = graph.get_connections("me", "friends", fields="first_name, last_name")

# Retrieve list of friends
friend_list = friends['data']

print "Adding your friends to the database!"

# Time to go through the list
for friend in friend_list:

    # Pull id and name from list for each friend 
    friend_id = friend['id'].encode('ascii', 'ignore')
    first_name = friend['first_name'].encode('ascii', 'ignore')
    last_name = friend['last_name'].encode('ascii', 'ignore')

    # Insert the friend's ID and name into the friends table
    dbc.execute("INSERT INTO friends VALUES (?, ?, ?)", (friend_id, first_name, last_name))

# Commit changes to db
dbconnection.commit()

print "\nDing! All done!\n\nClosing access to the database now.\n\nGoodbye."
dbconnection.close()

# Now open the database in SQLite to see your data!