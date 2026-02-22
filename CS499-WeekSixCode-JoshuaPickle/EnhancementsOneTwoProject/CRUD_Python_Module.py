# NAME: CRUD Python Module
# DESCRIPTION: Create, Read, Update, and Delete functions for a MongoDB database
# AUTHOR: Joshua Pickle
# LAST EDITED: 1/21/2026

# Used ChatGPT for some bug-fixing. Code is my own.

from pymongo import MongoClient 

class AnimalShelter(object): 
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
        COL = 'animals'

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
        COL = 'animals' 

        # Initialize Connection 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]

    # Method to return the next available record number for use in the create method
    def findNextRecordNumber(self):
        # Get the details of the largest record number in the collection
        lastRecordDetails = self.database.animals.find({}, 
        {'_id': 0, 'animal_id': 1}).sort({'animal_id': -1}).limit(1)
        # Parse the cursor object into a dictionary
        lastRecordDict = dict()
        lastRecordDict = dict(enumerate(list(lastRecordDetails)))
        # Get the last two numbers of the id and turn them into integers, and add one to make
        # a new highest id ending
        idLastNums = int(lastRecordDict['animal_id'][-1]) + (int(
            lastRecordDict['animal_id'][-2]) * 10) + 1
        # Replace the last two characters of the id with the new highest new highest id
        # ending to make the new highest id
        lastRecordDict['animal_id'] = lastRecordDict['animal_id'][:-2] + chr(
            ord('0') + idLastNums // 10) + chr(ord('0') + idLastNums % 10)
        # Return the new highest id
        return lastRecordDict['animal_id']
    
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        # Update the record number with a new record number
        data['animal_id'] = self.findNextRecordNumber()
        
        if data is not None: 
            return self.database.animals.insert_one(data)  # data should be dictionary
        else: 
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.
    def read(self, query):
        return self.database.animals.find(query)
    
    # Create method to implement the U in CRUD.
    def update(self, query, updates):
        updateResults = self.database.animals.update_many(query, {'$set': updates })
        return updateResults.modified_count
    
    # Create method to implement the D in CRUD
    def delete(self, query):
        readResults = self.read(query)
        if len(list(readResults)) > 0:
            self.database.animals.delete_many(query)
            return len(list(readResults))
        else:
            raise Exception("Nothing to delete")
            