from banner import banner
from sys import exit
from password import password_main
from keypair import keypair_main

def WARNING_ACKNOWLEDGEMENT() -> bool:
    print("This is a warning prior to proceeding with the exploit")
    print("This exploit is for educational purposes only")
    print("We are not responsible for any damage caused by the use of this exploit")
    print("We do not condone the use of this exploit for malicious purposes")
    print("We are not responsible for any damage caused by the use of this exploit")
    print("Do you acknowledge the warning?")
    while True:
        response = input("Enter 'yes' or 'no': ")
        if response.lower() == "yes":
            return True
        elif response.lower() == "no":
            return False
        else:
            print("Invalid response. Please try again.")

def print_menu():
    print("Welcome to the ESXI MacOS VMX Exploit")

    print("You must have SSH active and openon the ESXI host along with authorization to login to the host")
    print("The following script is intended to be used after running the esxi unlocker and setting up the MacOS VMX file")
    
def __is_int__(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_menu_input(prompt: str, options: list):
    print_menu()
    while True:
        print(prompt)
        for i in range(len(options)):
            print(f"{i+1}. {options[i]}")
        print("0. Exit")
        choice = input("Enter choice: ")
        if __is_int__(choice):
            c = int(choice)
            if c >= 0 and c <= len(options):
                return c
        print("Invalid choice. Please try again.")

def menu():
    aknowledgement = WARNING_ACKNOWLEDGEMENT()
    if not aknowledgement:
        exit(1)
    MENU_PROMPT = '''
Please select an option:
'''
    options = [ "SSH Key Pair Authentication", "SSH User/Password Authentication"]
    choice = get_menu_input(MENU_PROMPT, options)
    if choice == 0:
        exit(0)
    if choice == 1:
        keypair_main()
    if choice == 2:
        password_main()

def main():
    banner()
    menu()
    return 0

if __name__ == "__main__":
    main()
