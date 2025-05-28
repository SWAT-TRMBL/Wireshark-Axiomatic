import subprocess
import os
import sys
import shutil
import time

# Define your file paths - 
# should be the same for all windows machines 
# unless a custom installation was performed for wireshark
WIRESHARK_PATH = r"C:\Program Files\Wireshark\Wireshark.exe"
#CAPTURE_DIR = os.path.join(os.getcwd(), "captures")
# Test Commit comment

def check_wireshark_installation():
    if not os.path.isfile(WIRESHARK_PATH):
        print("Wireshark not found. Please install it at:", WIRESHARK_PATH)
        sys.exit(1)

def list_available_interfaces():
    try:
        result = subprocess.run([WIRESHARK_PATH, "-D"], capture_output=True, text=True)
        interfaces = result.stdout.strip().splitlines()
        if not interfaces:
            print("No interfaces found.")
            sys.exit(1)
        return interfaces
    except Exception as e:
        print("Failed to list interfaces:", e)
        sys.exit(1)

# For CAN to ETH converters we will want to chose ethernet
def choose_interface(interfaces):
    print("\nAvailable interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{iface}")
    choice = input("\n*Choose Ethernet for CAN to ETH converters*\nEnter the number(Left) of the interface to use: ")
    try:
        idx = int(choice)-1
        return interfaces[idx].split(".")[0]  # Interface ID (before the name)
    except (ValueError, IndexError):
        print("Invalid selection.")
        sys.exit(1)

def format_mac_address(mac):
    mac = mac.replace(":","").replace("-","")
    if len(mac) != 12:
        raise ValueError("MAC address must be 12 hexadecimal characters long")
    formatted_mac = ':'.join(mac[i:i+2] for i in range(0,12,2))
    return formatted_mac

def get_mac_address():
    mac = input("Enter a MAC address to filter (e.g., aa:bb:cc:dd:ee:ff or aa-bb-cc-dd-ee-ff or aabbccddeeff): ").strip()
    try:
        formatted_mac = format_mac_address(mac)
        print("MAC address entered:",formatted_mac)
    except ValueError as e:
        print(e)
        
    return formatted_mac

# Removing file capture to avoid directory creation issues on end user machines        
"""def ensure_capture_dir():
    if not os.path.isdir(CAPTURE_DIR):
        os.makedirs(CAPTURE_DIR)

def get_capture_filename(mac):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    sanitized_mac = mac.replace(":", "").lower()
    return os.path.join(CAPTURE_DIR, f"capture_{sanitized_mac}_{timestamp}.pcapng")
"""
def main():
    check_wireshark_installation()
    #ensure_capture_dir()

    interfaces = list_available_interfaces()
    interface_id = choose_interface(interfaces)
    mac = get_mac_address()
    display_filter = f"arp && eth.src == {mac}"
    #capture_file = get_capture_filename(mac)

    print("\nLaunching Wireshark with:")
    print(f"  Interface: {interface_id}")
    print(f"  Filter: {display_filter}")
    #print(f"  Output file: {capture_file}\n")

    subprocess.run([
        WIRESHARK_PATH,
        "-i", interface_id,
        "-k",  # start capturing immediately
        "-Y", display_filter
        #"-w", capture_file  # write to capture file
    ])

if __name__ == "__main__":
    main()
