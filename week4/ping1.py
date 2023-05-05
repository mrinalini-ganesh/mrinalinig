#!/usr/bin/python3
# This script reads a file of IPs and names, pings each one using the pinglib library, and prints the results to the screen.
# Mrinalini-20230505: Second version

import sys
import pinglib

def main():
    # Check if the file argument is passed
    if len(sys.argv) < 2:
        print("Please provide a file of IPs and names as an argument.")
        return

    # Get the file name from argument
    filename = sys.argv[1]

    # Read IPs and names from file
    with open(filename, "r") as f:
        for line in f:
            # Split the line into IP and name
            fields = line.strip().split()
            if len(fields) != 2:
                print(f"Invalid line in {filename}: {line}")
                continue
            ip, name = fields

            # Ping IP and get the time
            result = pinglib.pingthis(ip)

            # Print result with 2 decimal places
            print(f"{name}, {result[1]:.2f}" if result else f"{name}, Not Found")

if __name__ == "__main__":
    main()

