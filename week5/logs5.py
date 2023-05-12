#!/usr/bin/python3
# This script finds if we can get rid of any old redirects we have by scanning the wafeventlog file.
#Mrinalini-20230511:initial version

import re
from collections import defaultdict

# Define the regex pattern to extract redirect information
redirect_pattern = re.compile(r'REDIRECT: (.*?) to (.*?)$')

# Initialize a defaultdict to store redirect counts
redirects = defaultdict(int)

# Read the wafeventlog file
with open('wafeventlog', 'r') as f:
    for line in f:
        # Check if the line contains a redirect entry
        match = redirect_pattern.search(line)
        if match:
            from_url = match.group(1)
            to_url = match.group(2)

            # Exclude redirects with "ActiveSync" and "Basic" in the from_url
            if "ActiveSync" not in from_url and "Basic" not in from_url:
                redirects[(from_url, to_url)] += 1

# Write the redirect information to a file
with open('redirects.csv', 'w') as f:
    f.write("Count, From, To\n")
    for (from_url, to_url), count in redirects.items():
        f.write(f"{count},\"{from_url}\",\"{to_url}\"\n")

print("Redirect information has been written to redirects.csv")

