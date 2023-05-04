#!/usr/bin/python3
# This script that reads a file of IPs and names, pings each one using the pinglib library, and prints the results to the screen.
#Mrinalini-20230503:Intial version

import sys
import pinglib

def main():
    # Check if file argument is passed
    if len(sys.argv) < 2:
        print("Please provide a file of IPs and names as an argument.")
        return

    # Get file name from argument
    filename = sys.argv[1]

    # Read IPs and names from file
    with open(filename, "r") as f:
        for line in f:
            # Split line into IP and name
            ip, name = line.strip().split()

            # Ping IP and get time
            result = pinglib.pingthis(ip)

            # Print result
            print(f"{name}, {result[1] if result else 'Not Found'}")

if __name__ == "__main__":
    main()
