import can

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data, extended_id=False)
    bus.send(message)

def main():
    # Create a CAN bus instance for the 'vcan0' interface
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    # Telemetry data
    sensor_id = 0x123
    temperature = 25
    humidity = 60

    # Construct CAN message data
    can_data = [temperature, humidity]

    # Send CAN message
    send_can_message(bus, sensor_id, can_data)

if __name__ == '__main__':
    main()
