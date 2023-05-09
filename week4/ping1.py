#!/usr/bin/python3
# This script reads a file of IPs and names, pings each one using the pinglib library, and prints the results to the screen.
# Mrinalini-20230505: Second version

import pinglib
import sys

def main():
    # Get filename from command line argument
    filename = sys.argv[1]

    # Open file and read IP/DNS names
    with open(filename, 'r') as file:
        ipordns_list = file.readlines()

    # Ping each IP/DNS and print results
    for ipordns in ipordns_list:
        ipordns = ipordns.strip()  # Remove newline character
        result = pinglib.pingthis(ipordns)
        print(f"{result[0]}, {result[1]:.2f}" if result[1] != "Not Found" else f"{result[0]}, NotFound")

if __name__ == '__main__':
    main()

