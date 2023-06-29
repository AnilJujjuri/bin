import time
from azure.iot.device import IoTHubDeviceClient

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
                can_data = [int(byte) % 256 for byte in candump.split("_")[1:] if byte.isnumeric()]  # Convert and limit values to valid range

                send_can_message(bus, int(can_id), can_data)

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;SharedAccessKey=mOeGufRBpvjmFut51ghJ0gjmWZDR8BHN1WWJtdsrBY4="
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    retry_count = 0
    retry_limit = 3
    retry_delay = 10

    while retry_count < retry_limit:
        try:
            client.connect()

            while True:
                twin = client.get_twin()
                handle_device_twin_update(twin, bus)

                time.sleep(1)

        except Exception as e:
            print("An error occurred:", str(e))
            retry_count += 1
            print(f"Retry attempt {retry_count}/{retry_limit}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

        finally:
            client.disconnect()

    print(f"Unable to establish connection after {retry_limit} attempts. Exiting...")

if __name__ == '__main__':
    main()
