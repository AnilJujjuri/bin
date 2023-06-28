from azure.iot.device import IoTHubDeviceClient
import can

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)

def convert_telemetry_to_candump(sensor_id, telemetry_data):
    # Convert telemetry data to candump format
    # Adjust the conversion logic based on your specific telemetry data structure

    candump = f"{sensor_id}_"

    for key, value in telemetry_data.items():
        if isinstance(value, int):
            value = int(value)  # Convert to integer

        candump += f"{key}_{value}_"  # Append key-value pair to the candump string

    return candump.rstrip("_")  # Remove the trailing underscore

def handle_device_twin_update(twin, bus):
    reported_properties = twin["reported"]

    for sensor_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            can_id_parts = sensor_id.split("_")  # Split the sensor_id to get the parts
            if len(can_id_parts) >= 2 and can_id_parts[1].isnumeric():
                can_id = can_id_parts[1]  # The numeric part is the can_id

                candump = convert_telemetry_to_candump(sensor_id, telemetry_data)
                can_data = [int(byte) for byte in candump.split("_")[1:] if byte.isnumeric()]  # Skip the first part if numeric

                send_can_message(bus, int(can_id), can_data)

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;SharedAccessKey=mOeGufRBpvjmFut51ghJ0gjmWZDR8BHN1WWJtdsrBY4="
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    client.connect()

    while True:
        twin = client.get_twin()
        handle_device_twin_update(twin, bus)

    client.disconnect()

if __name__ == '__main__':
    main()

Traceback (most recent call last):
  File "/home/azure/generic.py", line 51, in <module>
    main()
  File "/home/azure/generic.py", line 46, in main
    handle_device_twin_update(twin, bus)
  File "/home/azure/generic.py", line 34, in handle_device_twin_update
    send_can_message(bus, int(can_id), can_data)
  File "/home/azure/generic.py", line 5, in send_can_message
    message = can.Message(arbitration_id=can_id, data=data)
  File "/home/Machine1/.local/lib/python3.8/site-packages/can/message.py", line 97, in __init__
    self.data = bytearray(data)
ValueError: byte must be in range(0, 256)
SocketcanBus was not properly shut down
