Traceback (most recent call last):
  File "/home/azure/test11.py", line 69, in <module>
    main(debug=True)
  File "/home/azure/test11.py", line 59, in main
    handle_device_twin_update(twin, bus)
  File "/home/azure/test11.py", line 47, in handle_device_twin_update
    send_can_message(bus, int(can_id), can_data)
  File "/home/azure/test11.py", line 7, in send_can_message
    message_data=bytes(data)
ValueError: bytes must be in range(0, 256)
SocketcanBus was not properly shut down
