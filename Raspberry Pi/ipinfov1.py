
# install this for the lldpcli. sudo apt-get install lldpd

import subprocess
import os
import time
import datetime
import sys
import logging
import psutil



def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())

    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)
    
       
    
def getlldpcli():
    global outputSysName
    global outputPortDescr
    global outputSysDescr
    global outputmgmtip
    global lldpSysName_status
    global lldpSysDescr_status
    global lldpPortDescr_status
    global lldpmpmtip_status


    ## The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
    ## subprocess.popen Execute a child program in a new process
    
    lldpSysName = subprocess.Popen("lldpcli show neighbors  | grep SysName | awk '{print $2}'", stdout=subprocess.PIPE, shell=True)
    lldpPortDescr = subprocess.Popen("lldpcli show neighbors  | grep PortDescr: | awk '{print $2,$3}'", stdout=subprocess.PIPE, shell=True)
    lldpSysDescr = subprocess.Popen("lldpcli show neighbors  | grep SysDescr: | awk '{print $2,$3,$4}'", stdout=subprocess.PIPE, shell=True)
    lldpmgmtip = subprocess.Popen("lldpcli show neighbors  | grep MgmtIP: | awk '{print $2}'", stdout=subprocess.PIPE, shell=True)
    
   

    ## Popen.communicate Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate and set the returncode attribute.
    ## communicate() returns a tuple (stdout_data, stderr_data). The data will be strings if streams were opened in text mode; otherwise, bytes.
    

    (outputSysName, err) = lldpSysName.communicate()
    (outputPortDescr, err) = lldpPortDescr.communicate()
    (outputSysDescr, err) = lldpSysDescr.communicate()
    (outputmgmtip, err) = lldpmgmtip.communicate()

    ## Wait for child process to terminate. Get return returncode ##
    lldpSysName_status = lldpSysName.wait()
    lldpPortDescr_status = lldpPortDescr.wait()
    lldpSysDescr_status = lldpSysDescr.wait()
    lldpmpmtip_status = lldpmgmtip.wait()


    print ("SwitchName = ",outputSysName.decode("utf-8"))
    print ("Port Description = " ,outputPortDescr.decode("utf-8"))
    print ("System Description = " ,outputSysDescr.decode("utf-8"))
    print ("Switch ManagementIP = " ,outputmgmtip.decode("utf-8"))

        
     ## raspberrypi eth0 status check /sys/class/net/eth0/operstate if up call the  getlldpcli function or restart the program  
        
try:        
        
   
    ifstatus = ''
    
    with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
        ifstatus = ifoper.readline()
        ifstatus = ifstatus.strip()
    
    
    while ifstatus == 'up':
        with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
            ifstatus = ifoper.readline()
            ifstatus = ifstatus.strip()
                
            print ("Eth0 Status = ",ifstatus)
            
            getlldpcli()
            time.sleep(10)
            #restart_program()
            
    while ifstatus != "up":

        with open ("/sys/class/net/eth0/operstate", "r") as ifoper:
            ifstatus = ifoper.readline()
            ifstatus = ifstatus.strip()
                   
            print ("Eth0 Status = ",ifstatus)
            time.sleep(5)
            
    print("Eth0 status changed. Restarting the Program")
    restart_program()
            
            
    
except:
    time.sleep(2)
    print ("\nRestarting...")
    restart_program()
    raise

#getifstats()