from sshlib import SSHException, SSHAuth, SSHClient, SSHKeyPairAuth, SSHUserPassAuth, SSHMain
from sys import exit
from getpass import getpass
from utils import port_is_open

def get_ssh_host():
    while True:
        host = input("Enter SSH Host: ")
        if port_is_open(host, 22):
            return host
        else:
            print("Port 22 is not open on the host.")

def get_ssh_user(host: str):
    return input(f"Enter SSH User for {host}: ")

def get_ssh_password(username: str):
    return getpass(f"Enter SSH Password for {username}: ")


def password_main():
    HOST = get_ssh_host()
    user = get_ssh_user(HOST)
    password = get_ssh_password(user)

    auth = SSHUserPassAuth(user, password)
    SSHMain(HOST, auth)


