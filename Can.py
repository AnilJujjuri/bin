def main():
        # Initialize CAN communication
        bus = can.interface.Bus(channel=self.can_interface, bustype="socketcan")

        while True:
            # Receive CAN messages
            can_messages = bus.recv()

            # Process CAN messages
            for message in can_messages:
                # Process the received CAN message and extract the desired data
                data = process_can_message(message)

                # Update the desired properties with the extracted data
               # self.properties["desired"].update(data)
               # if self.on_property_update_callback:
                #    self.on_property_update_callback(self.properties["desired"])

                # Update the reported properties in the device twin
                print(data)

message={"sensorid":123,"temperature":23,"humidity":20}
def process_can_message(message):
    # Process and extract desired data from the CAN message
    data = {
        "can_id": message.arbitration_id,
        "can_data": message.data,
        "can_timestamp": message.timestamp,
    }
    return data
