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
# Need to do some database design here
#dbc.execute("CREATE TABLE users (id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT)")
dbc.execute("DROP TABLE IF EXISTS friends")
dbc.execute("CREATE TABLE friends (id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, profile_picture_url TEXT)")

# Token from Facebook's Graph Explorer - put yours below
# Permissions used: user_about_me, user_friends
oauth_access_token = "CAACEdEose0cBAKfrfZANKmvZAY31q8eji1gQC3WZC1sCzZAxFnQWTLU6kJDvTGvb4XNjbvzIJ5htnRei6fw2hZBvaJDifV7qSp7OlrO03aZBZCC1rWpVwC9aZBvXonOrW3VU1uOvzzNMF2hDqOd0ibJdBHqurPPZBEcv69ersSHlzR5GZAZBq4kLQZBWeE2ZCqHus3kQZD"

# Create the Friend object
class Friend(object):
    friend_id = 0
    first_name = ""
    last_name = ""
    profile_picture_url = ""

    def __init__(self, id, first_name, last_name, profile_picture_url):
        self.friend_id = friend_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture_url = profile_picture_url

    # Insert the friend's ID and name into the friends table
    def store_friend(self):
        dbc.execute("INSERT INTO friends VALUES (?, ?, ?, ?)", (friend_id, first_name, last_name, profile_picture_url))


# Access the Graph
graph = facebook.GraphAPI(oauth_access_token)
print "\nGraph gotten!\n"

# Pull my profile
profile = graph.get_object("me")
print "Hello, " + profile['name'] + "\n"

# Get my friends' Facebook ID, first name and last name
friend_list = graph.get_connections("me", "friends", fields="first_name, last_name")

# Time to go through the list
for friend in friend_list['data']:

    # Pull id and name from list for each friend 
    friend_id = friend['id'].encode('ascii', 'ignore')
    first_name = friend['first_name'].encode('ascii', 'ignore')
    last_name = friend['last_name'].encode('ascii', 'ignore')

    # Pulls the URL for .
    profile_picture_request = graph.get_object(friend_id, fields="picture")
    profile_picture_url = profile_picture_request['picture']['data']['url'].encode('ascii', 'ignore')

    current_friend = Friend(friend_id, first_name, last_name, profile_picture_url)
    print "Added " + current_friend.first_name + " " + current_friend.last_name

    # Insert the friend's attributes into the friends table
    current_friend.store_friend()

# Commit changes to db
dbconnection.commit()

print "\nDing! All done!\n\nClosing access to the database now.\n\nGoodbye."
dbconnection.close()

# Now open the database in SQLite to see your data!