#!/usr/bin/python3
# This script gets the estimate of all the iphones on the network
#Mrinalini-20230510:initial version

import re

iphone_macs = set()

# Open the dhcpdsmall.log to read
with open('dhcpdsmall.log', 'r') as f:
# Loop through each line in the file
    for line in f:
        if 'iPhone' in line:
#To find the MAC Address in each line
            match = re.search(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', line)
            if match:
                mac = match.group(0)
                iphone_macs.add(mac)

print('\n'.join(iphone_macs))
#print the count
print(f"Count = {len(iphone_macs)}")

