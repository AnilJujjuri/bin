from azure.iot.device import IoTHubDeviceClient
import can
import csv
import os

def receive_can_messages(bus):
    csv_file = 'received_can_messages.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a+', newline='') as csvfile:
        fieldnames = ['Timestamp', 'CAN_ID', 'CAN_Data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:  # If the file doesn't exist, write the header
            writer.writeheader()

        while True:
            message = bus.recv()
            can_id = message.arbitration_id
            can_data = message.data.hex()
            timestamp = message.timestamp

            writer.writerow({'Timestamp': timestamp, 'CAN_ID': can_id, 'CAN_Data': can_data})
            csvfile.flush()  # Flush the buffer to ensure immediate write to the file

            print(f"Received CAN message: {message}")

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    receive_can_messages(bus)

if __name__ == '__main__':
    main()
