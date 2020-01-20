#!/usr/bin/env python
import socket
import subprocess
import sys
import argparse
from datetime import datetime
from termcolor import colored

def main(argv):
    # Set commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1', help='Print pscan version number')
    parser.add_argument('-pr', type=int, default=1025, help='Enter port range')
    parser.add_argument('-to', type=int, default=10, help='Enter Timeout in seconds')
    args = parser.parse_args()
    portRange = args.pr
    timeOut = args.to

    # Clear the screen
    subprocess.call('clear', shell=True)

    # Remote host input
    remoteServer    = input("Enter a host to scan: ")
    # Translate host name to IPV4 address
    remoteServerIP  = socket.gethostbyname(remoteServer)

    # Print a banner with information on which host we are about to scan
    print ("-" * 60)
    print ("Please wait, scanning remote host", remoteServerIP)
    print ("-" * 60)

    # Check what time the scan started
    t1 = datetime.now()

    # Using the range function to specify ports (it will scans all ports between 1 to 1024 by default)
    try:
        for port in range(1,portRange):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeOut)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print (colored("Port {:<10d}=>{:>12s}".format(port, 'Open'), 'green'))
            else:
                print (colored("Port {:<10d}=>{:>12s}".format(port, 'Closed'), 'red'))
            sock.close()
    # Added escape message on keyboard interrupt when using CTRL+C
    except KeyboardInterrupt:
        print ("Exiting pscan")
        sys.exit()
    # We also put in some error handling for catching errors
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print ("Couldn't connect to server")
        sys.exit()

    # Checking what time the scan completed
    t2 = datetime.now()

    # Calculates the difference in time, to see how long it took to run the script
    total =  t2 - t1

    # Print scan time information to screen
    print ('Scanning Completed in: ', total)

if __name__ == "__main__":
    main(sys.argv[1:])