"""
This is my web server baby monitor, currently only
checks an IP for connectivity and changes title of
cmd window accordingly. It will also play a error
noise when the network goes down. 
"""

import socket
import time
import winsound
from os import system

# External IP of server
dnsip = '127.0.0.1' #Left out IP, needs to be an IP of a webserver 
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
                        s.connect((dnsip, port))
                        s.shutdown(2)
                        s.close()
                        print("Online!\n")
                        if isDownShown == 1:
                                system('title ONLINE :)')
                                isDownShown = 0
                                break
                except socket.error as e:
                        print("Cannot connect to ")
                        print(dnsip, " on port:", str(port))
                        print(e)
                        #Play exclamation sound when internet goes down
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                        if isDownShown == 0:
                                system('title OFFLINE')
                        isDownShown = 1
                time.sleep(5);
while(1):
        checkI()
        # Set to re-loop every 30 seconds
        time.sleep(30)
