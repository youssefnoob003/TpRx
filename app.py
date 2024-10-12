from flask import Flask, render_template, jsonify
import subprocess
import re
import platform
import logging

app = Flask(__name__)

# Enable Flask logging
logging.basicConfig(level=logging.DEBUG)


def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()

    # Log and print the raw output for debugging
    app.logger.debug(f"Raw command output: {out}")

    if platform.system() == 'Linux':
        m = re.findall(' (wlan [0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    elif platform.system() == 'Windows':
        # Updated regular expression to match your specific output
        m = re.findall(r'Name\s*:\s*(.*?)\s*\n.*?Signal\s*:\s*([0-9]+) %', out, re.DOTALL)

    else:
        raise Exception('Unsupported platform')

    app.logger.debug(f"Parsed data: {m}")  # Log parsed data
    p.communicate()
    return m


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_signal')
def get_signal():
    data = read_data_from_cmd()
    if data:
        interface_name, signal_strength = data[0][0], data[0][1]
        app.logger.debug(f"Returning data: {interface_name}, {signal_strength}%")
        return jsonify({'interface_name': interface_name, 'signal_strength': signal_strength})
    else:
        app.logger.debug("No data found, returning N/A")
        return jsonify({'interface_name': 'N/A', 'signal_strength': 'N/A'})

if __name__ == '__main__':
    app.run(debug=True)
