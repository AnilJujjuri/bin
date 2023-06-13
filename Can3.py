import can
from flask import Flask, jsonify

app = Flask(__name__)

# Set up CAN interface
can_interface = "vcan0"
bus = can.interface.Bus(channel=can_interface, bustype="socketcan")

@app.route("/")
def home():
    return "CAN API"

@app.route("/send/<int:id>/<int:data>")
def send_can_message(id, data):
    message = can.Message(arbitration_id=id, data=[data], extended_id=False)
    bus.send(message)
    return jsonify({"status": "success"})

@app.route("/receive")
def receive_can_message():
    message = bus.recv()
    return jsonify({"id": message.arbitration_id, "data": message.data[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    
