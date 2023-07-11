import can
import csv
import os

def receive_can_messages(bus):
    csv_file = 'received_can_messages.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:  # If the file doesn't exist, write the header
            writer.writerow(['Timestamp', 'ID', 'Direction', 'DLC', 'Data', 'Channel'])  # Write the header row

        while True:
            message = bus.recv()
            timestamp = message.timestamp
            can_id = message.arbitration_id
            direction = 'Rx' if message.is_received else 'Tx'
            dlc = message.dlc
            data = ' '.join([f'{byte:02X}' for byte in message.data])
            channel = bus.channel_info

            writer.writerow([timestamp, can_id, direction, dlc, data, channel])  # Write the data row

            print(f"Received CAN message: Timestamp: {timestamp}    ID: {can_id:08X}    {direction:<4}                DL: {dlc:<2}    {data:26}    Channel: {channel}")

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    receive_can_messages(bus)

if __name__ == '__main__':
    main()
