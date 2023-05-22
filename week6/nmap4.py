#!/usr/bin/python3
# This script will scan the waveventlog file and create a csv file.
# Mrinalini-20230514: second version

import nmap3
import csv
import requests

DEFAULT_TARGET = 'nsd.org'

def main():
    result_list = scan_dns(DEFAULT_TARGET)
    filtered_list = filter_list(result_list)
    enrich_list(filtered_list)
    screen_output(filtered_list)
    csv_output(filtered_list)

def scan_dns(target):
    # Use nmap3 library to perform DNS brute scan
    nmap = nmap3.Nmap()
    dns_results = nmap.nmap_dns_brute_script(target)
    return dns_results

def filter_list(scan_list):
    # Filter out IPv6 entries from the scan results
    pruned_list = []
    for scan_dict in scan_list:
        ip_address = scan_dict['address']
        if ':' not in ip_address:
            pruned_list.append(scan_dict)
    return pruned_list

def enrich_list(scan_list):
    # Enhance the scan results with geolocation data
    for scan_dict in scan_list:
        ip_address = scan_dict['address']
        geolocation_data = get_geolocation_data(ip_address)
        if geolocation_data:
            scan_dict.update(geolocation_data)

def get_geolocation_data(ip_address):
    # Use IP geolocation API to fetch geolocation data for an IP address
    url = f'https://ipapi.co/{ip_address}/json/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'Country': data.get('country_name', ''),
            'RegionName': data.get('region', ''),
            'City': data.get('city', ''),
            'Zipcode': data.get('postal', ''),
            'ISP': data.get('org', '')
        }
    else:
        return {}

def screen_output(scan_list):
    # Display the scan results on the screen
    print()
    header = f"{'IP':<25} {'DNS':<15} {'Country':<15} {'RegionName':<15} {'City':<15} {'Zipcode':<10} {'ISP':<20}"
    print(header)
    print('-' * len(header))
    for scan_dict in scan_list:
        ip_address = scan_dict['address']
        dns = scan_dict['hostname']
        country = scan_dict.get('Country', '')
        region = scan_dict.get('RegionName', '')
        city = scan_dict.get('City', '')
        zipcode = scan_dict.get('Zipcode', '')
        isp = scan_dict.get('ISP', '')
        row = f"{ip_address:<25} {dns:<15} {country:<15} {region:<15} {city:<15} {zipcode:<10} {isp:<20}"
        print(row)

def csv_output(scan_list):
    # Write the scan results to a CSV file
    filename = 'nmap4.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['DNS', 'IP', 'Country', 'RegionName', 'City', 'Zipcode', 'ISP']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        for scan_dict in scan_list:
            row_dict = {
                'DNS': scan_dict['hostname'],
                'IP': scan_dict['address'],
                'Country': scan_dict.get('Country', ''),
                'RegionName': scan_dict.get('RegionName', ''),
                'City': scan_dict.get('City', ''),
                'Zipcode': scan_dict.get('Zipcode', ''),
                'ISP': scan_dict.get('ISP', '')
            }
            csv_writer.writerow(row_dict)
    print(f'\nOutput saved in {filename}')

# Run the main function if the script is called directly
if __name__ == "__main__":
    main()

