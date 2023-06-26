from azure.iot.device import IoTHubDeviceClient
import can
import time

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)

def convert_telemetry_to_candump(sensor_id,temperature, humidity):
    # Convert telemetry data to candump format
    # Adjust the conversion logic based on your specific telemetry data structure
    temperature = int(temperature * 10)  # Scale and convert to integer
    humidity = int(humidity * 10)  # Scale and convert to integer
    sensor_id = int(sensor_id * 10)
    candump = f"{sensor_id:02X} #{temperature:02X}{humidity:02X}"  # Assuming sensor_id is constant as '001'

    return candump

def main(debug=False):
    # Create a CAN bus instance for the 'vcan0' interface
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    # Create an instance of the IoTHubDeviceClient
    device_connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;ModuleId=SimulatedTemperatureSensor;SharedAccessKey=v1cnONzs99unf3XKKACDfx0E69/bE5INBg/o0A7sKXw="
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    # Connect to IoT Hub
    client.connect()

    # Start receiving and processing device twin updates
    while True:
        twin = client.get_twin()
        reported_properties = twin["reported"]

        # Check if there are reported properties related to temperature and humidity
        if "temperature" in reported_properties and "humidity" and "sensor_id" in reported_properties:
            temperature = reported_properties["temperature"]
            humidity = reported_properties["humidity"]
            sensor_id=reported_properties["sensor_id"]
            candump = convert_telemetry_to_candump(sensor_id,temperature, humidity)

            # Print the converted telemetry data in candump format
            print(candump)

            # Split the candump string into can_id and data
            can_id, can_data = candump.split("#")
            can_data = [int(can_data[i:i+2], 16) for i in range(0, len(can_data), 2)]

            # Send the CAN message
            send_can_message(bus, int(can_id), can_data)

        # Wait for some time before checking for device twin updates again
        time.sleep(1)

    # Disconnect from IoT Hub
    client.disconnect()

if __name__ == '__main__':
    main(debug=True)


/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (2.0.3) or chardet (5.1.0) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
33C0234FF4D400BC419A029 #FE278
Traceback (most recent call last):
  File "test6.py", line 59, in <module>
    main(debug=True)
  File "test6.py", line 50, in main
    send_can_message(bus, int(can_id), can_data)
ValueError: invalid literal for int() with base 10: '33C0234FF4D400BC419A029 '
SocketcanBus was not properly shut down
