# MACOS VMX EXPLOIT PATCHER

This exploit allows VMWare ESXI 7.0 servers to emulate MacOS Sonoma 14
It tricks the system into thinking it is running on a real Mac.
It does this by modifying the VMX file to include match the SMBIOS of a real Mac.

## Notice
This is a proof of concept
This is for educational purposes only
We are not responsible for any damages caused by this software
We are not responsible for any legal actions taken against you for using this software
We do not condone the use of this software for any illegal activities

## Prerequisites
 - [VMWare ESXI](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.esxi.install.doc/GUID-016E39C1-E8DB-486A-A235-55CAB242C351.html)
 - [ESXI-UNLOCKER](https://github.com/DrDonk/esxi-unlocker)
 - [MacOS Sonoma 14 ISO](https://iboysoft.com/howto/macos-sonoma-iso.html)

## Guide
In order to get MacOS Sonoma 14 running on a ESXI host, you will need to follow a few steps
 1. Install VMWare ESXI on your server and configure it
 2. Patch ESXI with the ESXI-UNLOCKER, this will allow MacOS machines to be created
 3. Create a ISO installer image for MacOS Sonoma 14 or any desired MacOS version
 4. Create a base MacOS VM with the desired settings
 5. Enable SSH on the ESXI host
 6. Run the VMX patcher exploit on the VM to enable MacOS emulation
 7. Disable SSH on the ESXI host
 8. Install MacOS on the VM and enjoy

## Usage of the VMX Patcher
Once you have a base MacOS VM created you can run the VMX patcher to enable MacOS emulation

From a bash terminal
```bash
./macos_vmx
```

From a Windows Powershell Terminal
```powershell
.\macos_vmx.ps1
```

The script will prompt for the ESXI host IP, username for SSH and password for SSH

Once the script has connected to the ESXI host, it will display a list of MacOS VMS it detected on the system

From here you will select which VM you want to patch and the script will do the rest

## License
[MIT](LICENSE)

