import os
from flask import Flask, render_template, Response
import requests # To fetch results from API

app = Flask(__name__)

# Get the internal API service name from environment variable
# Default to localhost for local testing
API_SERVICE_HOST = os.environ.get('API_SERVICE_HOST', 'localhost:5001')
API_PROTOCOL = os.environ.get('API_PROTOCOL', 'http')
API_BASE_URL = f"{API_PROTOCOL}://{API_SERVICE_HOST}"

@app.route('/')
def index():
     # The template itself will fetch data via the /api/results proxy
    return render_template('index.html')

# Proxy endpoint to forward requests to the backend API /results
@app.route('/api/results', methods=['GET'])
def proxy_results():
    try:
        api_url = f"{API_BASE_URL}/results"
        print(f"Forwarding results request to: {api_url}") # Debugging
        response = requests.get(api_url, timeout=5) # Add timeout
        # Forward the response from the API back to the client
        return Response(response.content, status=response.status_code, mimetype=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        print(f"Error forwarding results request: {e}")
        return "Error contacting results API", 502 # Bad Gateway


if __name__ == '__main__':
    # Port 5002 for the result UI
    app.run(host='0.0.0.0', port=5002, debug=True)
