#!/usr/bin/python3
# This script will search for an IP in the log file, get the MAC address, and print out the vendor of the network device.
# Mrinalini-20230514: second version

import re
import requests
import csv
import time

# Set input and output file paths
input_file = "dhcpdsmall.log"
output_file = "mac_vendor.csv"

# IP addresses to search for
ip_addresses = ["10.172.219.117", "10.192.125.251", "10.172.219.26", "10.191.155.13"]

# Regular expression pattern to match DHCP ACK messages
ack_pattern = r"DHCPACK on ([\d.]+) to ([\da-f:]+)"

# Dictionary to store MAC addresses for the given IP addresses
mac_addresses = {}

# Open input file for reading
with open(input_file, "r") as f:
    # Iterate over each line in the file
    for line in f:
        # Check if the line contains a DHCP ACK message
        match = re.search(ack_pattern, line)
        if match:
            ip_address = match.group(1)
            mac_address = match.group(2)
            if ip_address in ip_addresses:
                mac_addresses[ip_address] = mac_address

# Initialize the CSV data
csv_data = [["IP", "Mac Address", "Vendor"]]

# Function to call macvendors API with a delay
def api_call(mac):
    """Function to call macvendors API"""
    # Necessary delay for API calls
    delay = 0.75
    time.sleep(delay)
    url = f"https://api.macvendors.com/{mac}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f"Error for MAC '{mac}': status code {response.status_code}, response text '{response.text}'")
        return "Unknown"

# Iterate over the IP addresses
for ip_address in ip_addresses:
    mac_address = mac_addresses.get(ip_address)
    if mac_address:
        vendor = api_call(mac_address)
    else:
        vendor = "Not Found"
    csv_data.append([ip_address, mac_address, vendor])

# Write the CSV data to the output file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print("The CSV file generated successfully.")

