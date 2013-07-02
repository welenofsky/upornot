"""
This is my web server baby monitor, currently only
checks an IP for connectivity and changes title of
cmd window accordingly. It will also play a error
noise when the network goes down. 
"""
import argparse
import socket
import time
import winsound
from os import system

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument("-s","-server", help="The IP or Domain Name of the server to monitor")
parser.add_argument("--watch", action="store_true", help="Watches server until application closes")
args = parser.parse_args()

# 
server = args.s

if server == None:
    print("No IP or Host provided, exiting...")
    exit(0)

try:
    IP = socket.gethostbyname(server)
except socket.gaierror:
    print("Incorrect server name or IP provided, exiting...")
    exit(0)
except:
    print("Unknown error has occured, check credentials and try again")
    exit(0)

# initalize some more variables
port = 80
system('title Up or Not')

# Beef of the program, checks for active internet connection.
def checkI():
	isDownShown = 0
	while 1:
                localtime = time.asctime(time.localtime(time.time()))
                print(localtime)
                print("Connecting to External IP...")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                        s.connect((IP, port))
                        s.shutdown(2)
                        s.close()
                        print("Online!\n")
                        if isDownShown == 1:
                                system('title ONLINE :)')
                                isDownShown = 0
                                break
                except socket.error as e:
                        print("Cannot connect to ")
                        print(IP, " on port:", str(port))
                        print(e)
                        #Play exclamation sound when internet goes down
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                        if isDownShown == 0:
                                system('title OFFLINE')
                        isDownShown = 1
                if not args.watch:
                    exit(0)
                time.sleep(5);
while(1):
        checkI()
        # Set to re-loop every 30 seconds
        time.sleep(30)