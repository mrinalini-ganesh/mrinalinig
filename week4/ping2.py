#!/usr/bin/python3
# This script is a modification of the ping1 script. It will ping the names in the file or the IP/DNS name on the command line and display the results. 
#Mrinalini-20230503:Initial version

import sys
import os
import pinglib

def ping_ip(ip):
    result = pinglib.pingthis(ip)
    print(f"{ip}, {result[1]}")

def ping_file(filename):
    if not os.path.isfile(filename):
        print(f"{filename} is not a valid file.")
        return
    with open(filename) as f:
        for line in f:
            ip_or_dns = line.strip()
            result = pinglib.pingthis(ip_or_dns)
            print(f"{ip_or_dns}, {result[1]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: ping2.py filename or ip/dns")
        return
    arg = sys.argv[1]
    if os.path.isfile(arg):
        ping_file(arg)
    else:
        ping_ip(arg)

if __name__ == "__main__":
    main()
