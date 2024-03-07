from sshlib import SSHException, SSHAuth, SSHClient, SSHKeyPairAuth, SSHMain
from sys import  exit
from utils import port_is_open
import os

def get_ssh_host():
    while True:
        host = input("Enter the host: ")
        if port_is_open(host, 22):
            return host
        else:
            print("Port 22 is closed on the host")

def get_ssh_user(host: str):
    return input(f"Enter the username for {host}: ")

def get_ssh_keyfile(username: str):
    while True:
        keyfile = input(f"Enter the path to the private key for {username}: ")
        if os.path.exists(keyfile):
            return keyfile
        else:
            print(f"{keyfile} does not exist")

def keypair_main():
    HOST = get_ssh_host()
    user = get_ssh_user(HOST)
    keyfile = get_ssh_keyfile(user)
    auth = SSHKeyPairAuth(user, keyfile)
    SSHMain(HOST, auth)



