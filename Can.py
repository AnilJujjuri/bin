import can

def send_can_message(bus, arbitration_id, data):
    message = can.Message(arbitration_id=arbitration_id, data=data)
    bus.send(message)

def receive_can_messages(bus):
    while True:
        message = bus.recv(timeout=1.0)
        if message is None:
            break
        print("Received message:", message)

def main():
    # Create a CAN bus interface
    bus = can.interface.Bus(bustype='virtual', channel='can0')

    try:
        # Send a CAN message
        send_can_message(bus, arbitration_id=0x123, data=[0x01, 0x02, 0x03])

        # Receive CAN messages
        receive_can_messages(bus)

    except can.CanError as e:
        print("CAN error:", str(e))

    finally:
        # Properly shut down the CAN bus interface
        bus.shutdown()

if __name__ == '__main__':
    main()
