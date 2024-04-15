#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function # keeping it real with python 3
from __future__ import unicode_literals
# from flask import Flask, render_template, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This project is to document switch port connectivity. This code will be run on Raspberry Pi to display switch information, leveraging LLDP and Python code to achieve this functionality.

import socket
#from socket import *
import subprocess
import fcntl
import struct
import commands
import os
import time
import datetime
import sys
import logging
import dbus
import paramiko
import inspect
import random
import psutil
import re

#Turn on debug by changing below value to 1.  Set to 0 to leave debug off.
debugStatus =1  # Debug ON
#debugStatus = 0  # Debug OFF

# #################################################################

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

getDateTime = datetime.datetime.now().strftime("%m-%d-%y %I:%M:%S%p")

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        #for handler in p.get_open_files() + p.connections():
        #    os.close(handler.fd)
    except Exception, e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

# This function is just basic for this DEMO but shows the power of the ANSI _Esc_ codes...
def locate(user_string="$VER: Locate_Demo.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU.", x=0, y=0):
    # Don't allow any user errors. Python's own error detection will check for
    # syntax and concatination, etc, etc, errors.
    x=int(x)
    y=int(y)
    if x>=255: x=255
    if y>=255: y=255
    if x<=0: x=0
    if y<=0: y=0
    HORIZ=str(x)
    VERT=str(y)
    # Plot the user_string at the starting at position HORIZ, VERT...
    print("\033["+VERT+";"+HORIZ+"f"+user_string)

#assign these variables so that we can reference them as colors later.
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
#following from Python cookbook, #475186

def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False

has_colours = has_colours(sys.stdout)

def printout(text, colour=WHITE):
        if has_colours:
            seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
            sys.stdout.write(seq)
        else:
            sys.stdout.write(text)

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s'.encode('utf-8'), ifname[:15].encode('utf-8'))
        )[20:24])
    except:
        #printout("No IP address detected.  No DHCP?  Setting to 127.0.0.1",MAGENTA)
        return '127.0.0.1'
    else:
        print("")

def getmac(iface):
    words = commands.getoutput("ifconfig " + iface).split()
    if "HWaddr" in words:
        return words[ words.index("HWaddr") + 1 ]
    else:
        return 'MAC Address Not Found!'

def getip(iface):
    words = commands.getoutput("ip addr show " + iface).split()
    if "inet" in words:
        return words[ words.index("inet") + 1 ]
    else:
        return words #'IP Address Not Found!'
'''
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether b8:27:eb:0d:55:b8 brd ff:ff:ff:ff:ff:ff
    inet 172.26.38.51/24 brd 172.26.38.255 scope global eth0
       valid_lft forever preferred_lft forever
'''
def getifstats():
    rx_bytes, tx_bytes = get_network_bytes('eth0')
    print ('%s bytes received' % rx_bytes)
    print ('%s bytes sent' % tx_bytes)

def get_network_bytes(interface):
    for line in open('/proc/net/dev', 'r'):
        if interface in line:
            data = line.split('%s:' % interface)[1].split()
            rx_bytes, tx_bytes = (data[0], data[8])
            return (rx_bytes, tx_bytes)

def restart():
    command = "/usr/bin/sudo /sbin/shutdown now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)

def changeterm():
    command = "/usr/bin/sudo setfont /usr/share/consolefonts/Uni2-Terminus16"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)

def searchingStatus():
    x=0
    y=5
    char=""
    locate(char, x, y)

def ifStatus():
    x=0
    y=11
    char=""
    locate(char, x, y)

def getlldpcli():
    global outputSysName
    global outputPortDescr
    global outputVLAN
    global outputVoice
    global lldpSysName_status
    global lldpPortDescr_status
    global lldpVLAN_status
    global lldpVoice_status

    lldpSysName = subprocess.Popen("lldpcli show neighbors summary | grep SysName | awk '{print $2}'", stdout=subprocess.PIPE, shell=True)
    lldpPortDescr = subprocess.Popen("lldpcli show neighbors summary | grep PortID: | awk '{print $3}'", stdout=subprocess.PIPE, shell=True)
    lldpVLAN = subprocess.Popen("lldpcli show neighbors detail | grep VLAN | awk '{print $2}' | tr -d , | uniq -u", stdout=subprocess.PIPE, shell=True)
    lldpVoice = subprocess.Popen("lldpcli show neighbors detail | grep voice | awk '{print $2}' | tr -d , | uniq -u", stdout=subprocess.PIPE, shell=True)
    ## Talk with lldpcli command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
    ## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    ## or None, if no data should be sent to the child.
    (outputSysName, err) = lldpSysName.communicate()
    (outputPortDescr, err) = lldpPortDescr.communicate()
    (outputVLAN, err) = lldpVLAN.communicate()
    (outputVoice, err) = lldpVoice.communicate()
    ## Wait for date to terminate. Get return returncode ##
    lldpSysName_status = lldpSysName.wait()
    lldpPortDescr_status = lldpPortDescr.wait()
    lldpVLAN_status = lldpVLAN.wait()
    lldpVoice_status = lldpVoice.wait()

    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  outputSysName.rstrip() = ",outputSysName," and type is: ",type(outputSysName))
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  outputVLAN.rstrip() = ",outputVLAN," and type is: ",type(outputVLAN))
    outputVLAN = outputVLAN.rstrip() # remove linefeed at the end
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: outputVoice output and type : ", outputVoice, type(outputVoice))
    outputVoice = outputVoice.strip()
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: outputVoice output and type : ", outputVoice, type(outputVoice))
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  before outputVLAN.replace('\n', ' ') = ",outputVLAN," and type is: ",type(outputVLAN))
    outputVLAN = outputVLAN.replace('\n', ' ') # remove linefeed in the middle and replace with space
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  before outputVLAN.encode('ascii') = ",outputVLAN," and type is: ",type(outputVLAN))
    outputVLAN = outputVLAN.encode('ascii') # because unicode is hard to work with
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  before outputVLAN.strip() = ",outputVLAN," and type is: ",type(outputVLAN))
    outputVLAN = outputVLAN.strip() # remove whitespace at the beginning and end.
    #outputVoice = outputVoice.replace("\n", ",")
    #outputVLAN = outputVLAN.split(',') # makes it a lists
    #outputVoice = outputVoice.split(',')
    #VoiceVLAN = set(outputVLAN).intersection(outputVoice) # find the matching VLAN
    #outputVLAN = outputVLAN.replace(outputVoice,"")  #This doesn't works
    #kickoff = [item.replace("'", "") for item in kickoff]   #Example on how to make it works
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: outputSysName output : ", outputSysName)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: lldpSysName_status exit status/return code : ", lldpSysName_status)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: outputPortDescr output : ", outputPortDescr)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: lldpPortDescr_status exit status/return code : ", lldpPortDescr_status)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: outputVLAN output and type : ", outputVLAN, type(outputVLAN))
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: lldpVLAN_status exit status/return code : ", lldpVLAN_status)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: outputVoice output and type : ", outputVoice, type(outputVoice))
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: If outputVoice is empty, make it 0")
    if not outputVoice:
        outputVoice = "0"
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: UPDATED:  outputVoice output and type : ", outputVoice, type(outputVoice))
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (": DEBUG: lldpVoice_status exit status/return code : ", lldpVoice_status)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  before removing voice vlan from outputVLAN = ",outputVLAN," and type is: ",type(outputVLAN))
    #outputVLAN = [item.replace(outputVoice, "") for item in outputVLAN]
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  if outputVoice in outputVLAN:outputVLAN.remove(outputVoice) where outputVoice is ",int(outputVoice))
    #if int(outputVoice) in outputVLAN:
    #    outputVLAN.remove(int(outputVoice))
    outputVLAN = outputVLAN.replace(outputVoice,'')
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  before converting outputVLAN from unicode to ascii = ",outputVLAN," and type is: ",type(outputVLAN))
    outputVLAN = outputVLAN.encode('ascii')
    outputVLAN = outputVLAN.strip() # have to do this again because it puts whitespace around the value for some stupid reason that I'm too stupid to understand.
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  after converting outputVLAN from unicode to ascii = ",outputVLAN," and type is: ",type(outputVLAN))

    #sep = outputVoice
    #outputVLAN = outputVLAN.split(sep, 1)[0]
    #outputVLAN = [item.replace(outputVoice, "") for item in outputVLAN]
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  after removing voice vlan from outputVLAN = ",outputVLAN," and type is: ",type(outputVLAN))

    if outputSysName: # got a non-empty string
        printout("\n\nContinuing ...",GREEN)
    else:
        printout("\n\nNo LLDP detected... restarting script...",MAGENTA)
        #printout("\n\nNo outputSysName... restarting script...",MAGENTA)
        #print("LLDP not working... outputSysName value is {}".format(outputSysName))
        restart_program()

def netpi():
    try:
        changeterm()
        global macaddress # need to make this global or else this function won't know what it is
        switchport = outputPortDescr
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  switchport = {}".format(switchport))
        global parsePort
        parsePort = switchport.split('/') # ge-0/0/40.0
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  parsePort = {}".format(parsePort))
        splitSwitch = parsePort[0].split('-') #ge-0
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  splitSwitch = {}".format(splitSwitch))
        parseSwitchNumber = splitSwitch[1].encode('utf-8')
        parsePort = parsePort[2].encode('utf-8')
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  parsePort = {}".format(parsePort))
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  parseSwitchNumber = {}".format(parseSwitchNumber))
        #Take the result of parsePort and remove the .0 from it
        justPort = parsePort.split(".")
        justPort = justPort[0].encode('utf-8')
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  justPort = {}".format(justPort))
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  after justPort... hitting the return with switchName and switchport...")
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  **********************************************************************************")

        if debugStatus == 0: searchingStatus() # locate cursor and execute function to print status
        #time.sleep(3)
        #while remote_conn.recv_ready():
        #    output = remote_conn.recv(1000)
        switchName = outputSysName
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: switchName = ')
        if debugStatus == 1: print (switchName)
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: switchport = ')
        if debugStatus == 1: print (switchport)
        if debugStatus == 0: printout ("\n + Parsing Data...                                   ",WHITE)
        if debugStatus == 0: searchingStatus() # locate cursor and execute function to print status
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Start script.  DEBUG is on.')

        #Site, subnets and devices to test
        siteName=["Austin","Bay Area","Boise","Denver","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","DR","Austin","Bay Area","Boise","Denver","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","Home/Private","NO DHCP"]
        siteSubnet=["172.23.28.","172.23.112.","172.23.40.","172.23.50.","172.23.120.","172.23.62.","172.23.72.","172.23.82.","172.23.92.","172.23.96.","172.23.100.","172.23.180.","172.23.130.","172.23.116.","172.32.14.","10.23.28.","10.23.112.","10.23.40.","10.23.50.","10.23.120.","10.23.62.","10.23.72.","10.23.82.","10.23.92.","10.23.96.","10.23.100.","10.23.180.","10.23.124.","10.23.116.","192.168.1."]
        siteDeviceName=["Adtran 1335 Router","FortiGate Firewall (inside)","Adtran 1238 Switch A","Adtran 1238 Switch B","LifeSize Codec"]
        siteDeviceIP=["1","2","3","4","99"]

        #HQ devices and vlans
        hqDeviceName=["HQ Core .5","HQ Core .14","HQ VoIP","HQ VTC","Acano Primary Server Inside (admin)","Acano Primary Server Inside (Port A)","Acano Secondary Server Inside (admin)","Acano Secondary Server Inside (Port A)","LifeSize UVC Transit Client (Inside)","LifeSize UFC Transit Server - Signaling (VidNet)","LifeSize UFC Transit Server - Media (VidNet)"]
        hqDeviceIP=["172.23.5.1","172.23.14.1","172.23.8.1","172.20.1.1","172.20.1.31","172.20.1.30","172.20.1.33","172.20.1.32","172.20.1.20","199.249.210.10","199.249.210.11"]
        hqVLANNumber=["50","8","5","14","17","240","242","210","1020","173","200","2512","2532","2514","2534","2516","2536","2518","2538","2520","2540","2612","2632","2614","2634","2616","2636","2618","2638","2620","2640","2712","2732","2714","2734","2716","2736","2718","2738","2720","2740","2812","2832","2814","2834","2816","2836","2818","2838","2820","2840","2910","2920","2940","2950","200","28","112","40","50","120","62","72","82","92","96","100","180","124","116","35","10","18","19","22","23","1010"]
        hqVLANName=["VTCCore","VoIPCore","Transport","ServersProd","ServersNet","ServersLab","TestLab","VidNet","Comcast Private","Comcast Public","HQ T1 Lab","User/Printer A (2512)","User/Printer B (2532)","Phone A (2514)","Phone B (2534)","AV/VTC A (2516)","AV/VTC B (2536)","TS Infrastructure A (2518)","TS Infrastructure B (2538)","TS Bus Sol A (2520)","TS Bus Sol B (2540)","User/Printer A (2612)","User/Printer B (2632)","Phone A (2614)","Phone B (2634)","AV/VTC A (2616)","AV/VTC B (2636)","TS Inf A (2618)","TS Inf B (2638)","TS Bus Sol A (2620)","TS Bus Sol B (2640)","User/Printer A (2712)","User/Printer B (2732)","Phone A (2714)","Phone B (2734)","AV/VTC A (2716)","AV/VTC B (2736)","TS Infrastructure A (2718)","TS Infrastructure B (2738)","TS Bus Sol A (2720)","TS Bus Sol B (2740)","User/Printer A (2812)","User/Printer B (2832)","Phone A (2814)","Phone B (2834)","AV/VTC A (2816)","AV/VTC B (2836)","TS Infrastructure A (2818)","TS Infrastructure B (2838)","TS Bus Sol A (2820)","TS Bus Sol B (2840)","WiFi CFPcorp (2910)","WiFi CFPmobile (2920)","WiFi CFPguest (2940)","WiFi Crestron (2950)","T1 Lab (200)","Austin","Bay Area","Boise","Denver","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","DR","Kid Lab","Aruba IAP","CFPstaff","VoIP","Prod LAN"]
        hqVLANSubnet=["172.20.1.","172.23.8.","172.23.5.","172.23.14.","172.23.17.","172.23.240.","172.23.242.","199.249.210.","10.20.30.","1.2.3.4","172.23.200.","172.25.12.","172.25.32.","172.25.14.","172.25.34.","172.25.16.","172.25.36.","172.25.18.","172.25.38.","172.25.20.","172.25.40.","172.26.12.","172.26.32.","172.26.14.","172.26.34.","172.26.16.","172.26.36.","172.26.18.","172.26.38.","172.26.20.","172.26.40.","172.27.12.","172.27.32.","172.27.14.","172.27.34.","172.27.16.","172.27.36.","172.27.18.","172.27.38.","172.27.20.","172.27.40.","172.28.12.","172.28.32.","172.28.14.","172.28.34.","172.28.16.","172.28.36.","172.28.18.","172.28.38.","172.28.20.","172.28.40.","172.29.10.","172.29.20.","172.29.40.","172.29.50.","10.23.200.","172.23.200.","10.20.30.","172.23.28.","172.23.112.","172.23.40.","172.23.50.","172.23.55.","172.23.120.","172.23.62.","172.23.72.","172.23.82.","172.23.92.","172.23.96.","172.23.100.","172.23.180.","172.23.124.","172.23.116.","172.32.14.","10.23.28.","10.23.112.","10.23.40.","10.23.50.","10.23.120.","10.23.62.","10.23.72.","10.23.82.","10.23.92.","10.23.96.","10.23.100.","10.23.180.","10.23.124.","10.23.116.","192.168.1.","127.0.0."]
        hqVLANFloor=["Core","Core","Core","Core","Core","Core","Core","Internet Sw","Internet Sw","WTF","T1 Lab Adtran","25A","25B","25A","25B","25A","25B","25A","25B","25A","25B","26A","26B","26A","26B","26A","26B","26A","26B","26A","26B","27A","27B","27A","27B","27A","27B","27A","27B","27A","27B","28A","28B","28A","28B","28A","28B","28A","28B","28A","28B","WiFi","WiFi","WiFi","WiFi","26 (T1 Lab)","26 (T1 Lab)","Comcast","Austin","Bay Area","Boise","Denver","Atlanta","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","DR","Austin","Bay Area","Boise","Denver","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","Home/Private","NO DHCP"]
        hqSwitchFloor=["Core","Core","Core","Core","Core","Core","Core","Internet Sw","Internet Sw","WTF","T1 Lab Adtran","25-A","25-B","25-A","25-B","25-A","25-B","25-A","25-B","25-A","25-B","26-A","26-B","26-A","26-B","26-A","26-B","26-A","26-B","26-A","26-B","27-A","27-B","27-A","27-B","27-A","27-B","27-A","27-B","27-A","27-B","28-A","28-B","28-A","28-B","28-A","28-B","28-A","28-B","28-A","28-B","WiFi","WiFi","WiFi","WiFi","T1 Lab Adtran","T1 Lab Adtran","Internet Sw","Austin","Bay Area","Boise","Denver","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","DR","Austin","Bay Area","Boise","Denver","LA County","New York","Phoenix","Sacramento","San Antonio","San Diego","Seattle","Tucson","Wash DC","Yakima","Home/Private","NO DHCP"]
        switchType=["Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Adtran","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Juniper","Aruba","Aruba","Aruba","Aruba","Adtran","Adtran","Juniper","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Juniper","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Adtran","Juniper","Juniper"]

        global ipaddress
        ipaddress = get_ip_address('eth0')
        macaddress = getmac('eth0')
        ipsubnetlist = ipaddress.split(".")
        ipsubnet = "".join([ipsubnetlist[0].encode('utf-8'),".".encode('utf-8'),ipsubnetlist[1].encode('utf-8'),".".encode('utf-8'),ipsubnetlist[2].encode('utf-8'),".".encode('utf-8'),"0".encode('utf-8')])
        ipSubnetSearchValue = "".join([ipsubnetlist[0].encode('utf-8'),".".encode('utf-8'),ipsubnetlist[1].encode('utf-8'),".".encode('utf-8'),ipsubnetlist[2].encode('utf-8'),".".encode('utf-8')])

        #Clear the screen!
        if debugStatus == 0: os.system('clear')
        if debugStatus == 0: os.system('setterm -cursor off')

        #When using "printout", you need to specify a color which is one of these:
        #BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

        printout ("+======================================+\n", RED)
        printout ("NetPi Test Results " + getDateTime + ".\n",MAGENTA)
        printout ("+======================================+\n", RED)
        if ipaddress == "127.0.0.1":
            printout("No DHCP or cable unplugged!",YELLOW)
        else:
            printout ("IP Address:  ",GREEN)
            printout ("{}".format(ipaddress),WHITE)
        printout ("\nMAC Address: ",GREEN)
        printout ("{}".format(macaddress),YELLOW)

        #Find out the index for the list by matching the ip subnet. We can use the same index for other lists.
        getindex = hqVLANSubnet.index(ipSubnetSearchValue.encode('utf-8'))
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned getindex = {}'.format(getindex) )
        if debugStatus == 1: time.sleep(2)
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  after removing voice vlan from outputVLAN = ",outputVLAN," and type is: ",type(outputVLAN))

        try:
            vlanindex = hqVLANNumber.index(outputVLAN)
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned vlanindex = {}'.format(vlanindex) )
            outputVLAN_name = hqVLANName[vlanindex]
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned outputVLAN_name = {}'.format(outputVLAN_name) )
        except ValueError:
            outputVLAN_name = 'Unknown'
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  after removing voice vlan from outputVLAN = ",outputVLAN," and type is: ",type(outputVLAN))
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned outputVLAN_name = {}'.format(outputVLAN_name) )
            if debugStatus == 1: time.sleep(2)
        try:
            voiceindex = hqVLANNumber.index(outputVoice)
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned voiceindex = {}'.format(voiceindex) )
            outputVoice_name = hqVLANName[voiceindex]
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned outputVoice_name = {}'.format(outputVoice_name) )
        except ValueError:
            outputVoice_name = 'Unknown'
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned outputVoice_name = {}'.format(outputVoice_name) )
            if debugStatus == 1: time.sleep(2)

        '''
        When using print with lists, use format so that you don't see spaces after each value.
        Basic usage of the str.format() method looks like this:
        >>> print('We are the {} who say "{}!"'.format('knights', 'Ni'))
        We are the knights who say "Ni!"
        The brackets and characters within them (called format fields) are replaced with the objects passed into the str.format() method.
        A number in the brackets can be used to refer to the position of the object passed into the str.format() method.
        '''

        #printout ("\nVLAN Subnet: ",GREEN)
        #printout ("{}0 255.255.255.0".format(hqVLANSubnet[getindex]),YELLOW)
        #printout ("\nVLAN Name/#: ",GREEN)

        if "169.254" in ipaddress:
            printout("\n\nNo DHCP... restarting script...",MAGENTA)
            print("This address should be temporary...")
            #os.system('/usr/local/share/kupi/flask/netdiscover.sh')
            #sys.exit()
            #sudo "/usr/sbin/netdiscover -l /home/jkujath/netdiscover_list.txt -S -f -P"
            #restart_program()

        if "192.168.1." in ipaddress:
            printout("\n\nIs this a home network??",MAGENTA)
            #os.system('/usr/local/share/kupi/flask/netdiscover.sh')
            #sys.exit()
            #sudo "/usr/sbin/netdiscover -l /home/jkujath/netdiscover_list.txt -S -f -P"
            #restart_program()

        if ipaddress == "127.0.0.1":
            printout("\n\nNo DHCP... ",MAGENTA)
            #os.system('/usr/local/share/kupi/flask/netdiscover.sh')
            #sys.exit()
            #sudo "/usr/sbin/netdiscover -l /home/jkujath/netdiscover_list.txt -S -f -P"
            #restart_program()

        if debugStatus == 0: searchingStatus() # locate cursor and execute function to print status

        parsePortSwitch = 'Unknown'
        parsePortPort = 'Unknown'

        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: getindex = ')
        #print (getindex)
        #if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: hqSwitchFloor[getindex] = ' + hqSwitchFloor[getindex])
        #if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: switchType[getindex] = ' + switchType[getindex])
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned switchName = {}'.format(switchName) )

        newSwitchPort = ''
        #               ###################################
        printout ("\n / Searching for switch port...                   ",WHITE)
        if debugStatus == 0: searchingStatus() # locate cursor and execute function to print status
        # switchport was created as a tuple where each indexed item was a single letter.  That sucks.  So below I put it back into 1 single string
        for i in switchport:
            if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Returned switchport as tuple = ', i)
            newSwitchPort = newSwitchPort + i

        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: Switchport is now = {}'.format(switchport) )
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: newSwitchPort is now = ')
        if debugStatus == 1: print (newSwitchPort)

        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: newSwitchPort is not an uplink...')
        #               ###################################
        printout ("\n \ Port is not uplink...                               ",YELLOW)
        if debugStatus == 0: searchingStatus() # locate cursor and execute function to print status
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: **********************************************************')
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: newSwitchPort IS on this switch!  Stop everything!')
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: **********************************************************')
        #               ###################################
        printout ("\n *** Found the port!                                    ",CYAN)
        if debugStatus == 0: searchingStatus() # locate cursor and execute function to print status
        #Format a dataJack variable to match how the data jacks are labeled at HQ.
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print (': DEBUG: getindex = {}'.format(getindex) )
        if debugStatus == 1: time.sleep(2)
        dataJack = hqSwitchFloor[getindex] + newSwitchPort[3] + '-' + justPort
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  dataJack = {}".format(dataJack))
        newSwitchPort = switchport
        # Print the results, depending on switch type
        #printout ("\nVLAN Floor:  ",GREEN)
        #printout ("{}".format(hqVLANFloor[getindex]),YELLOW)
        #printout ("    ",YELLOW)
        printout ("VLAN(s):     ",GREEN)
        printout ("{}".format(outputVLAN),CYAN)
        printout (" [",WHITE)
        printout ("{}".format(outputVLAN_name),YELLOW)
        printout ("] ",WHITE)
        printout ("\nVoice VLAN:  ",GREEN)
        printout ("{}".format(outputVoice),CYAN)
        printout (" [",WHITE)
        printout ("{}".format(outputVoice_name),YELLOW)
        printout ("] ",WHITE)
        printout ("\nSwitch IP:   ",GREEN)
        printout ("{}".format(hqVLANSubnet[getindex]),YELLOW)
        printout ("1",YELLOW)
        printout ("\nSwitch Name: ",GREEN)
        printout ("{}".format(outputSysName),YELLOW)
        printout ("Switch Port: ",GREEN)
        printout ("{}".format(switchport),CYAN)
        printout ("Data Jack:   ",GREEN)
        printout ("{}".format(dataJack),WHITE)
        switchtype = switchType[getindex]
        switchName = outputSysName #because
        switchip = hqVLANSubnet[getindex] +'1'
        vlansubnet = hqVLANSubnet[getindex] + '0 255.255.255.0'
        vlanname = hqVLANName[getindex]
        vlannumber = hqVLANNumber[getindex]
        vlanfloor = hqVLANFloor[getindex]
        fullswitchport = switchport
        interfacetoggle = 0
        parsedswitchport = "Switch " + hqSwitchFloor[getindex] + parsePortSwitch + "-" + parsePortPort
        #
        if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  parsedswitchport = {}".format(parsedswitchport))


        if debugStatus == 1: print ('\n') ; print (': DEBUG: About to set the first ifstatus variable... ')
        with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
            ifstatus = ifoper.readline()
            ifstatus = ifstatus.strip()
            if debugStatus == 1: print ('\n') ; print ('DEBUG: Just set ifstatus to: {}'.format(ifstatus))
            if debugStatus == 1: print ('\n') ; print ('DEBUG: ifstatus type is: {}'.format(type(ifstatus)))
            if debugStatus == 1: print ('\n') ; print ('DEBUG: ifstatus length is: {}'.format(len(ifstatus)))

        #Get a specific interface by name
        file_path = '/usr/local/share/kupi/flask/if.up'

        #print ('DEBUG: file_path = {}'.format(file_path))
        #print ('DEBUG: ifstatus = {}'.format(ifstatus))

        if ifstatus == 'up':
            if debugStatus == 1: print ('DEBUG: Inside if ifstatus is '+ifstatus)
            if interfacetoggle == 1:
                interfacetoggle = 0
                if debugStatus == 1: print ('DEBUG: Interface came back up... interfacetoggle = 1' )
                if debugStatus == 1: print ('DEBUG: Resetting interfacetoggle and restarting program ...' )
                time.sleep(5)
                print ('Restarting program ...' )
                restart_program()
            while ifstatus =='up':
                #print ('DEBUG: file_path DOES exist...')
                #interface is up... check every second...
                with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
                    ifstatus = ifoper.readline()
                    ifstatus = ifstatus.strip()
                printout ("\nNetwork Interface is ", WHITE)
                printout ("UP    ",GREEN)
                waitsymbol = ['| ', '/ ', '- ', '\\ ', '* ']
                printout (random.choice(waitsymbol),YELLOW)
                if debugStatus == 0: ifStatus() # locate cursor and execute function to print status
                time.sleep(1)

        while ifstatus != "up":
            if debugStatus == 1: print ('DEBUG: while loop when ifstatus is not up:  ifstatus='+ifstatus)
            #interface is down... wait for it to come back up...
            interfacetoggle = 1
            if debugStatus == 1: print ('DEBUG: interfacetoggle = 1...')
            with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
                ifstatus = ifoper.readline()
                ifstatus = ifstatus.strip()
                if debugStatus == 1: print ('DEBUG: with open is reading the interface status:  ifstatus='+ifstatus)
            printout ("\nNetwork Interface is ", WHITE)
            printout ("DOWN  ",MAGENTA)
            waitsymbol = ['|', '/', '-', '\\', '*']
            printout (random.choice(waitsymbol),YELLOW)
            if debugStatus == 0: ifStatus() # locate cursor and execute function to print status
            time.sleep(1)

        if ifstatus == 'down':
            if debugStatus == 1: print ('DEBUG: if ifstatus is DOWN...')
            interfacetoggle = 1
            if debugStatus == 1: print ('DEBUG: interfacetoggle = 1...')
            if debugStatus == 1: time.sleep(2)
            while ifstatus != "down":
        #        if debugStatus == 1: print ('DEBUG: while file_path DOES EXIST!')
                with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
                    ifstatus = ifoper.readline()
                    ifstatus = ifstatus.strip()
                #restart the script
                restart_program()
        restart_program()
    except NameError as e:
        print(lineno())
        print (e)
        print (sys.exc_type)
        time.sleep(2)
        print ("\nRestarting...")
        restart_program()
        pass
    except IOError as e:
        print(lineno())
        print ("\n\nI/O error({0}): {1}".format(e.errno, e.strerror))
        time.sleep(2)
        print ("\nRestarting...")
        restart_program()
        pass
    except IndexError as e:
        print(lineno())
        print ("\n\nIndex Error:", sys.exc_info()[0])
        print (sys.exc_type)
        print ("\nRestarting...")
        restart_program()
    except:
        print(lineno())
        print ("\n\nUnexpected error:", sys.exc_info()[0])
        print (sys.exc_type)
        time.sleep(2)
        print ("\nRestarting...")
        restart_program()
        raise
try:
    global parseSwitchNumber
    global justPort
    global ipaddress
    global getindex
    parseSwitchNumber = 'Unknown'
    justPort = 'Unknown'
    getlldpcli()
    ##time.sleep(2) #takes it a bit of time to get the IP
    netpi()
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  **********************************************************************************")
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  ************ END TRY *************")
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  **********************************************************************************")
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  ----------------------------------------------------------------------------------")
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print ("\nDEBUG:  VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
except IOError as e:
    print(lineno())
    print ("\n\nI/O error({0}): {1}".format(e.errno, e.strerror))
    time.sleep(2)
    print ("\nRestarting...")
    restart_program()
except ValueError:
    print(lineno())
    printout ("\n\nCould not convert data to an integer...\nRESTARTING!",MAGENTA)
    print ("\n\nValueError:", sys.exc_info()[0])
    print (sys.exc_type)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (lineno(),"\nDEBUG:  outputVLAN = ",*outputVLAN)
    if debugStatus == 1: print ('\n') ; print(lineno()) ; print (lineno(),": DEBUG: outputVLAN output and type : ", outputVLAN, type(outputVLAN))
    time.sleep(2)
    print ("\nRestarting...")
    restart_program()
    pass #this could be bad?
    #restart_program()
except IndexError as e:
    print(lineno())
    print ("\n\nIndex Error:", sys.exc_info()[0])
    print (sys.exc_type)
    print ("\nRestarting...")
    restart_program()
except:
    print(lineno())
    print ("\n\nUnexpected error:", sys.exc_info()[0])
    print (sys.exc_type)
    time.sleep(2)
    print ("\nRestarting...")
    restart_program()
    raise
