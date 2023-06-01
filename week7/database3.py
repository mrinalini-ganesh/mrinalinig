#!/usr/bin/python3
# This script retrieves server information and inserts it into the 'device_1' table in the 'cmdb' database.
# Mrinalini-20230526: Updated version

import os
import socket
import pymysql

# Get the hostname of the machine
hostname = socket.gethostname()

# Get the number of CPUs on the machine
cpus = os.cpu_count()

# Get the amount of RAM in GB
ram = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.0 ** 3))

# Get the OS type and version
if os.path.exists('/etc/os-release'):
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if line.startswith('NAME='):
                ostype = line.split('=')[1].strip().strip('"')
            elif line.startswith('VERSION_ID='):
                osversion = line.split('=')[1].strip().strip('"')
else:
    ostype = os.name
    osversion = os.sys.platform

# Get the number of disks
disks = len([d for d in os.listdir('/sys/block') if not d.startswith(('loop', 'ram'))])

# Get the IP and MAC address
ifconfig = os.popen('ip addr show').read()
if 'inet ' in ifconfig:
    ipaddr = ifconfig.split('inet ')[1].split('/')[0].strip()
else:
    ipaddr = 'unknown'
if 'ether ' in ifconfig:
    macaddr = ifconfig.split('ether ')[1].split(' ')[0].strip()
else:
    macaddr = 'unknown'

# Database connection information
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ThisTooShallPass!',
    'database': 'cmdb'
}

# Function to insert server information into the database
def insert_server_info(data):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Truncate the name field if its length exceeds the maximum allowed length
        max_name_length = 50
        name = str(data[0])[:max_name_length].ljust(max_name_length) if len(data) > 0 else ''

        # Prepare the SQL query
        query = "INSERT INTO device (name, macaddress, ip, cpucount, disks, ram, ostype, osversion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, data[1], data[2], data[3], data[4], data[5], data[6], data[7])

        # Execute the query
        cursor.execute(query, values)
        connection.commit()

        print("Server information inserted successfully.")

        # Close the database connection
        connection.close()

    except pymysql.Error as e:
        print("Error connecting to the database:", str(e))

# Create the server_info list
server_info = [hostname, macaddr, ipaddr, cpus, disks, ram, ostype, osversion]

# Call the insert_server_info function
insert_server_info(server_info)
