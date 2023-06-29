from azure.iot.device import IoTHubDeviceClient
import can
import time

def send_can_message(bus, can_id, data):
    message = can.Message(arbitration_id=can_id, data=data)
    bus.send(message)
    print (message)
    

def convert_telemetry_to_candump(sensor_id, telemetry_data):
    candump = f"{sensor_id}_"
    can_data = []

    for key, value in telemetry_data.items():
        if isinstance(value, int):
            byte_value = value % 256
        elif isinstance(value, float):
            byte_value = int(value) % 256
        elif isinstance(value, str):
            try:
                byte_value = int(value) % 256
            except ValueError:
                try:
                    byte_value = int(float(value)) % 256
                except ValueError:
                    continue  # Skip this key-value pair if conversion is not possible
        else:
            continue  # Skip unsupported data types

        can_data.append(byte_value)
        candump += f"{key}_{byte_value}_"

    return candump.rstrip("_"), can_data

def handle_device_twin_update(twin, bus):
    reported_properties = twin["reported"]

    for sensor_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            can_id_parts = sensor_id.split("_")
            if len(can_id_parts) >= 2 and can_id_parts[1].isnumeric():
                can_id = int(can_id_parts[1])
                candump, can_data = convert_telemetry_to_candump(sensor_id, telemetry_data)
                
                send_can_message(bus, can_id, can_data)

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    device_connection_string = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=nodered;SharedAccessKey=mOeGufRBpvjmFut51ghJ0gjmWZDR8BHN1WWJtdsrBY4="
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    client.connect()
    retry_counter = 0 
    while True:
        twin = client.get_twin()
        handle_device_twin_update(twin, bus)
        # Retry mechanism
        if retry_counter < 3:
            time.sleep(10)  # Wait for 10 seconds between retries
            retry_counter += 1
        else:
            break  # Disconnect after the maximum number of retries
    client.disconnect()
    
    
if __name__ == '__main__':
    main()


Timestamp:        0.000000    ID: 000004d2    X Rx                DL:  2    19 3c
Timestamp:        0.000000    ID: 000004d3    X Rx                DL:  3    03 19 28
Timestamp:        0.000000    ID: 0000007d    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007e    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007f    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 00000082    X Rx                DL:  3    05 1c 3c
Timestamp:        0.000000    ID: 00000083    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 00000087    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 0000008b    X Rx                DL:  3    04 1c 3c
Timestamp:        0.000000    ID: 0000008c    X Rx                DL:  3    04 1d 3e
Timestamp:        0.000000    ID: 00000091    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000093    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000094    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000095    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000092    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000097    X Rx                DL:  3    07 23 46
Timestamp:        0.000000    ID: 00000098    X Rx                DL:  3    05 23 46
Timestamp:        0.000000    ID: 00000099    X Rx                DL:  4    07 23 46 04
Timestamp:        0.000000    ID: 0000009a    X Rx                DL:  4    07 23 46 04
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Timestamp:        0.000000    ID: 000004d2    X Rx                DL:  2    19 3c
Timestamp:        0.000000    ID: 000004d3    X Rx                DL:  3    03 19 28
Timestamp:        0.000000    ID: 0000007d    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007e    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007f    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 00000082    X Rx                DL:  3    05 1c 3c
Timestamp:        0.000000    ID: 00000083    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 00000087    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 0000008b    X Rx                DL:  3    04 1c 3c
Timestamp:        0.000000    ID: 0000008c    X Rx                DL:  3    04 1d 3e
Timestamp:        0.000000    ID: 00000091    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000093    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000094    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000095    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000092    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000097    X Rx                DL:  3    07 23 46
Timestamp:        0.000000    ID: 00000098    X Rx                DL:  3    05 23 46
Timestamp:        0.000000    ID: 00000099    X Rx                DL:  4    07 23 46 04
Timestamp:        0.000000    ID: 0000009a    X Rx                DL:  4    07 23 46 04
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Timestamp:        0.000000    ID: 000004d2    X Rx                DL:  2    19 3c
Timestamp:        0.000000    ID: 000004d3    X Rx                DL:  3    03 19 28
Timestamp:        0.000000    ID: 0000007d    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007e    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007f    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 00000082    X Rx                DL:  3    05 1c 3c
Timestamp:        0.000000    ID: 00000083    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 00000087    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 0000008b    X Rx                DL:  3    04 1c 3c
Timestamp:        0.000000    ID: 0000008c    X Rx                DL:  3    04 1d 3e
Timestamp:        0.000000    ID: 00000091    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000093    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000094    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000095    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000092    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000097    X Rx                DL:  3    07 23 46
Timestamp:        0.000000    ID: 00000098    X Rx                DL:  3    05 23 46
Timestamp:        0.000000    ID: 00000099    X Rx                DL:  4    07 23 46 04
Timestamp:        0.000000    ID: 0000009a    X Rx                DL:  4    07 23 46 04
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Exception caught in background thread.  Unable to handle.
['azure.iot.device.common.transport_exceptions.ConnectionDroppedError: Unexpected disconnection\n']
Timestamp:        0.000000    ID: 000004d2    X Rx                DL:  2    19 3c
Timestamp:        0.000000    ID: 000004d3    X Rx                DL:  3    03 19 28
Timestamp:        0.000000    ID: 0000007d    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007e    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 0000007f    X Rx                DL:  3    06 1c 3c
Timestamp:        0.000000    ID: 00000082    X Rx                DL:  3    05 1c 3c
Timestamp:        0.000000    ID: 00000083    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 00000087    X Rx                DL:  2    1c 3c
Timestamp:        0.000000    ID: 0000008b    X Rx                DL:  3    04 1c 3c
Timestamp:        0.000000    ID: 0000008c    X Rx                DL:  3    04 1d 3e
Timestamp:        0.000000    ID: 00000091    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000093    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000094    X Rx                DL:  3    04 21 46
Timestamp:        0.000000    ID: 00000095    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000092    X Rx                DL:  3    04 23 46
Timestamp:        0.000000    ID: 00000097    X Rx                DL:  3    07 23 46
Timestamp:        0.000000    ID: 00000098    X Rx                DL:  3    05 23 46
Timestamp:        0.000000    ID: 00000099    X Rx                DL:  4    07 23 46 04
Timestamp:        0.000000    ID: 0000009a    X Rx                DL:  4    07 23 46 04
