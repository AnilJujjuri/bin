from azure.iot.device import IoTHubDeviceClient
import can
import time
import struct

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)

def convert_telemetry_to_candump(sensor_id, telemetry_data):
    candump = f"{sensor_id}_"

    for key, value in telemetry_data.items():
        if isinstance(value, int):
            value = int(value)
        elif isinstance(value, float):
            value_bytes = struct.pack('!f', value)  # Convert float to IEEE 754 binary representation (4 bytes)
            value_ints = struct.unpack('BBBB', value_bytes)  # Unpack the 4 bytes into individual integers
            value = [int(byte) % 256 for byte in value_ints]  # Convert and limit values to valid range

        candump += f"{key}_{'_'.join(map(str, value))}_"  # Append key-value pair to the candump string

    return candump.rstrip("_")  # Remove the trailing underscore

def handle_device_twin_update(twin, bus):
    reported_properties = twin["reported"]

    for sensor_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            can_id_parts = sensor_id.split("_")
            if len(can_id_parts) >= 2 and can_id_parts[1].isnumeric():
                can_id = can_id_parts[1]

                candump = convert_telemetry_to_candump(sensor_id, telemetry_data)

                can_data = [int(byte) for byte in candump.split("_")[1:] if byte.isnumeric()]

                send_can_message(bus, int(can_id), can_data)

def main(debug=False):
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;SharedAccessKey=mOeGufRBpvjmFut51ghJ0gjmWZDR8BHN1WWJtdsrBY4="
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    client.connect()
    retry_counter = 0 
    while True:
        twin = client.get_twin()
        handle_device_twin_update(twin, bus)
        # Retry mechanism
        if retry_counter < 3:
            time.sleep(100)  # Wait for 10 seconds between retries
            retry_counter += 1
        else:
            break  # Disconnect after the maximum number of retries
    client.disconnect()

if __name__ == '__main__':
    main(debug=True)
