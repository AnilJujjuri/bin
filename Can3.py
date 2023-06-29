from azure.iot.device import IoTHubDeviceClient
import can
import time

def send_can_message(bus, can_id, data):
    can_data = [byte % 256 for byte in data]
    message = can.Message(arbitration_id=can_id, data=can_data)
    bus.send(message)

def convert_telemetry_to_candump(sensor_id, telemetry_data):
    candump = f"{sensor_id}_"

    for key, value in telemetry_data.items():
        if isinstance(value, int):
            value = int(value)
        elif isinstance(value, float):
            value = int(value * 100)
        elif isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    continue  # Skip this key-value pair if conversion is not possible

        # Skip the value if it is zero
        if value == 0:
            continue

        value = max(min(value, 255), 0)
        candump += f"{key}_{value}_"

    return candump.rstrip("_")

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
            time.sleep(10)  # Wait for 10 seconds between retries
            retry_counter += 1
        else:
            break  # Disconnect after the maximum number of retries
    client.disconnect()

if __name__ == '__main__':
    main(debug=True)
