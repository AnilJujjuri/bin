from azure.iot.device import IoTHubDeviceClient
import can
import time
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('Configuration.env')
load_dotenv(dotenv_path=dotenv_path)

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
        self.last_messages = {}
        self.bus = bus

    def send_can_message(self, can_id, can_data):
        message_key = f"{can_id}_{can_data}"
        if message_key not in self.last_messages:
            self.last_messages[message_key] = True
            send_can_message(self.bus, can_id, can_data)

def handle_device_twin_update(twin, can_controller):
    reported_properties = twin.get("reported", {})
    can_device_id = twin.get("can_device_id", "")

    if not reported_properties:  # Skip if reported properties is empty
        return

    for can_device_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            candump, can_data, can_id = convert_telemetry_to_candump(telemetry_data)
            if candump is not None and can_data is not None:
                can_controller.send_can_message(can_id, can_data)

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = os.environ.get('device_connection_string')
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    client.connect()
    retry_counter = 0
    can_controller = CanController(bus)
    while True:
        try:
            twin = client.get_twin()
            handle_device_twin_update(twin, can_controller)
            # Retry mechanism
            if retry_counter < 3:
                time.sleep(30)  # Wait for 20 seconds between retries
                retry_counter += 1
            else:
                break  # Disconnect after the maximum number of retries
        except Exception as e:
            print("Exception caught:", str(e))
            continue

    client.disconnect()

if __name__ == '__main__':
    main()

Traceback (most recent call last):
  File "/usr/local/lib/python3.8/dist-packages/azure/iot/device/common/auth/connection_string.py", line 37, in _parse_connection_string
    cs_args = connection_string.split(CS_DELIMITER)
AttributeError: 'NoneType' object has no attribute 'split'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/Machine1/can_connector/can_connector/src/new.py", line 98, in <module>
    main()
  File "/home/Machine1/can_connector/can_connector/src/new.py", line 76, in main
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
  File "/usr/local/lib/python3.8/dist-packages/azure/iot/device/patch_documentation.py", line 84, in create_from_connection_string
    return super(IoTHubDeviceClient, cls).create_from_connection_string(
  File "/usr/local/lib/python3.8/dist-packages/azure/iot/device/iothub/abstract_clients.py", line 284, in create_from_connection_string
    connection_string = cs.ConnectionString(connection_string)
  File "/usr/local/lib/python3.8/dist-packages/azure/iot/device/common/auth/connection_string.py", line 86, in __init__
    self._dict = _parse_connection_string(connection_string)
  File "/usr/local/lib/python3.8/dist-packages/azure/iot/device/common/auth/connection_string.py", line 39, in _parse_connection_string
    raise TypeError("Connection String must be of type str")
TypeError: Connection String must be of type str
SocketcanBus was not properly shut down
