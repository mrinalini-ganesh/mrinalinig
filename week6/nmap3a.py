#!/usr/bin/python3
# This script will run a brute scan against nsd.org and it will put the DNS names and IP's into a csv file.
# Mrinalini-20230517: initial version

import nmap3
import csv


def scan_dns(target):
    """Function accepts target and returns DNS scan results"""
    nmap = nmap3.Nmap()
    dns_results = nmap.nmap_dns_brute_script(target)
    return dns_results


def filter_ipv4(results):
    """Function filters out IPv6 entries from the scan results"""
    filtered_results = []
    for result in results:
        address = result.get('address', '')
        if ':' not in address:
            hostname = result.get('hostname', '')
            filtered_results.append({'address': address, 'hostname': hostname})
    return filtered_results


def screen_output(scan_list):
    """Function displays the scan results on the screen"""
    print()
    header = f"{'IP':<25} {'DNS':<15}"
    print(header)
    print('-' * len(header))
    for scan_dict in scan_list:
        ip_address = scan_dict['address']
        host = scan_dict['hostname']
        row = f"{ip_address:<25} {host:<15}"
        print(row)


def csv_output(scan_list, filename):
    """Function writes the scan results to a CSV file"""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'DNS']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        for scan_dict in scan_list:
            row_dict = {'IP': scan_dict['address'], 'DNS': scan_dict['hostname']}
            csv_writer.writerow(row_dict)
    print(f'\nOutput saved in {filename}')


def main():
    target = 'nsd.org'
    results = scan_dns(target)
    filtered_results = filter_ipv4(results)
    screen_output(filtered_results)
    csv_output(filtered_results, 'nmap3a.csv')


if __name__ == "__main__":
    main()
