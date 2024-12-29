# Wi-Fi Network Connection Script

## Overview
This script provides an automated way to scan, list, and connect to Wi-Fi networks using predefined passwords. It supports macOS and Windows operating systems, utilizing system-specific commands for network management. The script reads passwords from a CSV file and attempts multiple variations of each password to connect to available networks.

---

## Features
1. **Network Scanning**: Scans and lists available Wi-Fi networks, extracting SSIDs and network names.
2. **Password Management**: Generates variations of provided passwords to maximize connection attempts.
3. **Connection Modes**:
   - Connect to a specific Wi-Fi network.
   - Attempt to connect to all detected networks using a list of passwords.
4. **Cross-Platform**: Compatible with macOS and Windows (Linux not supported).

---

## Prerequisites
- **Python 3.x** installed on your machine.
- A **CSV file (`password.csv`)** containing Wi-Fi passwords (one password per line).
- Administrator or elevated privileges for running network commands.

---

## Installation
1. Clone the repository or download the script file.
2. Place the `password.csv` file in the same directory as the script. Example structure:
   ```
   script_directory/
   ├── network_script.py
   ├── password.csv
   ```
3. Ensure Python is installed and added to your system PATH.

---

## Usage

### 1. Run the Script
Execute the script using Python:
```bash
python network_script.py
```

### 2. Choose a Connection Mode
- **Specific Network**: Enter the name of the Wi-Fi network you want to connect to and provide a password.
- **All Networks**: The script will iterate over all available networks and attempt to connect using passwords from the `password.csv` file.

### 3. Password Variations
The script generates variations of each password for better connectivity:
- Original password
- All uppercase
- Capitalized
- Alternating case patterns

---

## Commands Used

### macOS
- Scan networks:  
  ```bash
  /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x
  ```
- Connect to network:  
  ```bash
  networksetup -setairportnetwork Airport [SSID] [PASSWORD]
  ```

### Windows
- Scan networks:  
  ```bash
  netsh wlan show networks mode=bssid
  ```
- Connect to network:  
  ```bash
  netsh wlan connect name="[NETWORK_NAME]" ssid="[SSID]" key="[PASSWORD]"
  ```

---

## Error Handling
- **Unsupported OS**: The script will terminate with a `NotImplementedError` for unsupported operating systems.
- **Command Failures**: If system commands fail, errors are logged, and the script continues to the next password or network.

---

## Limitations
- **OS Support**: Only supports macOS and Windows.
- **Password Security**: Ensure `password.csv` is stored securely to protect sensitive information.
- **Linux**: Not supported due to differing network management commands.

---

## Example `password.csv`
```csv
password123
mysecurepassword
admin1234
guestwifi
```

---

## License
This script is provided "as-is" for personal use. Please ensure compliance with local regulations and network policies when using this script.

---

## Contribution
Feel free to improve the script by adding:
- Support for Linux.
- Enhanced password management (e.g., hashed storage).
