#!/usr/bin/python3
# This script will do a syn scan on two IP ranges and create a CSV file.
# Mrinalini - 20230517: initial version

import csv
import nmap3

# Define the IP ranges to scan
ip_ranges = ["152.157.64.0/24", "152.157.65.0/24"]

# Perform SYN scan using nmap3 and save results
ip_ports = []
nmap = nmap3.NmapScanTechniques()
for ip_range in ip_ranges:
    result = nmap.nmap_syn_scan(ip_range)

    for ip in result:
        if "ports" in result[ip]:
            open_ports = [str(port["portid"]) for port in result[ip]["ports"] if port["state"] == "open"]
            if open_ports:
                ip_ports.append({"IP": ip, "Open Ports": " ".join(open_ports)})

# Save results to CSV file
filename = "nmap1.csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["IP", "Open Ports"])

    for entry in ip_ports:
        writer.writerow([entry["IP"], entry["Open Ports"]])

print(f"Scan results saved to {filename}")
