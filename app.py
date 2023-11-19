from flask import Flask, render_template, request
import socket
import psutil
import datetime
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_name = request.form['username']

    system_username = user_name
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_details = psutil.__version__
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    ip_info_url = f"https://db-ip.com/api/doc.php{ip_address}"
    ip_info_headers = {
        "Accept": "application/json",
        "Key": "c3ac4fdfbdfb63c1effc73278c7cefaede23c0b1"
    }

    ip_info = None  # Initialize ip_info variable

    try:
        ip_info_response = requests.get(ip_info_url, headers=ip_info_headers)
        ip_info_response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Check for 404 error explicitly
        if ip_info_response.status_code == 404:
            error_message = "IP not found in the database"
        else:
            ip_info = ip_info_response.json()
            error_message = None
    except requests.exceptions.RequestException as e:
        # Handle any request-related exceptions here
        error_message = f"Request error: {e}"
    except json.decoder.JSONDecodeError as e:
        # Handle JSON decoding error
        error_message = f"JSON decoding error: {e}"

    return render_template('result.html', username=user_name, system_username=system_username, date=date,
                           os_details=os_details, host_name=host_name, ip_address=ip_address, ip_info=ip_info,
                           error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
