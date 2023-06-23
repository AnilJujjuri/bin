import can
import logging
from azure.iot.device import IoTHubModuleClient

logger = logging.getLogger(__name__)

class CommunicationModule:
    def __init__(self, connection_string=None, can_interface=None):
        self.connection_string = connection_string
        self.can_interface = can_interface
        self.client = None

    def connect(self):
        logger.info(f"Connecting: {self.connection_string}")
        self.client = IoTHubModuleClient.create_from_connection_string(self.connection_string)
        self.client.connect()

        # Initialize CAN communication
        bus = can.interface.Bus(channel=self.can_interface, bustype="socketcan")

        while True:
            # Receive CAN messages
            can_messages = bus.recv()

            # Process CAN messages
            for message in can_messages:
                # Process the received CAN message and extract the desired data
                data = {
                    "can_id": message.arbitration_id,
                    "can_data": message.data,
                    "can_timestamp": message.timestamp,
                }
                print("Received CAN data:", data)

                # Send the data to device twin
                self.send_data_to_twin(data)

    def send_data_to_twin(self, data):
        reported_properties = {"reported": data}
        self.client.patch_twin_reported_properties(reported_properties)

    def disconnect(self):
        if self.client:
            self.client.shutdown()

if __name__ == "__main__":
    # Azure IoT Hub connection string
    connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;ModuleId=SimulatedTemperatureSensor;SharedAccessKey=v1cnONzs99unf3XKKACDfx0E69/bE5INBg/o0A7sKXw="

    # CAN interface name
    can_interface = "vcan0"

    # Instantiate the CommunicationModule
    module = CommunicationModule(connection_string=connection_string, can_interface=can_interface)

    try:
        # Connect to Azure IoT Hub and start listening to CAN bus
        module.connect()
    except KeyboardInterrupt:
        pass
    finally:
        # Disconnect from Azure IoT Hub
        module.disconnect()
