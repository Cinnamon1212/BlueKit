import subprocess
import os
import sys
import time
import bluetooth
import pyshark
import keyboard
from datetime import datetime
# globals
nearby = []
services = []
interface = "hci0"
load_capture = ""
file = ""
display_filter = ""
packet_selection = ""
saved_packets = []

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
    elif var == "load_capture":
        global load_capture
        load_capture = value
    elif var == "file":
        global file
        file = value
    elif var == "display_filter":
        global display_filter
        display_filter = value
    elif var == "packet_selection":
        global packet_selection
        packet_selection = value
    elif var == "saved_packets":
        global saved_packets
        saved_packets = value

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
    elif var == "load_capture":
        global load_capture
        return load_capture
    elif var == "file":
        global file
        return file
    elif var == "display_filter":
        global display_filter
        return display_filter
    elif var == "packet_selection":
        global packet_selection
        return packet_selection
    elif var == "saved_packets":
        global saved_packets
        return saved_packets

def cls():  # clear console
    os.system("clear")
def scan_nearby():  # Find nearby devices
    nearby = bluetooth.discover_devices(lookup_names=True)
    return nearby
def view_packets():  # Viewing packet information
    file = checkglobal("file")
    display_filter = checkglobal("display_filter")
    capture = checkglobal("load_capture")
    if capture == "":
        if file == "":
            print("Please load a file first!")
            time.sleep(3)
            cls()
            packet_analysis()
        if display_filter == "":
            capture = pyshark.FileCapture(file, use_json=True, include_raw=True)
            setglobal("load_capture", capture)
        else:  # display filter is validated at assignment
            capture = pyshark.FileCapture(file, display_filter=display_filter, use_json=True, include_raw=True)
            setglobal("load_capture", capture)
    else:
        pass  # capture already loaded
    print("(1) View layers")
    print("(2) View saved packets")
    print("(<) Back")
    print("(*) Packet selection")
    menu_choice = input("Please enter an option from the menu: ")
    menu_choice = menu_choice.lower()
    if menu_choice == "*" or menu_choice == "packet selection":
        print("(1) All packets")
        print("(2) Specific packet")
        print("(3) Packet range")
        menu_choice = input("Please enter an option from the menu: ")
        menu_choice = menu_choice.lower()
        if menu_choice == "1" or menu_choice == "all packets":
            setglobal("packet_selection", "all")
            print("All packets selected!")
            time.sleep(2)
            cls()
            view_packets()

        elif menu_choice == "2" or menu_choice == "specific packet":
            while True:
                packet = input("Please enter the packet you would like to use (starting at 1): ")
                try:
                    packet = int(packet)
                    packet = packet - 1
                    break
                except ValueError:
                    print("Invalid packet number")
                    time.sleep(2)
                    cls()
            setglobal("packet_selection", packet)
            print(f"Packet set to: {packet + 1}")
            time.sleep(2)
            cls()
            view_packets()
        elif menu_choice == "3" or menu_choice == "packet range":
            packet_range = []
            while True:
                start = input("Please enter the starting packet: ")
                try:
                    start = int(start)
                    start = start - 1
                    packet_range.append(start)
                    break
                except ValueError:
                    print("Invalid packet number")
                    time.sleep(2)
                    cls()
            while True:
                end = input("Please enter the end packet: ")
                try:
                    end = int(end)
                    end = end - 1
                    if end <= start:
                        print("Invalid end range selected")
                        time.sleep(2)
                        cls()
                    else:
                        packet_range.append(end)
                        break
                except ValueError:
                    print("Invalid packet number")
                    time.sleep(2)
                    cls()
            setglobal("packet_selection", packet_range)
            print(f"Selecting packet {start + 1} - {end + 1}")
            time.sleep(2)
            cls()
            view_packets()
    elif menu_choice == "<" or menu_choice == "back":
        cls()
        packet_analysis()
    elif menu_choice == "1" or menu_choice == "view layers":
        capture = checkglobal("load_capture")
        packet_selection = checkglobal("packet_selection")
        if packet_selection == "":
            print("No packets selected!")
            time.sleep(2)
            view_packets()
        saved_packets = checkglobal("saved_packets")
        if packet_selection == "all":
            i = 1
            for packet in capture:
                print(f"\nPacket number {i}")
                for layer in packet:
                    print(layer)
                    input("\nPress enter to go to the next layer")
                x = input("\nPress enter for next packet (or s to save, q to quit): ")
                x = x.lower()
                if x == "s" or x == "save":
                    saved_packets.append(packet)
                    setglobal("saved_packets", saved_packets)
                    print(f"Packet {i} saved")
                    i += 1
                elif x == "q" or x == "quit":
                    cls()
                    view_packets()
            input("Press enter to go back")
            cls()
            view_packets()
        elif isinstance(packet_selection, int):
            packet = capture[packet_selection]
            for layer in packet:
                print(layer)
                x = input("Press enter to go to the next layer (or q to quit)")
                x = x.lower()
                if x == "q" or x == "quit":
                    cls()
                    view_packets()
            x = input("Press enter to go back (or type s to save): ")
            if x.lower() == "s" or x.lower() == "save":
                saved_packets.append(capture[packet_selection])
                setglobal("saved_packets", saved_packets)
                print(f"Packet {packet_selection} saved")
                time.sleep(1)
                cls()
                view_packets()
        else:
            start = packet_selection[0]
            end = packet_selection[1]
            i = start
            while i != end:
                packet = capture[i]
                print(f"packet number {i}")
                for layer in packet:
                    print(layer)
                    x = input("\nPress enter to go to the next layer (or q to quit)")
                    x = x.lower()
                    if x == "q" or x == "quit":
                        cls()
                        view_packets()
                x = input("\nPress enter for next packet (or s to save, q to exit): ")
                x = x.lower()
                if x == "s" or x == "save":
                    saved_packets.append(packet)
                    setglobal("saved_packets", saved_packets)
                    print(f"Packet {i} saved")
                    time.sleep(1)
                    i += 1
                elif x == "q" or x == "quit":
                    cls()
                    view_packets()
            input("Press enter to go back")
            cls()
            view_packets()
    elif menu_choice == "2" or menu_choice == "view saved":
        saved_packets = checkglobal("saved_packets")
        if saved_packets == []:
            print("No packets saved!")
            time.sleep(2)
            cls()
            view_packets()
        print(f"{len(saved_packets)} packets saved.")
        while True:
            i = 1
            for packet in saved_packets:
                print(f"({i}) Packet number {i}")
                i += 1
            packet = input("Please enter which packet you'd like to view (type < to go back): ")
            if packet.lower() == "back" or packet == "<":
                break
                cls()
                view_packets()
            try:
                packet = int(packet - 1)
            except ValueError:
                print("Invalid packet number")
                time.sleep(2)
                cls()
            try:
                packet = saved_packets[packet]
                print(packet)
            except:
                print("Packet out of range")

            x = input("Press enter to go back (or < to exit)")
            if x == "<" or x.lower() == "exit":
                break
                cls()
                main()
            else:
                cls()
def packet_analysis():  #  Load file and filter packets
    print("(1) View packets")
    print("(2) Apply display filter")
    print("(<) Back")
    print("(*) Load file")
    menu_choice = input("Please choose an option from the menu: ")
    menu_choice = menu_choice.lower()
    if menu_choice == "*" or menu_choice == "load file":
        file = checkglobal("file")
        if file != "":
            while True:
                check = input("Capture file already loaded, would you like to load a new one? (y/N)")
                accepted = ['yes', 'no', 'n', 'y', '', ' ']
                check = check.lower()
                if check in accepted:
                    break
                else:
                    print("Invalid options, please use y/n (enter for default)")
                    time.sleep(2)
                    cls()
            negatives = ['no', 'n', '', ' ']
            if check in negatives:
                cls()
                packet_analysis()
            while True:
                file = input("Please enter the pcap file: ")
                if os.path.isfile(file):
                    break
                else:
                    print("Unable to locate file")
                    time.sleep(2)
                    cls()
            setglobal("file", file)
            print(f"{file} sucessfully loaded")
            time.sleep(2)
            cls()
            packet_analysis()
        else:
            while True:
                file = input("Please enter the pcap file: ")
                if os.path.isfile(file):
                    break
                else:
                    print("Unable to locate file")
                    time.sleep(2)
                    cls()
            setglobal("file", file)
            print(f"{file} sucessfully loaded")
            time.sleep(2)
            cls()
            packet_analysis()

    elif menu_choice == "<" or menu_choice == "back":
        cls()
        menu()
    elif menu_choice == "1" or menu_choice == "View packets":
        cls()
        view_packets()




    elif menu_choice == "2" or menu_choice == "Apply display filter":
        while True:
            display_filter = input("Please enter the display filter you would like to use: ")
            filters = ['bluetooth.addr', 'bluetooth.addr_str', 'bluetooth.dst', 'bluetooth.dst_str', 'bluetooth.src', 'bluetooth.src_str']
            if any(filter in display_filter for filter in filters):
                print(f"Filter set to {display_filter}")
                setglobal("display_filter", display_filter)
                time.sleep(2)
                cls()
                break
            else:
                print("Invalid bluetooth filter selected..")
                time.sleep(2)
                cls()
        packet_analysis()
def main():
    print("(1) Scan nearby devices")
    print("(2) Scan services")
    print("(3) Send file")
    print("(4) Pair")
    print("(5) Make discoverable")
    print("(6) Sniff live packets")
    print("(7) Open captured packets")
    print(f"(*) Set device options")
    menu_choice = input("Please enter an option from the menu (by number): ")
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
    elif menu_choice == "3" or menu_choice == "send file":
        nearby = checkglobal("nearby")
        if nearby == []:
            print("Plase scan for nearby devices first!")
            time.sleep(2)
            cls()
            main()
        else:
            while True:
                i = 1
                for device in nearby:
                    addr, name = device
                    print(f"({i}) {name}: {device}")
                device = input("Please enter which device you'd like to use: ")
                try:
                    device = int(device)
                    device = nearby[device - 1]
                    break
                except ValueError:
                    print("Please enter a valid number")
                    time.sleep(2)
                    cls()
            while True:
                file = input("Please enter the file you'd like to send: ")
                if os.path.isfile(file):
                    break
                else:
                    print("Invalid file, please enter full path to file")
                    time.sleep(2)
                    cls
            addr, name = device
            interface = checkglobal("interface")
            print(f"Sending {file} to {name} ({addr})")
            os.system(f"bluetooth-sendto --device {addr} {file}")
            time.sleep(2)
            cls()
            main()
    elif menu_choice == "4" or menu_choice == "pair":
        nearby = checkglobal("nearby")
        i = 1
        for device in nearby:
            addr, name = device
            print(f"({i}) {name}: {addr}")
        while True:
            device = input("Please enter which device you would like to pair with: ")
            try:
                device = int(device)
                device = nearby[device - 1]
                break
            except:
                print("Invalid device, please choose by number")
                time.sleep(2)
                cls()
        print("Attempting to open bluetooth settings incase of key pairing..")
        time.sleep(2)
        cls()
        if os.environ.get('DESKTOP_SESSION') == 'gnome':
            print("Opening bluetooth settings incase of key pairing")
            os.system('gnome-control-center bluetooth')
        elif os.environ.get('DESKTOP_SESSION') == 'mate':
            print("Opening bluetooth settings incase of key pairing")
            os.system('mate-control-center bluetooth')
        else:
            input("Unable to open bluetooth settings, please manually do so")
        print("Attempting to connect..")
        os.system(f"bluetoothctl remove {addr}")
        os.system("bluetoothctl agent on")
        os.system(f"bluetoothctl trust {addr}")
        os.system(f"bluetoothctl pair {addr}")
        os.system("sleep 10")
        os.system(f"bluetoothctl connect {addr}")
        time.sleep(3)
        cls()
        main()
    elif menu_choice == "5" or menu_choice == "Make discoverable":
        while True:
            choice = input("This will allow any device to connect, do you wish to continue (y/n): ")
            if choice.lower() == "y" or choice.lower() == "yes":
                break
            elif choice.lower() == "y" or choice.lower() == "no":
                break
                cls()
                main()
            else:
                print("Please enter y or n")
                time.sleep(2)
                cls()

        os.system("bluetoothctl agent on")
        os.system("bluetoothctl discoverable on")
        os.system("bluetoothctl pairable on")
        print("Attempting to open bluetooth settings for accepting key pairing")
        if os.environ.get('DESKTOP_SESSION') == 'gnome':
            print("Opening bluetooth settings incase of key pairing")
            os.system('gnome-control-center bluetooth')
        elif os.environ.get('DESKTOP_SESSION') == 'mate':
            print("Opening bluetooth settings incase of key pairing")
            os.system('mate-control-center bluetooth')
        else:
            input("Unable to open bluetooth settings, please manually do so")
        cls()
        main()
    elif menu_choice == "6" or menu_choice == "Sniff packets":
        check = input("Please make sure you are paired with a device (if not type \"back\"):")
        if check.lower() == "back":
            cls()
            main()
        while True:
            packet_count = input("Please enter how many packets you would like to capture (0 for infinite): ")
            try:
                packet_count = int(packet_count)
                break
            except ValueError:
                print("Please enter a valid number of packets")
                time.sleep(2)
                cls()
        while True:
            timeout = input("Please enter a value for the timeout (seconds): ")
            try:
                timeout = int(timeout)
                break
            except ValueError:
                print("Invalid timeout")
                time.sleep(2)
                cls()
        while True:
            df_choice = input("Would you link to set a display filter? (y/N)")
            df_choice = df_choice.lower()
            accepted = ['yes', 'no', 'n', 'y', '', ' ']
            if df_choice.lower() in accepted:
                break
            else:
                print("Please enter y/n or press enter for default")
                time.sleep(3)
                cls()
        if df_choice == "yes" or df_choice == "y":
            while True:
                display_filter = input("Please enter the filter you'd like to use: ")
                if display_filter != "" or display_filter == " ":
                    filters = ['bluetooth.addr', 'bluetooth.addr_str', 'bluetooth.dst', 'bluetooth.dst_str', 'bluetooth.src', 'bluetooth.src_str']
                    if any(filter in display_filter for filter in filters):
                        df_choice = True
                        break
                    else:
                        print("Invalid filter")
                        time.sleep(2)
                        cls()
        interface = checkglobal("interface")
        interface = f"bluetooth{interface[-1]}"
        now = datetime.now()
        filename = f'{now.strftime(f"%d%m%Y")}.pcap'
        if df_choice == True:
                capture = pyshark.LiveCapture(interface=interface, display_filter=display_filter, output_file=filename)
        else:
                capture = pyshark.LiveCapture(interface=interface, output_file=filename)

        print("Starting live capture on bluetooth0. Press q to stop")
        time.sleep(3)
        cls()
        capture.sniff(timeout=timeout)
        scan = True
        while scan is True:
            for packet in capture.sniff_continuously(packet_count=packet_count):
                print(packet)
                if keyboard.is_pressed("q"):
                    capture.close()
                    scan = False
                    print(f"PCAP file saved as {filename}")
                    time.sleep(3)
                    cls()
                    main()
    elif menu_choice == "7" or menu_choice == "Captured packets":
        cls()
        packet_analysis()
    elif menu_choice == "*":
        default_interface = checkglobal("interface")
        print(f"(1) Set interface ({default_interface})")
        print("(2) Spoof bluetooth address")
        menu_choice = input("Please enter an option (by number): ")
        menu_choice = menu_choice.lower()
        if menu_choice == "1" or menu_choice == "interface":
            os.system("hciconfig")
            interface = input("Please enter the name of the interface you'd like to use: ")
            setglobal("interface", interface)
            print(f"Interface set to: {interface}")
            time.sleep(2)
            cls()
            main()
        elif menu_choice == "2" or menu_choice == "spoof":
            interface = checkglobal("interface")
            random = input("Would you like to set values? (y/N): ")
            if random.lower() == "y" or random.lower() == "yes":
                name = input("Please enter the name you'd like to use: ")
                address = input("Please enter the address you'd like to use: ")
                bt_class = input("Please enter the class you'd like to use: ")
                os.system(f"spooftooph -i {interface} -n {name} -a {address} -c {bt_class}")
                time.sleep(2)
                cls()
                main()
            else:
                os.system(f"spooftooph -i {interface} -R")
                print("Interface details randomized!")
                time.sleep(2)
                cls()
                main()

    else:
        print("Please choose between 1 and x")
        cls()
        main()  # Main menu

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("BlueKit must be run as root!")
        sys.exit()
    cls()
    main()
