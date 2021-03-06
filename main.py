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

    print("Connecting to External IP...")

    localtime   = time.asctime(time.localtime(time.time()))
    s           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.settimeout(10)
        s.connect((IP, port))
        s.shutdown(2)
        s.close()
        print("Online!\n")
        title_or_pass('ONLINE')
        isOnline = True
        logSys("inetstat", localtime, isOnline)

    except socket.error as e:
        print("Cannot connect to ")
        print(IP, " on port:", str(port))
        print(e)
        # Play alert sound when internet goes down
        sound.play()
        # Give some time to play one sound before playing another
        time.sleep(1)
        sound.play()
        title_or_pass('OFFLINE')
        time.sleep(5)
        isOnline = False
        logSys("inetstat", localtime)

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
    title_or_pass('Up or Not')

    parser = argparse.ArgumentParser(description="Monitors a URL or IP address for connectivity on port 80.")
    parser.add_argument("-s","-server", type=str, help="The IP or Domain Name of the server to monitor")
    parser.add_argument("-d","-delay", type=int, help="Delay in seconds between checks")
    parser.add_argument("--watch", action="store_true", help="Watches server until application closes")
    args = parser.parse_args()

    server  = args.s
    delay   = args.d

    if delay != None and delay.isdigit():
        delay = int(delay)
    else:
        delay = 30

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
    port        = 80
    isOnline    = False
    sound       = pyglet.resource.media('alert.wav', streaming=False)

    logSys("logboot", (time.asctime(time.localtime(time.time()))), isOnline)

    while 1:
        checkI(IP, port, isOnline, sound)

        if not args.watch:
            exit(0)

        time.sleep(delay)


main()