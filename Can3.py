from azure.iot.device import IoTHubDeviceClient
import can
import time

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)

def convert_telemetry_to_candump(sensor_id, temperature, humidity):
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

    # Initialize the flag to track if the message has been sent
    message_sent = False

    # Start receiving and processing device twin updates
    while True:
        twin = client.get_twin()
        reported_properties = twin["reported"]

        # Check if there are reported properties related to temperature, humidity, and sensor_id
        if "temperature" in reported_properties and "humidity" in reported_properties and "sensor_id" in reported_properties:
            temperature = reported_properties["temperature"]
            humidity = reported_properties["humidity"]
            sensor_id = reported_properties["sensor_id"]

            # If the message has not been sent, send it
            if not message_sent:
                candump = convert_telemetry_to_candump(sensor_id, temperature, humidity)
                can_id, can_data = candump.split("#")
                can_id = can_id.strip()  # Remove extra whitespace
                can_data = [int(can_data[i:i+2], 16) for i in range(0, len(can_data), 2)]
                send_can_message(bus, int(sensor_id), can_data)
                message_sent = True

        # If the message has been sent, update the data
        if message_sent:
            # Update the telemetry data as needed
            temperature += 1.0
            humidity += 1.0

        # Reset the flag to allow sending a new message in the next iteration
        message_sent = False

        # Wait for some time before checking for device twin updates again
        time.sleep(1)

    # Disconnect from IoT Hub
    client.disconnect()

if __name__ == '__main__':
    main(debug=True)
