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
            can_id, *can_data = candump.split("_")  # Use *can_data to capture all remaining values

            if can_id.isnumeric():
                # Convert can_id to integer
                can_id = int(can_id)

                # Convert can_data list elements to integers (excluding non-integer values)
                can_data = [int(byte) for byte in can_data if byte.isdigit()]

                send_can_message(bus, can_id, can_data)

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
