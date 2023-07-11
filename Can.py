from azure.iot.device import IoTHubDeviceClient
import can
import csv
import threading
import time

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)

def convert_telemetry_to_candump(telemetry_data):
    candump = ""
    can_data = []
    can_id = 1001  # Default value

    for key, value in telemetry_data.items():
        if key == "can_id":
            if isinstance(value, int):
                can_id = value
            elif isinstance(value, str) and value.isdigit():
                can_id = int(value)
            continue

        if isinstance(value, int):
            byte_value = value % 256
        elif isinstance(value, float):
            byte_value = int(value) % 256
        elif isinstance(value, str):
            try:
                byte_value = int(value) % 256
            except ValueError:
                try:
                    byte_value = int(float(value)) % 256
                except ValueError:
                    continue  # Skip this key-value pair if conversion is not possible
        else:
            continue  # Skip unsupported data types

        can_data.append(byte_value)
        candump += f"{key}_{byte_value}_"

    return candump.rstrip("_"), can_data, can_id

class CanController:
    def __init__(self, bus):
        self.bus = bus

    def send_can_message(self, can_id, can_data):
        send_can_message(self.bus, can_id, can_data)

def handle_device_twin_update(patch, can_controller):
    reported_properties = patch.get("reported", {})
    can_device_id = patch.get("can_device_id", "")

    if not reported_properties:  # Skip if reported properties is empty
        return

    for can_device_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            candump, can_data, can_id = convert_telemetry_to_candump(telemetry_data)
            if candump is not None and can_data is not None:
                can_controller.send_can_message(can_id, can_data)

def listen_and_store_can_messages(bus):
    with open('received_can_messages.csv', 'a+', newline='') as csvfile:
        fieldnames = ['Timestamp', 'CAN_ID', 'CAN_Data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the CSV file is empty
        csvfile.seek(0)
        if csvfile.read().strip() == '':
            writer.writeheader()

        while True:
            message = bus.recv()
            can_id = message.arbitration_id
            can_data = message.data
            timestamp = time.time()

            # Check if the message is already present in the CSV file
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            is_duplicate = False
            for row in reader:
                if row[1] == str(can_id) and row[2] == can_data.hex():
                    is_duplicate = True
                    break

            # Write the message to the CSV file if it is not a duplicate
            if not is_duplicate:
                writer.writerow({'Timestamp': timestamp, 'CAN_ID': can_id, 'CAN_Data': can_data.hex()})

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = "HostName=<your-iothub-hostname>;DeviceId=<your-device-id>;SharedAccessKey=<your-shared-access-key>"
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    can_controller = CanController(bus)

    def twin_update_handler(patch):
        handle_device_twin_update(patch, can_controller)

    client.connect()
    client.on_twin_desired_properties_patch_received = twin_update_handler

    listen_thread = threading.Thread(target=listen_and_store_can_messages, args=(bus,))
    listen_thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    client.disconnect()

if __name__ == '__main__':
    main()
