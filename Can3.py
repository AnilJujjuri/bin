from azure.iot.device import IoTHubDeviceClient
import can
import time

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)
    print(message)

def convert_telemetry_to_candump(sensor_id, telemetry_data):
    candump = f"{sensor_id}_"
    can_data = []

    for key, value in telemetry_data.items():
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

    return candump.rstrip("_"), can_data

class CanController:
    def __init__(self):
        self.last_messages = {}

    def send_can_message(self, can_id, can_data):
        message_key = f"{can_id}_{can_data}"
        if message_key not in self.last_messages:
            self.last_messages[message_key] = True
            send_can_message(bus, can_id, can_data)

def handle_device_twin_update(twin, can_controller):
    reported_properties = twin["reported"]

    for sensor_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            can_id_parts = sensor_id.split("_")
            if len(can_id_parts) >= 2 and can_id_parts[1].isnumeric():
                can_id = int(can_id_parts[1])
                candump, can_data = convert_telemetry_to_candump(sensor_id, telemetry_data)

                can_controller.send_can_message(can_id, can_data)

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;SharedAccessKey=mOeGufRBpvjmFut51ghJ0gjmWZDR8BHN1WWJtdsrBY4="
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    client.connect()
    retry_counter = 0
    can_controller = CanController()
    while True:
        try:
            twin = client.get_twin()
            handle_device_twin_update(twin, can_controller)
            # Retry mechanism
            if retry_counter < 3:
                time.sleep(10)  # Wait for 10 seconds between retries
                retry_counter += 1
            else:
                break  # Disconnect after the maximum number of retries
        except Exception as e:
            print("Exception caught:", str(e))
            continue

    client.disconnect()

if __name__ == '__main__':
    main()
