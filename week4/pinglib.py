#!/usr/bin/python3
# This script takes in an IP or DNS name and pings it
#Mrinalini-20230503:initial version

import subprocess

def pingthis(ipordns):
    # Call ping command and capture output
    ping_output = subprocess.run(['ping', '-c', '1', ipordns], capture_output=True, text=True)
    
    # Check if ping was successful
    if ping_output.returncode == 0:
        # Parse ping time from output
        time_str = ping_output.stdout.split('time=')[1].split(' ')[0]
        time_ms = int(float(time_str))
        
        # Return IP and ping time
        return [ipordns, time_ms]
    else:
        # Return IP and "Not Found"
        return [ipordns, "Not Found"]

import sys

def main():
    # Get IP or DNS from command line argument
    ipordns = sys.argv[1]
    
    # Call pingthis function
    result = pingthis(ipordns)
    
    # Print result
    print(result[0] + ', ' + str(result[1]))

if __name__ == '__main__':
    main()
