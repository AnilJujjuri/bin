from flask import Flask, jsonify, request
import can
import threading
import time

app = Flask(__name__)

# Create a virtual CAN channel
can_interface = 'virtual'  # Virtual interface name
bus = can.interface.Bus(channel=can_interface, bustype='socketcan')

# Global variables for periodic message sender
send_thread = None
send_interval = 1.0  # Time interval between sending messages
send_message_id = 0x123  # Example message ID to send
send_message_data = [0x11, 0x22, 0x33]  # Example message data to send

def send_periodic_message():
    while True:
        msg = can.Message(arbitration_id=send_message_id, data=send_message_data)
        bus.send(msg)
        time.sleep(send_interval)

@app.route('/send', methods=['POST'])
def send_message():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON data"}), 400

    data = request.get_json()
    if 'id' not in data or 'data' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        msg_id = int(data['id'], 16)
        msg_data = [int(byte, 16) for byte in data['data']]
    except ValueError:
        return jsonify({"error": "Invalid message ID or data"}), 400

    msg = can.Message(arbitration_id=msg_id, data=msg_data)
    bus.send(msg)
    return jsonify({"success": True}), 200

@app.route('/receive', methods=['GET'])
def receive_message():
    message = bus.recv()
    response = {
        "id": hex(message.arbitration_id),
        "data": [hex(byte) for byte in message.data]
    }
    return jsonify(response), 200

@app.route('/start-sender', methods=['POST'])
def start_periodic_sender():
    global send_thread

    if send_thread is None or not send_thread.is_alive():
        send_thread = threading.Thread(target=send_periodic_message)
        send_thread.start()
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Periodic sender is already running"}), 400

@app.route('/stop-sender', methods=['POST'])
def stop_periodic_sender():
    global send_thread

    if send_thread is not None and send_thread.is_alive():
        send_thread.join()
        send_thread = None
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Periodic sender is not running"}), 400

if __name__ == '__main__':
    app.run(debug=True)
