from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory vote storage
votes = {
    "cats": 0,
    "dogs": 0
}

@app.route('/')
def health_check():
    return "API is running and storing votes in memory.\n"

@app.route('/vote/<option>', methods=['POST'])
def vote(option):
    if option not in votes:
        return "Invalid option", 400

    votes[option] += 1
    return jsonify({"option": option, "count": votes[option]})

@app.route('/results', methods=['GET'])
def results():
    return jsonify(votes)

if __name__ == '__main__':
    # Port 5001 for the API
    app.run(host='0.0.0.0', port=5001, debug=True)
