import can

def main():
    # Create a CAN bus interface
    bus = can.Bus(interface='socketcan', channel='can0')

    try:
        # Send a CAN message
        message = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03])
        bus.send(message)

        # Receive CAN messages
        while True:
            received_message = bus.recv(timeout=1.0)
            if received_message is None:
                break
            print("Received message:", received_message)

    except can.CanError as e:
        print("CAN error:", str(e))

    finally:
        # Close the CAN bus interface
        bus.shutdown()

if __name__ == '__main__':
    main()
