from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# Simulated CAN message storage
received_messages = []

# Simulated periodic message sender
def send_periodic_message():
    while True:
        # Simulate sending a periodic CAN message
        message = {'id': 0x123, 'data': [0x01, 0x02, 0x03]}
        received_messages.append(message)

        time.sleep(1)  # Wait for 1 second

# Start the periodic message sender in a separate thread
import threading
t = threading.Thread(target=send_periodic_message)
t.start()

# API endpoint to retrieve received messages
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(received_messages)

# API endpoint to send a CAN message
@app.route('/api/messages', methods=['POST'])
def send_message():
    if not request.json or 'id' not in request.json or 'data' not in request.json:
        return jsonify({'error': 'Invalid request'}), 400

    message = {
        'id': request.json['id'],
        'data': request.json['data']
    }
    
    # Simulate receiving a CAN message
    received_messages.append(message)

    return jsonify({'success': True}), 201

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
curl -X POST -H "Content-Type: application/json" -d '{"id": 123, "data": [1, 2, 3]}' http://localhost:5000/api/messages
