#!/usr/bin/python3
# This script will take in on the command line a full path, create a MD5 hash of the file and the timestamp, file path, and hash to a databse table.
# Mrinalini-20230529: Initial version

import sys
import hashlib
import datetime
import mysql.connector

# Get the file path from the command line argument
file_path = sys.argv[1]

# Read the file and calculate the MD5 hash
with open(file_path, 'rb') as file:
    file_data = file.read()
    file_hash = hashlib.md5(file_data).hexdigest()

# Get the current timestamp in ISO format
timestamp = datetime.datetime.utcnow().isoformat()

# Establish a connection to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ThisTooShallPass!",
    database="cmdb"
)

# Create a cursor to execute SQL queries
cursor = cnx.cursor()

# Prepare the SQL query to insert the data into the 'files' table
insert_query = "INSERT INTO files (timestamp, path, hash) VALUES (%s, %s, %s)"

# Execute the query with the timestamp, file path, and hash as parameters
cursor.execute(insert_query, (timestamp, file_path, file_hash))

# Commit the changes to the database
cnx.commit()

# Close the cursor and the database connection
cursor.close()
cnx.close()
