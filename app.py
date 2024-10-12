from flask import Flask, render_template, jsonify
import subprocess
import json

app = Flask(__name__)


def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
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

    # Return parsed data as a dictionary
    return parsed_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_signal')
def get_signal():
    data = read_data_from_cmd()  # Get all the parsed key-value pairs
    return jsonify(data)  # Return as JSON to be used in the table


if __name__ == '__main__':
    app.run(debug=True)
