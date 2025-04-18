'''import os
from flask import Flask, render_template, Response
import requests # For proxying

app = Flask(__name__)

# Get the internal API service name from environment variable
# Default to localhost for local testing
API_SERVICE_HOST = os.environ.get('API_SERVICE_HOST', 'localhost:5001')
API_PROTOCOL = os.environ.get('API_PROTOCOL', 'http')
API_BASE_URL = f"{API_PROTOCOL}://{API_SERVICE_HOST}"

@app.route('/')
def index():
    return render_template('index.html')

# Proxy endpoint to forward requests to the backend API
# This avoids CORS issues and hides the internal API address from the browser
@app.route('/api/vote/<option>', methods=['POST'])
def proxy_vote(option):
    try:
        api_url = f"{API_BASE_URL}/vote/{option}"
        print(f"Forwarding vote to: {api_url}") # For debugging
        response = requests.post(api_url, timeout=5) # Add timeout
        # Forward the response from the API back to the client
        return Response(response.content, status=response.status_code, mimetype=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        print(f"Error forwarding vote request: {e}")
        return "Error contacting vote API", 502 # Bad Gateway


if __name__ == '__main__':
    # Port 5000 for the vote UI
    app.run(host='0.0.0.0', port=5000, debug=True)'''
import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Get API URL from environment variable or use default
API_HOST = os.getenv('API_HOST', 'voteapi')
API_PORT = os.getenv('API_PORT', '5001')
API_URL = f"http://{API_HOST}:{API_PORT}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vote/<option>', methods=['POST'])
def send_vote(option):
    vote_url = f"{API_URL}/vote/{option}"
    app.logger.info(f"Forwarding vote to: {vote_url}")
    try:
        response = requests.post(vote_url, timeout=5)
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error(f"Error forwarding vote request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
