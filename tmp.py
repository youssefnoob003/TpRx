import subprocess
import re
import time
import platform
import matplotlib.pyplot as plt
import numpy as np
import json

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

read_data_from_cmd()