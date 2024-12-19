from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Set your Pastebin API key
PASTEBIN_API_KEY = '9HETseTyt6LMhiqmVURSAiKFtpb7Q3AH'

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate_pastebin', methods=['POST'])
def generate_pastebin():
    # Get data from form
    paste_title = request.form.get('title')
    paste_content = request.form.get('content')
    paste_format = request.form.get('format', 'text')  # Default to text
    paste_private = request.form.get('private', '0')  # Default to public (0)
    paste_expire_date = request.form.get('expire_date', 'N')  # Default to never expire

    # Pastebin API endpoint
    pastebin_url = "https://pastebin.com/api/api_post.php"

    # Data to send to Pastebin
    payload = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': paste_content,
        'api_paste_name': paste_title,
        'api_paste_format': paste_format,
        'api_paste_private': paste_private,
        'api_paste_expire_date': paste_expire_date
    }

    try:
        # Make the POST request to Pastebin
        response = requests.post(pastebin_url, data=payload)
        response.raise_for_status()

        # Return the Pastebin URL if successful
        return jsonify({"success": True, "url": response.text})
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)})
