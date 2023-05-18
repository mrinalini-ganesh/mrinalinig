#!/usr/bin/python3
# This script will scan the waveventlog file and create a csv file.
# Mrinalini-20230514: second version

import re
from collections import defaultdict

# Define the regex pattern to extract redirect information
redirect_pattern = re.compile(r'REDIRECT: (.*?) to (https?://\S+)')

# Initialize a dictionary to store redirect information
redirect_dict = {}

# Read the wafeventlog file
with open('wafeventlog', 'r') as f:
    for line in f:
        if "ActiveSync" in line or "Basic" in line:
            continue
        match = redirect_pattern.search(line)
        if match:
            from_value = match.group(1)
            to_value = match.group(2)
            if from_value in redirect_dict and redirect_dict[from_value][0] == to_value[:-2]:
                redirect_dict[from_value][1] += 1
            else:
                redirect_dict[from_value] = [to_value[:-2], 1]

# Write the redirect information to a file
with open('redirects.csv', 'w') as f:
    f.write("Count, From, To\n")
    for from_value, (to_value, count) in redirect_dict.items():
        if count > 1:
            f.write(f"{count},\"{from_value}\",\"{to_value}\"\n")

print("Redirect information has been written to redirects.csv")
