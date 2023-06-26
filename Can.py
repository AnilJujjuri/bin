anilvm@Machine1:/home/azure$ python test3.py
/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (2.0.3) or chardet (5.1.0) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
<azure.iot.device.iothub.sync_clients.IoTHubDeviceClient object at 0x7fd0dc50dd00>
{'SendData': True, 'SendInterval': 5, 'CustomProperty': 2000, 'reported': {'CustomProperty': 2000, 'sensor_id': 123, 'temperature': 25.5, 'humidity': 60.2}, 'sensor_id': '001', 'temperature': 25.4, 'humidity': 63.2, '$version': 78}
Traceback (most recent call last):
  File "test3.py", line 50, in <module>
    main(debug = True)
  File "test3.py", line 43, in main
    send_can_message(bus, can_id, can_data)            # Print the converted telemetry data in candump format
  File "test3.py", line 5, in send_can_message
    message = can.Message(arbitration_id=can_id, data=data, extended_id=False)
TypeError: __init__() got an unexpected keyword argument 'extended_id'
SocketcanBus was not properly shut down
anilvm@Machine1:/home/azure$ sudo vi test3.py
anilvm@Machine1:/home/azure$ python test3.py
/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (2.0.3) or chardet (5.1.0) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
<azure.iot.device.iothub.sync_clients.IoTHubDeviceClient object at 0x7f0ec99b6d00>
{'SendData': True, 'SendInterval': 5, 'CustomProperty': 2000, 'reported': {'CustomProperty': 2000, 'sensor_id': 123, 'temperature': 25.5, 'humidity': 60.2}, 'sensor_id': '001', 'temperature': 25.4, 'humidity': 63.2, '$version': 78}
Traceback (most recent call last):
  File "/usr/local/lib/python3.8/dist-packages/can/message.py", line 97, in __init__
    self.data = bytearray(data)
TypeError: 'float' object cannot be interpreted as an integer

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "test3.py", line 50, in <module>
    main(debug = True)
  File "test3.py", line 43, in main
    send_can_message(bus, can_id, can_data)            # Print the converted telemetry data in candump format
  File "test3.py", line 5, in send_can_message
    message = can.Message(arbitration_id=can_id, data=data)
  File "/usr/local/lib/python3.8/dist-packages/can/message.py", line 100, in __init__
    raise TypeError(err) from error
TypeError: Couldn't create message from [25.4, 63.2] (<class 'list'>)
SocketcanBus was not properly shut down
