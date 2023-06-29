Traceback (most recent call last):
  File "/home/Machine1/.local/lib/python3.8/site-packages/can/interfaces/socketcan/socketcan.py", line 792, in _send_once
    sent = self.socket.send(data)
OSError: [Errno 22] Invalid argument

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/azure/test11.py", line 55, in <module>
    main(debug=True)
  File "/home/azure/test11.py", line 45, in main
    handle_device_twin_update(twin, bus)
  File "/home/azure/test11.py", line 33, in handle_device_twin_update
    send_can_message(bus, can_id, can_data)
  File "/home/azure/test11.py", line 8, in send_can_message
    bus.send(message)
  File "/home/Machine1/.local/lib/python3.8/site-packages/can/interfaces/socketcan/socketcan.py", line 777, in send
    sent = self._send_once(data, channel)
  File "/home/Machine1/.local/lib/python3.8/site-packages/can/interfaces/socketcan/socketcan.py", line 794, in _send_once
    raise can.CanOperationError(
can.exceptions.CanOperationError: Failed to transmit: Invalid argument [Error Code 22]
