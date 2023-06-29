from azure.iot.device import IoTHubDeviceClient

def send_telemetry(device_connection_string, telemetry_data):
    # Create an instance of the IoTHubDeviceClient
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    # Connect to IoT Hub
    client.connect()

    # Send the telemetry data to the device twin
    client.patch_twin_reported_properties(telemetry_data)

    # Disconnect from IoT Hub
    client.disconnect()

if __name__ == '__main__':
    # Define the device connection string and telemetry data
    connection_string = "HostName=your-iot-hub.azure-devices.net;DeviceId=your-device-id;SharedAccessKey=your-shared-access-key"
    telemetry_data = {
        "sensor": "unique_key",
        "temperature": 25.5,
        "humidity": 60.2
    }

    # Send telemetry data to device twin
    send_telemetry(connection_string, telemetry_data)
