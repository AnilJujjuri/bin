from azure.iot.device import IoTHubDeviceClient

device_connection_string = "HostName=<your-iothub-hostname>;DeviceId=<your-device-id>;SharedAccessKey=<your-shared-access-key>"

# Create an instance of the IoTHubDeviceClient
client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

# Connect to the IoT Hub
client.connect()

# Define the sample data
sample_data = {
    "can_device_id": "my_can_device",
    "my_can_device": {
        "telemetry1": 42,
        "telemetry2": 3.14,
        "telemetry3": "value"
    }
}

# Send the sample data to the device twin
client.patch_twin_reported_properties(sample_data)

# Disconnect from the IoT Hub
client.disconnect()
