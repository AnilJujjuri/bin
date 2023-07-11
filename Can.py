from azure.iot.device import IoTHubDeviceClient
import can
import csv
import os

def receive_can_messages(bus):
    csv_file = 'received_can_messages.csv'
    file_exists = os.path.isfile(csv_file)
    existing_data = set()

    if file_exists:
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            print(f"Field names in the CSV file: {fieldnames}")
            for row in reader:
                # Convert CAN_ID and CAN_Data to string for comparison
                can_id = str(row['CAN_ID'])
                can_data = str(row['CAN_Data'])
                existing_data.add((can_id, can_data))

    with open(csv_file, 'a+', newline='') as csvfile:
        fieldnames = ['Timestamp', 'CAN_ID', 'CAN_Data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        while True:
            message = bus.recv()
            can_id = str(message.arbitration_id)
            can_data = str(message.data.hex())

            if (can_id, can_data) in existing_data:
                # Skip writing the data if it already exists
                continue

            timestamp = message.timestamp

            writer.writerow({'Timestamp': timestamp, 'CAN_ID': can_id, 'CAN_Data': can_data})
            csvfile.flush()

            print(f"Received CAN message: {message}")

            # Add the received CAN message to the existing data set
            existing_data.add((can_id, can_data))

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    receive_can_messages(bus)

if __name__ == '__main__':
    main()
