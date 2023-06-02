#!/usr/bin/python3
# This script checks the status of servers in servers.csv file and writes the results to updown.csv
# Mrinalini-20230602: initial version

import csv
import subprocess
import time

def pingthis(ipordns):
    # Call ping command and capture output
    ping_output = subprocess.run(['ping', '-c', '1', ipordns], capture_output=True, text=True)
    
    # Check if ping was successful
    if ping_output.returncode == 0:
        # Parse ping time from output
        time_str = ping_output.stdout.split('time=')[1].split(' ')[0]
        time_ms = int(float(time_str))
        
        # Return IP and status
        return [ipordns, "up"]
    else:
        # Return IP and status
        return [ipordns, "down"]

def main():
    # Open servers.csv file
    with open('servers.csv', 'r') as csvfile:
        # Create a reader object
        reader = csv.reader(csvfile)
        
        # Skip the header row
        next(reader)
        
        # Create updown.csv file
        with open('updown.csv', 'w', newline='') as outputfile:
            # Create a writer object
            writer = csv.writer(outputfile)
            
            # Write the header row
            writer.writerow(['Timestamp', 'Server IP', 'Type', 'Status'])
            
            # Iterate over the servers
            for row in reader:
                server_ip = row[1]
                timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                
                # Call pingthis function to get the status
                result = pingthis(server_ip)
                
                # Write the result to updown.csv
                writer.writerow([timestamp, server_ip, 'updown', result[1]])
                
                # Sleep for 10 seconds
                time.sleep(10)

if __name__ == '__main__':
    main()
