#!/usr/bin/python3
# This script is the same as ping2, but takes an optional second command line argument that is a csv output file.
#Mrinalini-20230503:Initial version

import sys
import os
import csv
import pinglib

# Function to ping an IP address
def ping_ip(ip):
    result = pinglib.pingthis(ip)
    print(f"{ip}, {result[1]}")
    return result

# Function to ping a list of IPs in a file
def ping_file(filename, output_file=None):
    if not os.path.isfile(filename):
        print(f"{filename} is not a valid file.")
        return

    # Create a list to store the results
    results = []

    with open(filename) as f:
        for line in f:
            ip_or_dns = line.strip()
            result = pinglib.pingthis(ip_or_dns)

            # Appending the IP and ping time to the results list
            if result[1] != "Not Found":
                results.append([ip_or_dns, result[1]])

            print(f"{ip_or_dns}, {result[1]}")

    # Write results to CSV if output file is specified
    if output_file:
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["IP", "TimeToPing (ms)"])
            for row in results:
                writer.writerow(row)

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: ping3.py filename or ip/dns [output_file.csv]")
        return

    # Check if the second argument is an output file
    if len(sys.argv) == 3:
        output_file = sys.argv[2]
    else:
        output_file = None

    # Check if the first argument is a file or IP/DNS
    arg = sys.argv[1]
    if os.path.isfile(arg):
        ping_file(arg, output_file)
    else:
        result = ping_ip(arg)

        # Write single IP result to CSV if output file is specified
        if output_file:
            with open(output_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["IP", "TimeToPing (ms)"])
                if result[1] != "Not Found":
                    writer.writerow([arg, result[1]])

# Execute the main function
if __name__ == "__main__":
    main()
