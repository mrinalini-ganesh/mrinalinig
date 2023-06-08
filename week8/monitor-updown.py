#!/usr/bin/python3
# This script checks the status of servers in servers.csv file and writes the results to updown.csv
# Mrinalini-20230602: initial version

import csv
import time
from datetime import datetime  # Import the datetime module
import subprocess

def pingthis(ipordns):
    # Call ping command and capture output
    ping_output = subprocess.run(['ping', '-c', '1', ipordns], capture_output=True, text=True)

    # Check if ping was successful
    if ping_output.returncode == 0:
        # Return IP and status
        return "up"
    else:
        # Return IP and status
        return "down"

def main():
    num_iterations = 4  # Number of times to loop the server checking process
    
    for _ in range(num_iterations):
        with open('servers.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

            with open('updown.csv', 'w', newline='') as outputfile:
                writer = csv.writer(outputfile)
                writer.writerow(['Timestamp', 'Server IP', 'Type', 'Status'])

                for row in reader:
                    if row:  # Check if row is not empty
                        server_ip = row[0]
                        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Use datetime.now() to get the current timestamp

                        result = pingthis(server_ip)
                        writer.writerow([timestamp, server_ip, 'updown', result])

                    else:
                        print("Invalid row format in servers.csv")

        print("Iteration completed!")
        time.sleep(10)
    
    # Print a message after the loop completes
    print("Server checking completed!")

if __name__ == '__main__':
    main()
