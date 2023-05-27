#!/usr/bin/python3
# This script will connect to the database and export the data in the rows to CSV and JSON formatted files.
# Mrinalini-20230525: Initial version

import sys
import csv
import json
import pymysql

# Database connection information
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ThisTooShallPass!',
    'database': 'cmdb'
}

# Function to export data to CSV file
def export_to_csv(data):
    with open('device_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if data:  # Check if data is not empty
            writer.writerow(data[0].keys())  # Write header row
            for row in data:
                writer.writerow(row.values())

# Function to export data to JSON file
def export_to_json(data):
    with open('device_data.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Check command-line arguments
if len(sys.argv) != 2 or sys.argv[1] not in ['csv', 'json']:
    print("Usage: python3 database2.py [csv|json]")
    sys.exit(1)

# Connect to the database
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Retrieve data from the 'device' table
    query = "SELECT * FROM device_1"
    cursor.execute(query)
    data = cursor.fetchall()

    # Export data to the specified format
    if sys.argv[1] == 'csv':
        export_to_csv(data)
        print("Data exported to device_data.csv")
    elif sys.argv[1] == 'json':
        export_to_json(data)
        print("Data exported to device_data.json")

    # Close the database connection
    connection.close()

except pymysql.Error as e:
    print("Error connecting to the database:", str(e))
