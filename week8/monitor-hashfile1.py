#!/usr/bin/python3
# This script will take in on the command line a full path, create an MD5 hash of the file, and store it in the database.
# If the file path already exists in the database, it prompts the user to update the hash if desired.

import sys
import hashlib
import datetime
import mysql.connector

# Get the file path from the command line argument
file_path = sys.argv[1]

# Establish a connection to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ThisTooShallPass!",
    database="cmdb"
)

# Create a cursor to execute SQL queries
cursor = cnx.cursor()

# Check if the file path already exists in the database
select_query = "SELECT path, hash FROM files WHERE path = %s"
cursor.execute(select_query, (file_path,))
result = cursor.fetchone()

if result:
    # File path exists in the database, prompt the user to update the hash
    print("This file path already exists in the database.")
    choice = input("Would you like to update the hash? (y/n): ")
    
    if choice.lower() == 'y':
        # Read the file and calculate the new MD5 hash
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_hash = hashlib.md5(file_data).hexdigest()
        
        # Get the current timestamp in ISO format
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Update the hash in the database
        update_query = "UPDATE files SET hash = %s, timestamp = %s WHERE path = %s"
        cursor.execute(update_query, (file_hash, timestamp, file_path))
        cnx.commit()
        print("Hash updated successfully.")
    else:
        print("There were no changes made. Exiting...")
else:
    # File path doesn't exist in the database, add it with the hash
    # Read the file and calculate the MD5 hash
    with open(file_path, 'rb') as file:
        file_data = file.read()
        file_hash = hashlib.md5(file_data).hexdigest()

    # Get the current timestamp in ISO format
    timestamp = datetime.datetime.utcnow().isoformat()

    # Prepare the SQL query to insert the data into the 'files' table
    insert_query = "INSERT INTO files (timestamp, path, hash) VALUES (%s, %s, %s)"

    # Execute the query with the timestamp, file path, and hash as parameters
    cursor.execute(insert_query, (timestamp, file_path, file_hash))
    cnx.commit()
    print("File hash added to the database.")

# Close the cursor and the database connection
cursor.close()
cnx.close()
