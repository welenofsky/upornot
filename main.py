from __future__ import print_function

"""
This is my web server baby monitor, currently only
checks an IP for connectivity and changes title of
cmd window accordingly. It will also play a error
noise when the network goes down. 
"""
import argparse
import socket
import time
import pyglet
import os


# Beef of the program, checks for active internet connection.
def checkI(IP, port, isOnline, sound):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    isDownShown = 0
    localtime = time.asctime(time.localtime(time.time()))
    print("Connecting to External IP...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(10)
        s.connect((IP, port))
        s.shutdown(2)
        s.close()
        print("Online!\n")
        title_or_pass('ONLINE')
        if isOnline == "no":
            isOnline = "yes"
            logSys("inetstat",localtime,isOnline)
    except socket.error as e:
        print("Cannot connect to ")
        print(IP, " on port:", str(port))
        print(e)
        # Play exclamation sound when internet goes down
        sound.play()
        # Give some time to play one sound before playing another
        time.sleep(1)
        sound.play()
        title_or_pass('OFFLINE')
        time.sleep(5)
        if isOnline == "yes":
            isOnline = "no"
            logSys("inetstat",localtime)

    print("Last check:", localtime)


def title_or_pass(title):
    if os.name == 'nt':
        os.system('title ' + title)
    else:
        pass


def logSys(message, timestamp, isOnline):
    logfile = open('sysl.txt', 'a')
    if message == "inetstat":
        if isOnline == "yes":
            logfile.write("The host is online " + timestamp + '\n')
        else:
            logfile.write("The host is offline " + timestamp + '\n')
    elif message == "logboot":
        logfile.write("Boot Log - System Awake: " + timestamp + '\n')    
    logfile.closed


def main():
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

    sound = pyglet.resource.media('alert.wav', streaming=False)

    # initalize some more variables
    port = 80
    title_or_pass('Up or Not')
    isOnline = "no"

    logSys("logboot", (time.asctime(time.localtime(time.time()))), isOnline)
    while 1:
        checkI(IP, port, isOnline, sound)
        if not args.watch:
            exit(0)

        # Set to re-loop every 30 seconds if --watch passed
        time.sleep(30)


main()