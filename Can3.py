Traceback (most recent call last):
  File "/home/azure/test11.py", line 60, in <module>
    main(debug=True)
  File "/home/azure/test11.py", line 50, in main
    handle_device_twin_update(twin, bus)
  File "/home/azure/test11.py", line 38, in handle_device_twin_update
    send_can_message(bus, int(can_id), can_data)
  File "/home/azure/test11.py", line 7, in send_can_message
    message = can.Message(arbitration_id=can_id, data=data)
  File "/home/Machine1/.local/lib/python3.8/site-packages/can/message.py", line 97, in __init__
    self.data = bytearray(data)
ValueError: byte must be in range(0, 256)
