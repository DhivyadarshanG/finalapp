import os
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to Redis - Use environment variables for host and port
redis_host = os.environ.get('REDIS_HOST', 'localhost')  # Redis host
redis_host = os.environ.get('REDIS_HOST', 'redis.please.svc.cluster.local')
  # Extract port number from the string


'''try:
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    r.ping()
    print("Connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    # Optionally, exit or handle the error appropriately in a real app
    # For this simple example, we'll let it proceed but endpoints will fail
    r = None # Indicate connection failure'''
try:
    r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), 
                   port=int(os.getenv('REDIS_PORT', 6379)),
                   socket_connect_timeout=2)
    r.ping()
except Exception as e:
    app.logger.error(f"Could not connect to Redis: {e}")
    redis_connection = False

@app.route('/')
def health_check():
    if r and r.ping():
        return "API is running and connected to Redis.\n"
    else:
        return "API is running but FAILED to connect to Redis.\n", 500

@app.route('/vote/<option>', methods=['POST'])
def vote(option):
    if not r:
        return "Redis connection not available", 500

    if option not in ['cats', 'dogs']:
        return "Invalid option", 400

    try:
        count = r.incr(option)
        return jsonify({"option": option, "count": count})
    except redis.exceptions.RedisError as e:
        return f"Redis error: {e}", 500

@app.route('/results', methods=['GET'])
def results():
    if not r:
        return "Redis connection not available", 500

    try:
        cats_count = r.get('cats') or 0
        dogs_count = r.get('dogs') or 0
        return jsonify({"cats": int(cats_count), "dogs": int(dogs_count)})
    except redis.exceptions.RedisError as e:
        return f"Redis error: {e}", 500

if __name__ == '__main__':
    # Port 5001 for the API
    app.run(host='0.0.0.0', port=5001, debug=True)
