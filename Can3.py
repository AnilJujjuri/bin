import time
from azure.iot.device import IoTHubDeviceClient

def send_telemetry_data(device_client, sensor_id, telemetry_data):
    properties = {
        "sensor_" + str(sensor_id): telemetry_data
    }
    device_client.patch_twin_reported_properties(properties)

def main():
    device_connection_string = "HostName=your-iot-hub.azure-devices.net;DeviceId=your-device-id;SharedAccessKey=your-shared-access-key"
    device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    device_client.connect()

    sensor_id = 1234

    while True:
        # Generate sample telemetry data
        temperature = 25.5
        humidity = 60.0
        vibration = "high"

        # Create a dictionary to hold the telemetry data
        telemetry_data = {
            "temperature": temperature,
            "humidity": humidity,
            "vibration": vibration
        }

        # Send the telemetry data to the device twin
        send_telemetry_data(device_client, sensor_id, telemetry_data)

        time.sleep(5)  # Wait for 5 seconds before sending the next data

    device_client.disconnect()

if __name__ == '__main__':
    main()
