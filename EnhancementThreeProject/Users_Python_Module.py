# NAME: User Manager
# DESCRIPTION: Manage the various needs of the user class
# AUTHOR: Joshua Pickle
# LAST EDITED: 2/5/2026

# Used ChatGPT for some bug-fixing. Code is my own.

import pymysql

from werkzeug.security import generate_password_hash, check_password_hash

class UserManager(object): 
    def __init__(self, username, password):
        # Connection Variables 
        self.USER = username 
        self.PASS = password 
        self.HOST = 'localhost' 
        self.PORT = 3306
        self.DB = 'aac'
        self.CHARSET = 'utf8mb4' 

    # Method to determine whether a user exists (COMPLETE?)
    def doesUserExist(self, username):
        db = pymysql.connect(
            host = self.HOST,
            port = self.PORT,
            user = self.USER,
            password = self.PASS,
            database = self.DB,
            charset = self.CHARSET
        )
        dbCur = db.cursor(pymysql.cursors.DictCursor)
        textQuery = 'SELECT username FROM users WHERE username = %s'
        dbCur.execute(textQuery, username)
        potentialUser = dbCur.fetchone()
        dbCur.close()
        db.close()
        if potentialUser is not None:
            return True
        else:
            return False

    # Method to determine whether a user/password combination exists
    def isSignInCorrect(self, username, password):
        db = pymysql.connect(
            host = self.HOST,
            port = self.PORT,
            user = self.USER,
            password = self.PASS,
            database = self.DB,
            charset = self.CHARSET
        )
        dbCur = db.cursor(pymysql.cursors.DictCursor)
        textQuery = 'SELECT * FROM users WHERE username = %s'
        dbCur.execute(textQuery, username)
        potentialUser = dbCur.fetchone()
        dbCur.close()
        db.close()
        if potentialUser is not None and check_password_hash(potentialUser['password'], password) :
            return True
        else:
            return False
        
    # Method to create a new user
    def createUser(self, username, password):
        if username is not None and password is not None:
            db = pymysql.connect(
                host = self.HOST,
                port = self.PORT,
                user = self.USER,
                password = self.PASS,
                database = self.DB,
                charset = self.CHARSET
            )
            dbCur = db.cursor(pymysql.cursors.DictCursor)
            textQuery = 'INSERT INTO users (username, password) VALUES (%s, %s)'
            dataQuery = (username, generate_password_hash(password))
            dbCur.execute(textQuery, dataQuery)
            db.commit()
            # Get the new user from the username
            textQuery = 'SELECT * FROM users WHERE username = %s'
            dbCur.execute(textQuery, username)
            newUser = dbCur.fetchone()
            dbCur.close()
            db.close()
            return newUser
        else:
            raise Exception("Nothing to save, because data parameter is empty")
        

            