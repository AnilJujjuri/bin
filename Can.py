import can
import csv
import os

def receive_can_messages(bus):
    csv_file = 'received_can_messages.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a+', newline='') as csvfile:
        fieldnames = ['Timestamp', 'ID', 'DLC', 'Data', 'Channel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:  # If the file doesn't exist, write the header
            writer.writeheader()

        while True:
            message = bus.recv()
            timestamp = message.timestamp
            can_id = message.arbitration_id
            dlc = message.dlc
            data = ' '.join([f'{byte:02X}' for byte in message.data])
            channel = bus.channel_info

            writer.writerow({'Timestamp': timestamp, 'ID': can_id, 'DLC': dlc, 'Data': data, 'Channel': channel})
            csvfile.flush()  # Flush the buffer to ensure immediate write to the file

            print(f"Received CAN message: Timestamp: {timestamp}    ID: {can_id:08X}    DL: {dlc:<2}    {data:26}    Channel: {channel}")

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    receive_can_messages(bus)

if __name__ == '__main__':
    main()
