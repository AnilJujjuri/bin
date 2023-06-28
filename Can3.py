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
            candump = convert_telemetry_to_candump(sensor_id, telemetry_data)
            can_id, can_data = candump.split("_")
            can_id = can_id.strip()
            can_data = [int(byte) for byte in can_data.split("_")]

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
  File "/home/azure/generic.py", line 49, in <module>
    main()
  File "/home/azure/generic.py", line 44, in main
    handle_device_twin_update(twin, bus)
  File "/home/azure/generic.py", line 30, in handle_device_twin_update
    can_data = [int(byte) for byte in can_data]
  File "/home/azure/generic.py", line 30, in <listcomp>
    can_data = [int(byte) for byte in can_data]
ValueError: invalid literal for int() with base 10: 'vibration'
