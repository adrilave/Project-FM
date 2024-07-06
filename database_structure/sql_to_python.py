import mysql.connector # For sql-python connection
import sys
import pandas as pd


#------------------------------------------------------------------------------------------------------------------------#

# Connection to the database

db = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = "root",
    database = "fm")

cursor = db.cursor()

#------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------#

# Query to database function

def query_to_database(query: str) -> pd.DataFrame:
    
    # To create a pandas dataframe from the sql query
    # query : (str) takes the mysql query as input
    # returns : (pd.DataFrame) returns the dataframe of the query
    
    cursor.execute(query)
    sequence = cursor.column_names
    myresult = cursor.fetchall()
    
    df = pd.DataFrame(myresult)
    df.columns = sequence
    
    return df

#------------------------------------------------------------------------------------------------------------------------#
