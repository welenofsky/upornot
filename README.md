upornot
=======

Upornot watches your or someone elses web server. It can be used as an uptime baby monitor or
a internet verification utility. UporNot is written in python 3 and does not work in python 2.7.

FLAGS and OPTIONS:
to watch a server you must pass a servers domain name or IP address with the -s option you may also pass 
the --watch flag to monitor your ability to connect to a server indefinitely. You can see an example below. 

[Justin@FedoraBox]$ python main.py -server google.com --watch

In this command the -server flag specifies the IP/Domain name of the computer that you would like to monitor. The --watch flag tells upornot to watch server indefinitely or until you kill the process.

If you are able to connect to the remote server a local time stamp and status will be printed to the console to confirm
that it connected alright. If it is not able to connect it will play a Windows notification sound to alert you that 
you have been disconnected or the server is offline. It will also change the title of the window to reflect the current status of the server. This utility does not 100% verify a servers uptime, it can only tell you your personal ability to connect to a server.

note: this is currently being ported to all operating systems but currently invokes some windows only functionality. 