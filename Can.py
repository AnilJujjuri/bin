import can

def receive_can_messages(bus):

    while True:

        message = bus.recv()

        print("Received message:", message)

def main():

    # Create a CAN bus object

    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    # Start a separate thread to receive CAN messages

    receiver_thread = can.ThreadSafeBus(bus, receive_own_messages=True)

    receiver_thread.start()

    # Send a CAN message

    message = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03])

    bus.send(message)

    # Wait for a while to receive messages

    input("Press Enter to stop receiving messages...\n")

    # Stop the receiver thread

    receiver_thread.stop()

if __name__ == "__main__":

    main()
