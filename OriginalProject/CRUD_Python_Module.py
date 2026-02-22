# Example Python Code to Insert a Document 

# Used ChatGPT for some bug-fixing. Code is my own.

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'CS340pwd' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 
        
    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Connection Variables 
        # 
        USER = username 
        PASS = password 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]
        
    #def __init__(self, username, password, host, port, db, collection):
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Connection Variables 
        # 
        #USER = username 
        #PASS = password 
        #HOST = host 
        #PORT = port 
        #DB = db
        #COL = collection 
        # 
        # Initialize Connection 
        # 
        #self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        #self.database = self.client['%s' % (DB)] 
        #self.collection = self.database['%s' % (COL)]
        

    # Create a method to return the next available record number for use in the create method
    def findNextRecordNumber(self):
        # Get the details of the largest record number in the collection
        lastRecordDetails = self.database.animals.find({}, 
        {'_id': 0, 'animal_id': 1}).sort({'animal_id': -1}).limit(1)
        # Parse the cursor object into a dictionary
        lastRecordDict = dict()
        for result in lastRecordDetails:
            lastRecordDict.update(result)
        # Get the last two numbers of the id and turn them into integers, and add one to make
        # a new highest id ending
        idLastNums = int(lastRecordDict['animal_id'][-1]) + (int(
            lastRecordDict['animal_id'][-2])* 10) + 1
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
            return {}

    # Create method to implement the R in CRUD.
    def read(self, query):
        readResults = self.database.animals.find(query)
        return readResults
    
    # Create method to implement the U in CRUD.
    def update(self, query, updates):
        updateResults = self.database.animals.update_many(query, {'$set': updates })
        return updateResults.modified_count
    
    # Create method to implement the D in CRUD
    def delete(self, query):
        readResults = self.read(query)
        readResultsSize = len(list(readResults))
        if readResultsSize > 0:
            self.database.animals.delete_many(query)
            return readResultsSize
        else:
            raise Exception("Nothing to delete")
            return 0
            