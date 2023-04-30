#!/usr/bin/python3
#This script returns the information about the machine it is running on.
#Mrinalini-20230429:second version

# This is importing two python modules
import socket
import os

# This will get the hostname of the machine
hostname = socket.gethostname()

# This will get the number of CPUs on the machine and stores it in the variable, cpu_count
cpus = os.cpu_count()

# This will get the RAM value in GB, coverts it from bytes to gigabytes
ram = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.0 ** 3))

# This will Get OS type and version
if os.path.exists('/etc/os-release'):
    with open('/etc/os-release', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('NAME='):
                ostype = line.split('=')[1].strip().strip('"')
            elif line.startswith('VERSION_ID='):
                osversion = line.split('=')[1].strip().strip('"')
else:
    ostype = os.name
    osversion = os.sys.platform

# This will get the number of disks
disks = len([d for d in os.listdir('/sys/block') if d.startswith('sd') and not os.path.islink(f'/sys/block/{d}/loop/backing_file')])

# This will get the IP and MAC address
ifconfig = os.popen('ip addr show').read()
if 'inet ' in ifconfig:
    ipaddr = ifconfig.split('inet ')[1].split('/')[0].strip()
else:
    ipaddr = 'unknown'
if 'ether ' in ifconfig:
    macaddr = ifconfig.split('ether ')[1].split(' ')[0].strip()
else:
    macaddr = 'unknown'

# This will print all the information
print(f"Hostname: {hostname}")
print(f"CPU (count): {cpus}")
print(f"RAM (GB): {ram}")
print(f"OSType: {ostype}")
print(f"OSVersion: {osversion}")
print(f"Disks (Count): {disks}")
print(f"IP of eth0: {ipaddr}")
print(f"MAC of eth0: {macaddr}")

