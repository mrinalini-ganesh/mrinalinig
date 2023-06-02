#!/usr/bin/python3
# This script will read the data of file hashes in the database and check them against newly calculated hashes of the files on disk.
# It will then print out a CSV file (filecheck.csv) with the specified columns.

import csv
import hashlib
import datetime
import mysql.connector

# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ThisTooShallPass!",
    database="cmdb"
)

# Create a cursor to execute SQL queries
cursor = cnx.cursor()

# Retrieve the file hashes from the database
select_query = "SELECT path, hash FROM files"
cursor.execute(select_query)
file_hashes = cursor.fetchall()

# Prepare the CSV file
csv_file = open("filecheck.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["filepath", "dbhash", "db hash date", "current hash", "status"])

# Iterate through the file hashes and check against the current hashes
for path, dbhash in file_hashes:
    with open(path, 'rb') as file:
        file_data = file.read()
        current_hash = hashlib.md5(file_data).hexdigest()
    
    # Get the current timestamp in ISO format
    timestamp = datetime.datetime.utcnow().isoformat()
    
    # Compare the current hash with the database hash
    if current_hash == dbhash:
        status = "ok"
    else:
        status = "file changed"
    
    # Write the row to the CSV file
    csv_writer.writerow([path, dbhash, timestamp, current_hash, status])

# Close the cursor and the database connection
cursor.close()
cnx.close()

# Close the CSV file
csv_file.close()

print("Filecheck completed. Please check the filecheck.csv for the results.")
