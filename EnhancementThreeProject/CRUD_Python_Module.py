# NAME: CRUD Python Module
# DESCRIPTION: Create, Read, and Delete functions for a MySQL database
# AUTHOR: Joshua Pickle
# LAST EDITED: 2/5/2026

# Used ChatGPT for some bug-fixing. Code is my own.

# NOTE: As it turns out, to use PyMySQL, you need to have a connection variable, which needs to be closed because it might not always close by itself
# NOTE: From what I can tell, when you return a connection variable via a function, it doesn't return the connection itself, only database access
# NOTE: As such, each function that wants to access the SQL database must individually connect to the SQL database so that it can close its connection.

import pymysql

class AnimalShelter(object): 
    def __init__(self, username, password): 
        # Connection Variables 
        self.USER = username 
        self.PASS = password 
        self.HOST = 'localhost' 
        self.PORT = 3306 
        self.DB = 'aac'
        self.CHARSET = 'utf8mb4'

    # Method to return the next available record number for use in the create method (COMPLETE?)
    def findNextRecordNumber(self):
        db = pymysql.connect(
            host = self.HOST,
            port = self.PORT,
            user = self.USER,
            password = self.PASS,
            database = self.DB,
            charset = self.CHARSET
        )
        dbCur = db.cursor(pymysql.cursors.DictCursor)
        # Get the details of the largest record number in the collection
        dbCur.execute('SELECT animal_id FROM animals ORDER BY animal_id DESC LIMIT 1')
        lastRecordDict = dict(dbCur.fetchone())
        # Database access no longer necessary
        dbCur.close()
        db.close()
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
        if data is not None: 
            # Update the record number with a new record number
            data['animal_id'] = self.findNextRecordNumber()

            db = pymysql.connect(
            host = self.HOST,
            port = self.PORT,
            user = self.USER,
            password = self.PASS,
            database = self.DB,
            charset = self.CHARSET
            )
            dbCur = db.cursor(pymysql.cursors.DictCursor)
            # Perform the insertion
            textQuery = 'INSERT INTO animals (animal_id, animal_type, breed, sex_upon_outcome,' \
                ' age_upon_outcome_in_weeks, name, location_lat, location_long) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            dataQuery = (data['animal_id'], data['animal_type'], data['breed'], data['sex_upon_outcome'], data['age_upon_outcome_in_weeks'],
                 data['name'], data['location_lat'], data['location_long']
                )
            dbCur.execute(textQuery, dataQuery)
            db.commit()
            # Get the database entry with the animal_id
            textQuery = 'SELECT * FROM animals WHERE animal_id = %s'
            dbCur.execute(textQuery, data['animal_id'])
            result = dict(dbCur.fetchall())
            dbCur.close()
            db.close()
            return result
        else: 
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.
    def read(self, query):
        db = pymysql.connect(
            host = self.HOST,
            port = self.PORT,
            user = self.USER,
            password = self.PASS,
            database = self.DB,
            charset = self.CHARSET
        )
        dbCur = db.cursor(pymysql.cursors.DictCursor)
        textQuery, dataQuery = self.queryToWHERE(query)
        textQuery = 'SELECT animal_id, animal_type, breed, sex_upon_outcome, age_upon_outcome_in_weeks, name, location_lat, location_long FROM animals' + textQuery
        dbCur.execute(textQuery, dataQuery)
        results = dbCur.fetchall()
        dbCur.close()
        db.close()
        return results
    
    # Create method to implement the D in CRUD
    def delete(self, query):
        db = pymysql.connect(
            host = self.HOST,
            port = self.PORT,
            user = self.USER,
            password = self.PASS,
            database = self.DB,
            charset = self.CHARSET
        )
        dbCur = db.cursor(pymysql.cursors.DictCursor)
        textQuery, dataQuery = self.queryToWHERE(query)
        textQuery = 'SELECT * FROM animals' + textQuery
        dbCur.execute(textQuery, dataQuery)
        numToAffect = dbCur.fetchall()
        if len(list(numToAffect)) > 0:
            textQuery, dataQuery = self.queryToWHERE(query)
            textQuery = 'DELETE FROM animals' + textQuery
            dbCur.execute(textQuery, dataQuery)
            db.commit()
            dbCur.close()
            db.close()
            return numToAffect
        else:
            dbCur.close()
            db.close()
            raise Exception("Nothing to delete")
        
    # Create method to handle MongoDB query (for WHERE)
    def queryToWHERE(self, query):
        # If query doesn't exist, don't bother with anything else
        if not query:
            return '', ()
        
        # Instantiate return values
        textQuery = ''
        dataQuery = ()

        # Loop through each of the columns of the query
        for column in query:
            # If it's the first loop, give the text query its initial "WHERE"
            if (textQuery == ''):
                textQuery = ' WHERE '
            # If it's not the first loop, separate the next query from the previous one with "AND"
            else: 
                textQuery += ' AND '

            # Start the next column assignment
            textQuery += column

            # Check if the query for the column is a special expression
            if (isinstance(query[column], dict)):
                # Check if the special expression is IN
                if '$in' in query[column]:
                    # Check that IN expression exists
                    if query[column]['$in']:
                        # Special expression is IN
                        textQuery += ' IN ('
                        # Go through the IN values, adding them to the query
                        for value in query[column]['$in']:
                            textQuery += '%s, '
                            dataQuery = dataQuery + (value,)
                        # Remove extra separator text, end IN 
                        textQuery = textQuery.removesuffix(', ') + ')'
                    # Cover empty IN case (results should be empty)
                    else:
                        return ' WHERE 1 = 0', ()
                # Check if the special expression is GTE and LTE (extra steps from just one of them)
                elif '$gte' in query[column] and '$lte' in query[column]:
                    # Special expression is both GTE and LTE
                    textQuery += ' >= %s AND ' + column + ' <= %s'
                    dataQuery += (query[column]['$gte'], query[column]['$lte'])
                # Check if the special expression is just GTE
                elif '$gte' in query[column]:
                    # Special expression is just GTE
                    textQuery += ' >= %s'
                    dataQuery = dataQuery + (query[column]['$gte'],)
                # Check if the special expression is just LTE
                elif '$lte' in query[column]:
                    textQuery += ' <= %s'
                    dataQuery = dataQuery + (query[column]['$lte'],)
            # Query for the column is a single value
            else:
                textQuery += ' = %s'
                dataQuery = dataQuery + (query[column],)
        
        # Return final query values
        return textQuery, dataQuery


        