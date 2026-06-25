from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

vehicle_events = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "version": "1.1", "timestamp": datetime.datetime.utcnow().isoformat()})

@app.route('/ingest', methods=['POST'])
def ingest():
    event = request.get_json()
    if not event:
        return jsonify({"error": "No JSON body provided"}), 400

    event['received_at'] = datetime.datetime.utcnow().isoformat()
    vehicle_events.append(event)

    return jsonify({"message": "Event ingested", "total_events": len(vehicle_events)}), 201

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify({"count": len(vehicle_events), "events": vehicle_events})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
