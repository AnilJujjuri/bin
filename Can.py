<azure.iot.device.iothub.sync_clients.IoTHubDeviceClient object at 0x7f905000ad00>
{'SendData': True, 'SendInterval': 5, 'CustomProperty': 2000, 'reported': {'CustomProperty': 2000, 'sensor_id': 123, 'temperature': 25.5, 'humidity': 60.2}, 'sensor_id': '001', 'temperature': 25.4, 'humidity': 63.2, '$version': 78}
Traceback (most recent call last):
  File "test3.py", line 54, in <module>
    main(debug = True)
  File "test3.py", line 47, in main
    send_can_message(bus, can_id, can_data)            # Print the converted telemetry data in candump format
  File "test3.py", line 5, in send_can_message
    message = can.Message(arbitration_id=can_id, data=data)
  File "/usr/local/lib/python3.8/dist-packages/can/message.py", line 97, in __init__
    self.data = bytearray(data)
ValueError: byte must be in range(0, 256)
