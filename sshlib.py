import paramiko
from utils import *
from sys import exit

class SSHException(Exception):
    pass

class SSHAuth:
    def __init__(self):
        self.username = None
        self.password = None
        self.key = None
        self.AUTH_METHOD = None

    def to_dict(self):
        raise NotImplementedError

    def auth_method(self) -> str | None:
        return self.AUTH_METHOD

class SSHUserPassAuth(SSHAuth):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.AUTH_METHOD = 'password'

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'AUTH_METHOD': self.AUTH_METHOD
        }

class SSHKeyPairAuth(SSHAuth):
    def __init__(self, username: str, key: str):
        self.username = username
        self.key = key
        self.AUTH_METHOD = 'key'
        if not self.__key_exists():
            raise SSHException(f"Key file {key} does not exist")

    def __key_exists(self) -> bool:
        try:
            with open(self.key, 'r') as f:
                return True
        except Exception as e:
            print(f"Error occured during key file check: {e}")
            return False

    def to_dict(self):
        return {
            'username': self.username,
            'key': self.key,
            'AUTH_METHOD': self.AUTH_METHOD
        }

class SSHClient:
    def __init__(self, host: str, auth: SSHAuth, port: int = 22):
        self.host = host
        self.auth = auth
        self.port = port
        self._client = None
        self._connected = False
        self.__test_connection()

    def connected(self) -> bool:
        if not self._connected:
            return False
        if self._client == None:
            self._connected = False
            return False
        return True

    def __test_connection(self):
        try:
            if not self.__connect():
                return False
            self.__disconnect()
            return True
        except Exception as e:
            print(f"Error occured during connection testing: {e}")
            return False
    
    def __private_key_client(self) -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        auth_dict = self.auth.to_dict()
        USERNAME = auth_dict['username']
        KEYFILE = auth_dict['key']
        key = paramiko.RSAKey.from_private_key_file(KEYFILE)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = self.host, username = USERNAME, pkey = key)
        return client

    def __password_client(self) -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        auth_dict = self.auth.to_dict()
        USERNAME = auth_dict['username']
        PASSWORD = auth_dict['password']
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = self.host, username = USERNAME, password = PASSWORD)
        return client
    
    def connect(self) -> bool:
        return self.__connect()

    def __connect(self) -> bool:
        if self.connected():
            return True
        try:
            AUTH_METHOD = self.auth.auth_method()
            if AUTH_METHOD == None:
                raise SSHException("Invalid authentication method")
            
            match AUTH_METHOD:
                case "password":
                    self._client = self.__password_client()
                    self._connected = True
                    return True
                case "key":
                    self._client = self.__private_key_client()
                    self._connected = True
                    return True
                case _:
                    raise SSHException(f"Invalid authentication method: {AUTH_METHOD}")

        except Exception as e:
            #if the exception is a SSHException, raise it
            if isinstance(e, SSHException):
                raise e
            print(f"Error occured during connection: {e}")
            return False

    def __disconnect(self) -> bool:
        if not self.connected():
            return True
        try:
            self._client.close()
            self._connected = False
            self._client = None
            return True
        except Exception as e:
            print(f"Error occured during disconnect: {e}")
            return False

    def execv(self, command: str) -> str | None:
        if not self.connected():
            raise SSHException("Not connected to host")
        try:
            stdin, stdout, stderr = self._client.exec_command(command)
            return stdout.read().decode('utf-8') + stderr.read().decode('utf-8')

        except Exception:
            return None

def select_vm(vm_list: list[str]) -> str:
    print("Select a VM to modfy")
    for i, vm in enumerate(vm_list):
        print(f"{i+1}. {vm}")
    selection = input("Enter the number of the VM: ")
    try:
        selection = int(selection)
        if selection < 1 or selection > len(vm_list):
            raise ValueError
    except ValueError:
        print("Invalid selection")
        return select_vm(vm_list)
    return vm_list[selection-1]

def SSHMain(host: str, auth: SSHAuth):
    client = SSHClient(host, auth)
    try:
        if not client.connect():
            print("Failed to connect to the host")
            exit(1)
        print("Connected to the host")
        all_vms = client.execv(list_darwin_vms_cmd())
        vm_list = all_vms.split('\n')
        #There is a emptu element at the end of the list
        vm_list.pop()
        VM_TO_USE = select_vm(vm_list)
        vm_datastore = client.execv(get_vm_datastore_cmd(VM_TO_USE))
        vm_datastore = vm_datastore.strip()
        vm_datastore = vm_datastore.replace("[", "")
        vm_datastore = vm_datastore.replace("]", "")
        print(f"VM {VM_TO_USE} is on datastore {vm_datastore}")
        datastore_path = client.execv(get_datastore_path(vm_datastore)).strip()
        VMX_FILE_PATH = f"{datastore_path}/{VM_TO_USE}/{VM_TO_USE}.vmx"
        EXISTS_STR = client.execv(vmx_file_exists_cmd(VMX_FILE_PATH))
        if "True" in EXISTS_STR:
            print(f"VMX file exists at {VMX_FILE_PATH}")
        else:
            print(f"Failed to locate VMX file at {VMX_FILE_PATH}")
            exit(1)
        COMMANDS = vmx_file_commands(VMX_FILE_PATH)
        for cmd in COMMANDS:
            print(f"Executing command: {cmd}")
            client.execv(cmd)
        print("Commands executed")
        print("VMX file updated")
        print("Boot the VM and install MacOS")
        exit(0)
    except SSHException as e:
        print(f"Failed to connect to the host: {e}")
        exit(1)
