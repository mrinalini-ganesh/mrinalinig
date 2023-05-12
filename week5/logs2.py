#!/usr/bin/python3
# This script reads the dhcp server and produces a csv file with the Mac address, IP address and Total number of acks
#Mrinalini-20230510:initial version

import re

# Set input and output file paths
input_file = "dhcpdsmall.log"
output_file = "dhcpd_ack_counts.csv"
problem_macs_file = "ProblemMacs.txt"

# Regular expression pattern to match DHCP ACK messages
ack_pattern = r"DHCPACK on ([\d.]+) to ([\da-f:]+)"

# Dictionary to store counts of ACK messages by MAC address and IP
ack_counts = {}

# Open input file for reading
with open(input_file, "r") as f:
    # Iterate over each line in the file
    for line in f:
        # Check if the line contains a DHCP ACK message
        match = re.search(ack_pattern, line)
        if match:
            ip_address = match.group(1)
            mac_address = match.group(2)
            # Combine MAC address and IP address to use as dictionary key
            key = mac_address + "-" + ip_address
            # Increment the count for this key
            ack_counts[key] = ack_counts.get(key, 0) + 1

# Check if there are MAC addresses with ACK counts
if len(ack_counts) > 0:
    # Get the top two MAC addresses and their ACK counts
    top_macs = sorted(ack_counts.items(), key=lambda x: x[1], reverse=True)[:2]
    top_mac1 = top_macs[0][0]
    top_ack1 = top_macs[0][1]
    top_mac2 = top_macs[1][0]
    top_ack2 = top_macs[1][1]

    # Print the top two MAC addresses and their ACK counts
    print("The top two MAC addresses and their ACK counts are:")
    print(f"{top_mac1}, {top_ack1}")
    print(f"{top_mac2}, {top_ack2}")

    # Write the output to the ProblemMacs.txt file
    with open(problem_macs_file, "w") as f:
        f.write("The top two MAC addresses and their ACK counts are:\n")
        f.write(f"{top_mac1}, {top_ack1}\n")
        f.write(f"{top_mac2}, {top_ack2}\n\n")
        f.write("Mac address,IP address,Total number of acks\n")
        for key, ack_count in ack_counts.items():
            mac_address, ip_address = key.split("-")
            f.write(f"{mac_address},{ip_address},{ack_count}\n")
else:
    print("No DHCP ACK messages were found in the log file.")

