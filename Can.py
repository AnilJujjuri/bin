from azure.iot.device import IoTHubDeviceClient
import can
import time

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)

def convert_telemetry_to_candump(telemetry):
    # Convert telemetry data to candump format
    # Adjust the conversion logic based on your specific telemetry data structure
    sensor_id = telemetry["sensor_id"]
    temperature = int(telemetry["temperature"] * 10)  # Scale and convert to integer
    humidity = int(telemetry["humidity"] * 10)  # Scale and convert to integer

    candump = f"{sensor_id} #{temperature:02X}{humidity:02X}"

    return candump

def main(debug=False):
    # Create a CAN bus instance for the 'vcan0' interface
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    # Create an instance of the IoTHubDeviceClient
    device_connection_string = "<Your Device Connection String>"
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    # Connect to IoT Hub
    client.connect()

    # Start receiving and processing device twin updates
    while True:
        twin = client.get_twin()
        desired_properties = twin["desired"]

        # Check if there are desired properties related to telemetry
        if "telemetry" in desired_properties:
            telemetry = desired_properties["telemetry"]
            candump = convert_telemetry_to_candump(telemetry)

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
