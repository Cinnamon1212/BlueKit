import bluetooth
import subprocess
import os
import sys
import time

# globals
nearby = []
services = []
interface = "hci0"

def setglobal(var, value):
    if var == "nearby":
        global nearby
        nearby = value
    elif var == "services":
        global services
        services = value
    elif var == "interface":
        global interface
        interface = value


def checkglobal(var):
    if var == "nearby":
        global nearby
        return nearby
    elif var == "services":
        global services
        return services
    elif var == "interface":
        global interface
        return interface
def cls():
    os.system("clear")

def scan_nearby():
    nearby = bluetooth.discover_devices(lookup_names=True)
    return nearby

def main():
    default_interface = checkglobal("interface")
    print("(1) Scan nearby devices")
    print("(2) Scan services")
    print("(3) RFCOMM connect")
    print("(4) l")
    print(f"(*) Set bluetooth interface (Default: {default_interface})")
    menu_choice = input("Please enter an option from the menu (by number)")
    menu_choice == menu_choice.lower()

    if menu_choice == "1" or menu_choice == "nearby":
        cls()
        nearby = []
        while nearby == []:
            nearby = scan_nearby()
            if nearby == []:
                print("Scanning.. ", end="\r")
        print(f"Found {len(nearby)} devices!")
        setglobal("nearby", nearby)
        for addr, name in nearby:
            print(f"{name}: {addr}")
        input("Press any key to continue")
        cls()
        main()

    elif menu_choice == "2" or menu_choice == "services":
        nearby = checkglobal("nearby")
        if nearby == []:
            print("Please scan for nearby devices first!")
            time.sleep(2)
            cls()
            main()
        services = checkglobal("services")
        if services != []:
            print("This will overwrite the currently saved services, do you wish to continue? ")
            while True:
                overwrite = input("Y/N: ")
                if overwrite.lower() == "n":
                    break
                    cls()
                    main()
                elif overwrite.lower() == "y":
                    break
                else:
                    continue
        i = 0
        print("Please choose a MAC Address from the list below: ")
        for addr, name in nearby:
            print(f"({i + 1}) {name}: {addr}")
            i += 1
        while True:
            device = input("Please enter the number of the device you'd like to check: ")
            try:
                device = int(device)
                nearbycount = len(nearby)
                if device <= nearbycount + 1:
                    break
                else:
                    continue
            except ValueError:
                continue
        device = nearby[device - 1]
        services = bluetooth.find_service(address=device[0])
        if services != []:
            for serv in services:
                print(f"\nService name: {serv['name']}")
                print(f"Service description: {serv['description']}")
                print(f"Protocol: {serv['protocol']}")
                print(f"Port: {serv['port']}")
        else:
            print("No services found!")
            time.sleep(2)
            cls()
            main()
        input("Press any key to continue")
        cls()
        main()
    elif menu_choice == "3" or menu_choice == "rfcomm connect":
        nearby = checkglobal("nearby")
        if nearby == []:
            print("Please scan for nearby devices first")
            time.sleep(2)
            cls()
            main()
        i = 1
        for device in nearby:
            addr, name = device
            print(f"({i}) {name}: {addr} ")
            i += 1
        while True:
            device = input("Please enter which device you would look to connect to: ")
            try:
                device = int(device)
                if device <= len(nearby):
                    break
                else:
                    print("Please enter an number from the list provided")
                    time.sleep(2)
                    cls()
            except ValueError:
                print("Please enter a number from the list provided")
                time.sleep(2)
                cls()
        device = nearby[device - 1]
        addr, name = device
        while True:
            port = input("Please enter the RFCOMM port (If you're unsure, go back and perform a service scan): ")
            if port == "back":
                cls()
                main()
            try:
                port = int(port)
                if port  <= 65536:
                    break
                else:
                    print("Ports must be not be larger than 65536")
                    time.sleep(2)
                    cls()
            except ValueError:
                print("Ports must be integers")
                time.sleep(2)
                cls()
        interface = checkglobal("interface")
        while True:
            passkey = input("Please enter the passkey (leave blank if unknown): ")
            if passkey != "":
                connect = subprocess.call(f"hcitool -i {interface} cc {addr}; hcitool auth {addr}", shell=True)
            else:
                connect = subprocess.call(f"hcitool -i {interface} cc {addr}", shell=True)
    elif menu_choice == "4" or menu_choice == "l2cap connect":
        pass
    elif menu_choice == "*":
        os.system("hciconfig")
        interface = input("Please choose an interface: ")
        setglobal("interface", interface)
        print(f"Interface set to: {interface}")
        time.sleep(2)
        cls()
        main()



    else:
        print("Please choose between 1 and x")
        cls()
        main()

if __name__ == "__main__":
    cls()
    main()
