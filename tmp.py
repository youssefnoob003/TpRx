import subprocess
import re
import time
import platform
import matplotlib.pyplot as plt
import numpy as np
import json

from matplotlib.cbook import pts_to_midstep


def bssid_to_dict(payload):
    # Initialize a dictionary to hold the networks
    networks = {}
    # Split the output into lines
    lines = payload.strip().split('\n')[1:]

    current_ssid = None
    current_bssid = None

    # Regular expressions to match different lines
    ssid_pattern = re.compile(r'SSID \d+ : (.+)')
    bssid_pattern = re.compile(r'BSSID \d+ : (.+)')
    property_pattern = re.compile(r'(.+?)\s+:\s+(.+)')

    for line in lines:
        ssid_match = ssid_pattern.match(line)
        bssid_match = bssid_pattern.match(line)
        property_match = property_pattern.match(line)

        if ssid_match:
            current_ssid = ssid_match.group(1)
            networks[current_ssid] = {
                'network_type': None,
                'authentication': None,
                'encryption': None,
                'bssids': {}
            }

        elif bssid_match and current_ssid:
            current_bssid = bssid_match.group(1)
            networks[current_ssid]['bssids'][current_bssid] = {
                'signal': None,
                'radio_type': None,
                'band': None,
                'channel': None,
                'basic_rates': None,
                'other_rates': None
            }

        elif property_match:
            key, value = property_match.groups()
            key = key.strip().lower().replace(' ', '_')

            if current_bssid:
                if key in networks[current_ssid]['bssids'][current_bssid]:
                    networks[current_ssid]['bssids'][current_bssid][key] = value.strip()
                else:
                    networks[current_ssid][key] = value.strip()
            else:
                networks[current_ssid][key] = value.strip()

    return networks


def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
    print(out)
    p.communicate()
    parsed_data = {}
    lines = out.splitlines()

    for line in lines:
        # Remove any leading/trailing whitespace
        line = line.strip()

        # Check if the line contains a key-value pair
        if " : " in line:
            key, value = line.split(" : ", 1)  # Split by first occurrence of " : "
            parsed_data[key.strip()] = value.strip()

    # Convert to JSON
    json_data = json.dumps(parsed_data, indent=4)
    print(json_data)
    return json_data


def get_bssid_info():
    p = subprocess.Popen("netsh wlan show networks mode=bssid", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
    p.communicate()

    print(out)
    return bssid_to_dict(str(out))


def read_all_ssids():
    p = subprocess.Popen("netsh wlan show networks", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
    p.communicate()

    ssids = []
    lines = out.splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith("SSID"):
            ssid_match = re.search(r'SSID \d+ : (.+)', line)
            if ssid_match:
                ssids.append(ssid_match.group(0).strip())

    return ssids

print((read_all_ssids()))
