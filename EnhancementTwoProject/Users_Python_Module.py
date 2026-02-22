# NAME: User Manager
# DESCRIPTION: Manage the various needs of the user class
# AUTHOR: Joshua Pickle
# LAST EDITED: 1/25/2026

# Used ChatGPT for some bug-fixing. Code is my own.

from pymongo import MongoClient 

from werkzeug.security import generate_password_hash, check_password_hash

class UserManager(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 

        # Connection Variables 
        USER = 'aacuser' 
        PASS = 'CS340pwd' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'users'

        # Initialize Connection 
        self.client = MongoClient('mongodb://%s:%s@%s:%d/?authSource=aac' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 
        
    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 

        # Connection Variables 
        USER = username 
        PASS = password 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'users' 

        # Initialize Connection 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]

    # Method to determine whether a user exists
    def doesUserExist(self, username):
        if self.database.users.find_one({'username': username}) is not None:
            return True
        else:
            return False

    # Method to determine whether a user/password combination exists
    def isSignInCorrect(self, username, password):
        if self.database.users.find_one({'username': username}) is not None and check_password_hash(self.database.users.find_one({'username': username})['password'], password) :
            return True
        else:
            return False
        
    # Method to create a new user
    def createUser(self, username, password):
        if username is not None and password is not None:
            return self.database.users.insert_one({'username': username, 'password': generate_password_hash(password)})
        else:
            raise Exception("Nothing to save, because data parameter is empty")
        

            