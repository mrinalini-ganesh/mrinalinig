#!/usr/bin/python3
# This script will write to nmap2.csv with an additional column.
# Mrinalini-20230517: initial version

import csv
from nmap3 import Nmap

# Read the IPs and open ports from nmap1.csv
input_filename = "nmap1.csv"
output_filename = "nmap2.csv"

ip_ports = []
with open(input_filename, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ip = row["IP"]
        open_ports = [port.strip("[]'") for port in row["Open Ports"].split(", ")]
        ip_ports.append({"IP": ip, "Open Ports": open_ports})

# Perform OS detection scan for each IP address
nm = Nmap()
for entry in ip_ports:
    ip = entry["IP"]

    # Perform OS detection scan
    result = nm.nmap_os_detection(ip)
    os_guesses = result[ip]["osmatch"]

    # Determine the best guess for OS
    best_guess = None
    highest_accuracy = 0
    for guess in os_guesses:
        accuracy = int(guess["accuracy"])  # Convert accuracy to integer
        if accuracy > highest_accuracy:
            best_guess = guess["name"]
            highest_accuracy = accuracy

    # Add the best guess to the dictionary
    entry["OS Guess"] = best_guess

# Save the results to nmap2.csv
with open(output_filename, "w", newline="") as csvfile:
    fieldnames = ["IP", "Open Ports", "OS Guess"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for entry in ip_ports:
        writer.writerow({"IP": entry["IP"], "Open Ports": " ".join(entry["Open Ports"]), "OS Guess": entry["OS Guess"]})

print(f"Scan results saved to {output_filename}")
