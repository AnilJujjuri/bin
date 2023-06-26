from azure.iot.device import IoTHubDeviceClient

def send_telemetry(device_connection_string, telemetry):
    # Create an instance of the IoTHubDeviceClient
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    # Connect to IoT Hub
    client.connect()

    # Send the telemetry data to the device twin
    client.patch_twin_reported_properties(telemetry)

    # Disconnect from IoT Hub
    client.disconnect()

if __name__ == '__main__':
    # Define the device connection string and telemetry data
    connection_string = "<your-device-connection-string>"
    telemetry_data = {
        "sensor_id": "001",
        "temperature": 25.4,
        "humidity": 63.2
    }

    # Send telemetry data to device twin
    send_telemetry(connection_string, telemetry_data)
