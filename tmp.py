import subprocess
import re
import time
import platform
import matplotlib.pyplot as plt
import numpy as np

def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
    print(out)
    if platform.system() == 'Linux':
        m = re.findall(' (wlan [0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    elif platform.system() == 'Windows':
        m = re.findall ('Nom. *?ÿ:.*?([A-Z0-9 ]*).*?Signal. *?ÿ:.*?([0-9]*) %', out, re.DOTALL)
    else:
        raise Exception('reached else of if statement')
    p.communicate()
    print(m)
    return m

read_data_from_cmd()