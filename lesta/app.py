from flask import Flask, jsonify
import redis

app = Flask(__name__)

redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

COUNTER_KEY = "visit_count"

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

@app.route("/count", methods=['GET'])
def increment_and_get_count():
    try:
        count = redis_client.incr(COUNTER_KEY)
        return jsonify({"count": int(count)})
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return jsonify({"error": "Could not connect to Redis"}), 500


if __name__ == "__main__":
    if not redis_client.exists(COUNTER_KEY):
        redis_client.set(COUNTER_KEY, 0)
    app.run(debug=True, host='0.0.0.0')
