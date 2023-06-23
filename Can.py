 def run(self):
        # Initialize CAN communication
        #bus = can.interface.Bus(channel=self.can_interface, bustype="socketcan_native")
        bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
        while True:
            # Receive CAN messages
            can_messages = bus.recv()

            # Process CAN messages
            for message in can_messages:
                # Process the received CAN message and extract the desired data
                data = process_can_message(message)

                # Update the desired properties with the extracted data
                self.properties["desired"].update(data)
                if self.on_property_update_callback:
                    self.on_property_update_callback(self.properties["desired"])

                # Update the reported properties in the device twin
                self.update_property(data)

            time.sleep(1)

def process_can_message(message):
    # Extract the desired data from the CAN message
    data = {
        "can_id": message.arbitration_id,
        "can_data": message.data,
        "can_timestamp": message.timestamp,
    }
    return data
from azure.iot.device import IoTHubModuleClient
import logging

from azurecom import CommunicationModule
logger = logging.getLogger(__name__)

can='vcan0'
connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;ModuleId=SimulatedTemperatureSensor;SharedAccessKey=v1cnONzs99unf3XKKACDfx0E69/bE5INBg/o0A7sKXw="
client = IoTHubModuleClient.create_from_connection_string(connection_string)
logger.info(f"self.client in connect if: {client}")
print(client)
# properties = client.get_twin()
# print(properties)

with CommunicationModule(connection_string=connection_string) as module:
    properties=module.get_properties()
    print(properties)

    print(module.run())
    data_to_insert={"sensor_id":123,"temperature": 25.5,"humidity": 60.2}
    module.update_property(data_to_insert)

    properties=module.get_properties()
    print(properties)

