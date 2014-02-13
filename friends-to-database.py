#!/usr/bin/env python
#
# Friends to Database
# Created by Michael Rudden, 2014
#
# Uses Facebook Python SDK (https://github.com/pythonforfacebook/facebook-sdk)

import facebook
import sqlite3

# Enabled for Mike to test things
debug = True

# Set up SQLite database!!
dbconnection = sqlite3.connect('friends.db')

dbc = dbconnection.cursor()

if debug:
    dbc.execute("DROP TABLE IF EXISTS users")
    dbc.execute("DROP TABLE IF EXISTS friends")
    dbc.execute("DROP TABLE IF EXISTS users_friends")
    dbc.execute("DROP TABLE IF EXISTS notes")

# Create table
# Need to do some database design here
dbc.execute("CREATE TABLE users (fb_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT)")
dbc.execute("CREATE TABLE friends (fb_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT)")
dbc.execute("CREATE TABLE users_friends (id INTEGER PRIMARY KEY, user_id TEXT, friend_id TEXT)")
dbc.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, user_friends_id INTEGER, note TEXT)")

# Token from Facebook's Graph Explorer - put yours below when in debug mode
# Permissions used: user_about_me, user_friends
if debug:
    oauth_access_token = "token_goes_here"

# Create the Person object
class Person(object):

    def __init__(self, fb_id, first_name, last_name):
        self.fb_id = fb_id
        self.first_name = first_name
        self.last_name = last_name

# Create the User object
class User(Person):

    def __init__(self, fb_id, first_name, last_name):
        super(User, self).__init__(fb_id, first_name, last_name)

    def store(self):
        dbc.execute("INSERT INTO users VALUES (?, ?, ?)", (self.fb_id, self.first_name, self.last_name))
        if debug:
            print "Added " + self.first_name + " " + self.last_name + " to the users table."

# Create the Friend object
class Friend(Person):

    def __init__(self, fb_id, first_name, last_name):
        super(Friend, self).__init__(fb_id, first_name, last_name)

    # Insert the friend's ID and name into the friends table
    def store(self):
        dbc.execute("INSERT INTO friends VALUES (?, ?, ?)", (self.fb_id, self.first_name, self.last_name))
        if debug:
            print "Added " + self.first_name + " " + self.last_name + " to the friends table."


# Access the Graph
graph = facebook.GraphAPI(oauth_access_token)
print "\nGraph gotten!\n"

# Pull my profile
profile = graph.get_object("me")
print "Hello, " + profile['name'] + "\n"

# Create User object and call it's store method
user = User(profile['id'], profile['first_name'], profile['last_name'])
user.store()

# Get user's friends' Facebook ID, first name and last name
friend_list = graph.get_connections("me", "friends", fields="first_name, last_name")

# Time to go through the list
for friend in friend_list['data']:

    current_friend = Friend(friend['id'], friend['first_name'], friend['last_name'])

    # Insert the friend's attributes into the friends table
    current_friend.store()

# Commit changes to db
dbconnection.commit()

print "\nDing! All done!\n\n"
if debug:
   print "Closing access to the database now.\n\n"
print "Goodbye."
dbconnection.close()

# Now open the database in SQLite to see your data!