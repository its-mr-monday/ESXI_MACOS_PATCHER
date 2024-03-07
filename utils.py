import socket

def port_is_open(ip: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

#These are some things to add to the vmx file
#They ensure that ESXI tricks the OS into thinking it's running
#on a Macbook Pro 2019, which is the most compatible hardware
def vmx_file_additions() -> list[str]:
    return [
        "ethernet0.virtualDev = \"vmxnet3\"",
        "board-id = \"Mac-AA95B1-DDAB278B95\"",
        "hw.model.reflectHost = \"FALSE\"",
        "hw.model = \"MacBookPro19,1\"",
        "serialNumber.reflectHost = \"FALSE\"",
        "serialNumber = \"C02ZT0J0MD6H\"",
        "board-id.reflectHost = \"FALSE\"",
    ]

def vmx_file_exists_cmd(file_path: str) -> str:
    return f"test -f {file_path} && echo 'True' || echo 'False'"


def vmx_file_commands(file_path: str):
    file_additions = vmx_file_additions()
    commands = []
    commands.append(f"sed -i '/ethernet0.virtualDev = /d' {file_path}")
    for line in file_additions:
        commands.append(f"echo '{line}' >> {file_path}")
    return commands

def test_file_exists(file_path: str) -> str:
    return f"test -f {file_path} && echo 'True' || echo 'False'"

def test_dir_exists(dir_path: str) -> str:
    return f"test -d {dir_path} && echo 'True' || echo 'False'"

def pretty_list_dir(dir_path: str) -> str:
    return f"ls -l {dir_path} | awk '{{print $9}}'"

def test_datastore_exists_cmd(datastore_name: str) -> str:
    return f"esxcli storage filesystem list | grep \"VMFS-6\" | grep {datastore_name} && echo 'True' || echo 'False'"

def list_datastores_cmd() -> str:
    return "esxcli storage filesystem list | grep \"VMFS-6\" | awk '{print $2}'"

def list_vms_cmd() -> str:
    return "vim-cmd vmsvc/getallvms | awk '{print $2} | grep -V '^[[:space:]]*$' | awk '!/-/''"

def list_darwin_vms_cmd() -> str:
    return "vim-cmd vmsvc/getallvms | grep darwin | awk '{print $2'}"

def get_vm_datastore_cmd(vm_name: str) -> str:
    return f"vim-cmd vmsvc/getallvms | grep {vm_name} | awk '{{print $3}}'"

def get_datastore_path(datastore: str) -> str:
    return "esxcli storage filesystem list | grep " + datastore + " | awk '{print $1}'"

def get_vmx_guestos_cmd(vmx_file: str) -> str:
    return f"cat {vmx_file} | grep guestOS = | awk -F '\"' '{{print $2}}'"

def pretty_list_files(dir_path: str) -> str:
    return f"ls -l {dir_path} | grep -v ^d | awk '{{print $9}}'"
