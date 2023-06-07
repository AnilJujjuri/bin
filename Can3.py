import can
import threading
import time

# Define the desired message IDs to filter
desired_message_ids = [0x100, 0x200]

# Message counters
sent_message_count = 0
received_message_count = 0


def send_can_message(bus, arbitration_id, data):
    global sent_message_count

    message = can.Message(arbitration_id=arbitration_id, data=data)
    bus.send(message)
    sent_message_count += 1
    print(f"Sent message: ID={hex(arbitration_id)}, Data={data}")


def receive_can_messages(bus):
    global received_message_count

    while True:
        message = bus.recv(timeout=1.0)
        if message is None:
            break

        received_message_count += 1
        print(f"Received message: ID={hex(message.arbitration_id)}, Data={message.data}")


def periodic_message_sender(bus):
    # Define the periodic message details
    periodic_message_id = 0x300
    periodic_message_data = [0xAA, 0xBB, 0xCC]
    period_sec = 1.0

    while True:
        send_can_message(bus, periodic_message_id, periodic_message_data)
        time.sleep(period_sec)


def main():
    # Create a CAN bus interface with the appropriate backend for Windows
    # Change the channel and bitrate as per your CAN interface configuration
    bus = can.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)

    # Create and start the thread for periodic message sending
    sender_thread = threading.Thread(target=periodic_message_sender, args=(bus,))
    sender_thread.start()

    try:
        # Start receiving CAN messages
        receive_can_messages(bus)

    except can.CanError as e:
        print("CAN error:", str(e))

    finally:
        # Stop the sender thread
        sender_thread.join()

        # Properly shut down the CAN bus interface
        bus.shutdown()


if __name__ == '__main__':
    main()
