#!/usr/bin/python3
# This script takes the name of the file, finds all the servers that sent email and then writes out a csv file.
#Mrinalini-20230514:second version

import re
import csv
import sys

def extract_server_info(log_file):
    server_info = {}
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'connect from (\S+)\[([\d.]+)\]', line)
            if match:
                server_name = match.group(1)
                server_ip = match.group(2)
                if server_name not in server_info:
                    server_info[server_name] = server_ip
    return server_info

def write_to_csv(server_info, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Server Name', 'Server IP'])
        for server_name, server_ip in server_info.items():
            writer.writerow([server_name, server_ip])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python maillog.py <mail_log_file>')
        sys.exit(1)
    
    mail_log_file = sys.argv[1]
    server_info = extract_server_info(mail_log_file)
    output_csv_file = 'servers.csv'
    write_to_csv(server_info, output_csv_file)
    print(f'Successfully written all the server information to {output_csv_file}.')
